import ctypes
from ctypes import Structure, c_float, c_uint32, sizeof, c_bool, c_int, c_void_p
import time
import sys
import math
import glm

from loguru import logger
import numpy as np

from crunge.core import as_capsule
from crunge import wgpu
import crunge.wgpu.utils as utils

from ..common import Demo

from .data import vertex_data


WORLD_AXIS_X = glm.vec3(1.0, 0.0, 0.0)
WORLD_AXIS_Y = glm.vec3(0.0, 1.0, 0.0)
WORLD_AXIS_Z = glm.vec3(0.0, 0.0, 1.0)
WORLD_SCALE = 1

# 32 is the maximum we can use here without going over the max binding size
# of a uniform buffer which is 65,536
x_count: int = 32
y_count: int = 32
num_instances: int = x_count * y_count

shader_code = """
struct Uniforms {
  modelViewProjectionMatrix : array<mat4x4<f32>, {{NUM_INSTANCES}}>,
}
@binding(0) @group(0) var<uniform> uniforms : Uniforms;

struct VertexInput {
  @builtin(instance_index) instance_idx : u32,
  @location(0) pos: vec4<f32>,
  @location(1) uv: vec2<f32>,
}

struct VertexOutput {
  @builtin(position) vertex_pos : vec4<f32>,
  @location(0) uv: vec2<f32>,
  @location(1) frag_colour: vec4<f32>,
}

@vertex
fn vs_main(in : VertexInput) -> VertexOutput {
  let vert_pos = uniforms.modelViewProjectionMatrix[in.instance_idx] * in.pos;
  let frag_colour = 0.5 * (in.pos + vec4(1));
  return VertexOutput(vert_pos, in.uv, frag_colour);
}

@fragment
fn fs_main(in : VertexOutput) -> @location(0) vec4<f32> {
  return in.frag_colour;
}
"""

shader_code = shader_code.replace("{{NUM_INSTANCES}}", str(num_instances))

# TODO: Use code from enginedemo/cubes/cubes.py


