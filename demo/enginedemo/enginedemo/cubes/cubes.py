from ctypes import Structure, c_float, c_uint32, sizeof, c_bool, c_int, c_void_p
import time
import math
import glm

from loguru import logger

from crunge import wgpu
import crunge.wgpu.utils as utils
from crunge.engine import Renderer

from ..demo import Demo

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

# logger.debug(shader_code)
# exit()


class CubesDemo(Demo):
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

        step = 4.0
        half_x = (x_count / 2) + 0.5
        half_y = (y_count / 2) + 0.5

        for x in range(x_count):
            for y in range(y_count):
                self.model_matrices[(x * y_count) + y] = glm.translate(
                    glm.mat4(1), glm.vec3(step * (x - half_x), step * (y - half_y), 0)
                )

    def create_device_objects(self):
        self.create_buffers()
        self.create_pipeline()

    def on_size(self):
        super().on_size()
        self.resize_camera(self.size)

    def resize_camera(self, size: glm.ivec2):
        aspect = float(size.x) / float(size.y)
        fov_y_radians = (2.0 * math.pi) / 5.0
        # fov_y_radians = glm.radians(60.0)
        self.projectionMatrix = glm.perspective(fov_y_radians, aspect, 1.0, 100.0)

    def create_pipeline(self):
        shader_module = self.gfx.create_shader_module(shader_code)

        # Pipeline creation

        vertAttributes = wgpu.VertexAttributes(
            [
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
        )

        vb_layouts = [
            wgpu.VertexBufferLayout(
                array_stride=self.kCubeDataStride * sizeof(c_float),
                attributes=vertAttributes,
            )
        ]

        color_targets = [wgpu.ColorTargetState(format=wgpu.TextureFormat.BGRA8_UNORM)]

        fragmentState = wgpu.FragmentState(
            module=shader_module,
            entry_point="fs_main",
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
            buffers=vb_layouts,
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
            entries=bg_entries,
        )

        self.uniformBindGroup = self.device.create_bind_group(bindGroupDesc)

    @property
    def transform_matrix(self):
        viewMatrix = glm.translate(glm.mat4(1.0), glm.vec3(0, 3, -92))
        viewMatrix = glm.scale(
            viewMatrix, glm.vec3(WORLD_SCALE, WORLD_SCALE, WORLD_SCALE)
        )
        return self.projectionMatrix * viewMatrix

    def update_transformation_matrices(self):
        now = time.time()
        ms = round(now * 1000) / 1000
        for x in range(x_count):
            for y in range(y_count):
                rotMatrix = glm.rotate(
                    glm.mat4(1.0),
                    math.sin(ms),
                    glm.vec3(0, 1, 0),
                )
                movZ = glm.translate(
                    glm.mat4(1.0), glm.vec3(0, 0, math.sin(x + 0.5) * ms)
                )
                idx = (x * y_count) + y
                self.mvp_matrices[idx] = (
                    self.transform_matrix * self.model_matrices[idx] * rotMatrix
                )

    def create_buffers(self):
        self.vertex_buffer = utils.create_buffer_from_ndarray(
            self.device, "VERTEX", vertex_data, wgpu.BufferUsage.VERTEX
        )

        # Setup Uniforms
        """
        matrix_element_count = 4 * 4
        # 4x4 matrix
        matrix_byte_size = sizeof(c_float) * matrix_element_count
        self.uniformBufferSize = matrix_byte_size * num_instances
        """
        self.uniformBufferSize = self.mvp_matrices.nbytes
        self.uniformBuffer = utils.create_buffer(
            self.device,
            "Uniform buffer",
            self.uniformBufferSize,
            wgpu.BufferUsage.UNIFORM,
        )

    def draw(self, renderer: Renderer):
        color_attachments = [
            wgpu.RenderPassColorAttachment(
                view=renderer.viewport.color_texture_view,
                load_op=wgpu.LoadOp.CLEAR,
                store_op=wgpu.StoreOp.STORE,
                clear_value=wgpu.Color(0.5, 0.5, 0.5, 1.0),
                # clear_value=wgpu.Color(0.0, 0.0, 0.0, 1.0),
            )
        ]

        depthStencilAttach = wgpu.RenderPassDepthStencilAttachment(
            view=renderer.viewport.depth_stencil_texture_view,
            depth_load_op=wgpu.LoadOp.CLEAR,
            depth_store_op=wgpu.StoreOp.STORE,
            depth_clear_value=1.0,
        )

        renderpass = wgpu.RenderPassDescriptor(
            label="Main Render Pass",
            color_attachments=color_attachments,
            depth_stencil_attachment=depthStencilAttach,
        )

        encoder: wgpu.CommandEncoder = self.device.create_command_encoder()
        pass_enc: wgpu.RenderPassEncoder = encoder.begin_render_pass(renderpass)
        pass_enc.set_pipeline(self.pipeline)
        pass_enc.set_bind_group(0, self.uniformBindGroup)
        pass_enc.set_vertex_buffer(0, self.vertex_buffer)
        pass_enc.draw(self.kVertexCount, num_instances)
        pass_enc.end()
        command_buffer = encoder.finish()

        self.queue.submit([command_buffer])

        super().draw(renderer)

    def frame(self):
        self.update_transformation_matrices()
        self.device.queue.write_buffer(self.uniformBuffer, 0, self.mvp_matrices)
        super().frame()


def main():
    CubesDemo().create().run()


if __name__ == "__main__":
    main()