class CubesDemo(Demo):
    depth_stencil_view: wgpu.TextureView = None
    vertex_buffer: wgpu.Buffer = None

    kVertexCount = 36
    kPositionByteOffset = 0
    kUVByteOffset = 4 * sizeof(c_float)
    kCubeDataStride = 6

    def __init__(self):
        super().__init__()
        self.model_matrices = glm.array.zeros(num_instances, glm.mat4)
        for i in range(num_instances):
            self.model_matrices[i] = glm.mat4(1.0)

        self.mvp_matrices = glm.array.zeros(num_instances, glm.mat4)
        for i in range(num_instances):
            self.mvp_matrices[i] = glm.mat4(1.0)

        step = 4
        half_x = (x_count / 2) + 0.5
        half_y = (y_count / 2) + 0.5

        for x in range(x_count):
            for y in range(y_count):
                self.model_matrices[(x * y_count) + y] = glm.translate(
                    glm.mat4(1), glm.vec3(step * (x - half_x), step * (y - half_y), 0)
                )

    def resize(self, size: glm.ivec2):
        super().resize(size)
        self.create_depth_stencil_view()

    def create_device_objects(self):
        self.create_depth_stencil_view()
        self.create_buffers()
        self.create_pipeline()

    def create_depth_stencil_view(self):
        self.depthTexture = utils.create_texture(
            self.device,
            "Depth texture",
            wgpu.Extent3D(self.size.x, self.size.y),
            wgpu.TextureFormat.DEPTH24_PLUS,
            wgpu.TextureUsage.RENDER_ATTACHMENT,
        )
        self.depth_stencil_view = self.depthTexture.create_view()

    def create_pipeline(self):
        shader_module = self.create_shader_module(shader_code)

        # Pipeline creation

        vertAttributes = [
            wgpu.VertexAttribute(
                format=wgpu.VertexFormat.FLOAT32X4,
                offset=self.kPositionByteOffset,
                shader_location=0,
            ),
            wgpu.VertexAttribute(
                format=wgpu.VertexFormat.FLOAT32X2,
                offset=self.kUVByteOffset,
                shader_location=1,
            ),
        ]

        vertBufferLayouts = [
            wgpu.VertexBufferLayout(
                array_stride=self.kCubeDataStride * sizeof(c_float),
                attribute_count=2,
                attributes=vertAttributes,
            )
        ]

        color_targets = [wgpu.ColorTargetState(format=wgpu.TextureFormat.BGRA8_UNORM)]

        fragmentState = wgpu.FragmentState(
            module=shader_module,
            entry_point="fs_main",
            target_count=1,
            targets=color_targets,
        )

        depthStencilState = wgpu.DepthStencilState(
            format=wgpu.TextureFormat.DEPTH24_PLUS,
            depth_write_enabled=True,
            depth_compare=wgpu.CompareFunction.LESS,
        )

        primitive = wgpu.PrimitiveState(cull_mode=wgpu.CullMode.BACK)

        vertex_state = wgpu.VertexState(
            module=shader_module,
            entry_point="vs_main",
            buffer_count=1,
            buffers=vertBufferLayouts,
        )

        descriptor = wgpu.RenderPipelineDescriptor(
            label="Main Render Pipeline",
            vertex=vertex_state,
            primitive=primitive,
            depth_stencil=depthStencilState,
            fragment=fragmentState,
        )

        self.pipeline = self.device.create_render_pipeline(descriptor)

        bg_entries = [
            wgpu.BindGroupEntry(
                binding=0, buffer=self.uniformBuffer, size=self.uniformBufferSize
            )
        ]

        bindGroupDesc = wgpu.BindGroupDescriptor(
            label="Uniform bind group",
            layout=self.pipeline.get_bind_group_layout(0),
            entry_count=1,
            entries=bg_entries,
        )

        self.uniformBindGroup = self.device.create_bind_group(bindGroupDesc)

        aspect = float(self.kWidth) / float(self.kHeight)
        fov_y_radians = (2.0 * math.pi) / 5.0
        self.projectionMatrix = glm.perspective(fov_y_radians, aspect, 1.0, 100.0)

        # exit()

    """
    auto viewMatrix = dusk::Mat4::Translation(dusk::Vec3(0, 3, -92));
    viewMatrix = viewMatrix * dusk::Mat4::Rotation(30, dusk::Vec3(1., 0., 0.));
    """

    @property
    def transform_matrix(self):
        viewMatrix = glm.translate(glm.mat4(1.0), glm.vec3(0, 3, -92))
        viewMatrix = glm.scale(
            viewMatrix, glm.vec3(WORLD_SCALE, WORLD_SCALE, WORLD_SCALE)
        )
        rotMatrix = glm.rotate(glm.mat4(1.0), math.degrees(30), WORLD_AXIS_X)
        return self.projectionMatrix * viewMatrix * rotMatrix

    """
    auto update_transformation_matrices = [&]() {
        auto now_s = std::chrono::time_point_cast<std::chrono::milliseconds>(
            std::chrono::steady_clock::now());
        auto ms = float(now_s.time_since_epoch().count()) / 10000.f;

        for (size_t x = 0; x < x_count; x++) {
        for (size_t y = 0; y < y_count; y++) {
            auto rotMatrix = dusk::Mat4::Rotation(
                1, dusk::Vec3(sinf((float(x) + 0.5f) * ms),
                            cosf((float(y) + 0.5f) * ms), 0));

            auto movZ = dusk::Mat4::Translation(
                dusk::Vec3(0, 0, sinf((float(x) + 0.5f) * ms)));

            auto idx = (x * y_count) + y;
            mvp_matrices[idx] = projectionMatrix * viewMatrix *
                                (model_matrices[idx] * movZ) * rotMatrix;
        }
        }
    """

    # TODO: This is screwed up somehow ...
    def update_transformation_matrices(self):
        now = time.time()
        ms = round(now * 1000) / 1000
        for x in range(x_count):
            for y in range(y_count):
                rotMatrix = glm.rotate(
                    glm.mat4(1.0),
                    math.degrees(1),
                    glm.vec3(math.sin(x + 0.5) * ms, math.cos(y + 0.5), 0),
                )
                movZ = glm.translate(
                    glm.mat4(1.0), glm.vec3(0, 0, math.sin(x + 0.5) * ms)
                )
                idx = (x * y_count) + y
                self.mvp_matrices[idx] = (
                    self.transform_matrix
                    * (self.model_matrices[idx] * movZ)
                    * rotMatrix
                )

    def create_buffers(self):
        self.vertex_buffer = utils.create_buffer_from_ndarray(
            self.device, "VERTEX", vertex_data, wgpu.BufferUsage.VERTEX
        )

        # Setup Uniforms
        matrix_element_count = 4 * 4
        # 4x4 matrix
        matrix_byte_size = sizeof(c_float) * matrix_element_count

        self.uniformBufferSize = matrix_byte_size * num_instances
        # self.uniformBufferSize = self.mvp_matrices.nbytes
        self.uniformBuffer = utils.create_buffer(
            self.device,
            "Uniform buffer",
            self.uniformBufferSize,
            wgpu.BufferUsage.UNIFORM,
        )

    def render(self, view: wgpu.TextureView):
        color_attachments = [
            wgpu.RenderPassColorAttachment(
                view=view,
                load_op=wgpu.LoadOp.CLEAR,
                store_op=wgpu.StoreOp.STORE,
                clear_value=wgpu.Color(0.5, 0.5, 0.5, 1.0),
            )
        ]

        depthStencilAttach = wgpu.RenderPassDepthStencilAttachment(
            view=self.depth_stencil_view,
            depth_load_op=wgpu.LoadOp.CLEAR,
            depth_store_op=wgpu.StoreOp.STORE,
            depth_clear_value=1.0,
        )

        renderpass = wgpu.RenderPassDescriptor(
            label="Main Render Pass",
            color_attachment_count=1,
            color_attachments=color_attachments,
            depth_stencil_attachment=depthStencilAttach,
        )

        encoder: wgpu.CommandEncoder = self.device.create_command_encoder()
        pass_enc: wgpu.RenderPassEncoder = encoder.begin_render_pass(renderpass)
        pass_enc.set_pipeline(self.pipeline)
        pass_enc.set_bind_group(0, self.uniformBindGroup)
        pass_enc.set_vertex_buffer(0, self.vertex_buffer)
        pass_enc.draw(self.kVertexCount)
        pass_enc.end()
        commands = encoder.finish()

        self.queue.submit(1, commands)

    def frame(self):
        self.update_transformation_matrices()

        self.device.queue.write_buffer(
            self.uniformBuffer,
            0,
            self.mvp_matrices
        )

        '''
        self.device.queue.write_buffer(
            self.uniformBuffer,
            0,
            as_capsule(self.mvp_matrices.ptr),
            self.uniformBufferSize,
        )
        '''

        backbufferView: wgpu.TextureView = self.get_surface_view()
        backbufferView.set_label("Back Buffer Texture View")
        self.render(backbufferView)
        self.surface.present()


def main():
    CubesDemo().run()


if __name__ == "__main__":
    main()
