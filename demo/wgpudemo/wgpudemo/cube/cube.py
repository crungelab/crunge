from ctypes import c_float, sizeof
import time
import math
import glm

from loguru import logger

from crunge.core import as_capsule
from crunge import wgpu
import crunge.wgpu.utils as utils

from ..common import Demo, Renderer

from .data import vertex_data


WORLD_AXIS_X = glm.vec3(1.0, 0.0, 0.0)
WORLD_AXIS_Y = glm.vec3(0.0, 1.0, 0.0)
WORLD_AXIS_Z = glm.vec3(0.0, 0.0, 1.0)

shader_code = """
struct Uniforms {
  modelViewProjectionMatrix : mat4x4<f32>,
}
@binding(0) @group(0) var<uniform> uniforms : Uniforms;

struct VertexInput {
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
  let vert_pos = uniforms.modelViewProjectionMatrix * in.pos;
  let frag_colour = 0.5 * (in.pos + vec4(1));
  return VertexOutput(vert_pos, in.uv, frag_colour);
}

@fragment
fn fs_main(in : VertexOutput) -> @location(0) vec4<f32> {
  return in.frag_colour;
}
"""


class CubeDemo(Demo):
    vertex_buffer: wgpu.Buffer = None
    kVertexCount = 36
    kPositionByteOffset = 0
    kUVByteOffset = 4 * sizeof(c_float)
    kCubeDataStride = 6

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

        logger.debug(vertBufferLayouts[0].array_stride)
        logger.debug(vertBufferLayouts[0].attribute_count)
        logger.debug(vertBufferLayouts[0].step_mode)

        colorTargetStates = [
            wgpu.ColorTargetState(format=wgpu.TextureFormat.BGRA8_UNORM)
        ]

        fragmentState = wgpu.FragmentState(
            module=shader_module,
            entry_point="fs_main",
            target_count=1,
            targets=colorTargetStates,
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
        logger.debug(descriptor)

        self.pipeline = self.device.create_render_pipeline(descriptor)

        logger.debug(self.pipeline)

        bind_group_entries = [
            wgpu.BindGroupEntry(
                binding=0,
                # TODO: deprecated?
                # resource=wgpu.BindingResource.buffer(self.uniformBuffer),
                buffer=self.uniformBuffer,
            )
        ]

        bindGroupDesc = wgpu.BindGroupDescriptor(
            label="Uniform bind group",
            layout=self.pipeline.get_bind_group_layout(0),
            entry_count=1,
            entries=bind_group_entries,
        )

        self.uniformBindGroup = self.device.create_bind_group(bindGroupDesc)

        aspect = float(self.kWidth) / float(self.kHeight)
        fov_y_radians = (2.0 * math.pi) / 5.0
        self.projectionMatrix = glm.perspective(fov_y_radians, aspect, 1.0, 100.0)

    @property
    def transform_matrix(self):
        now = time.time()
        ms = round(now * 1000) / 1000
        viewMatrix = glm.translate(glm.mat4(1.0), glm.vec3(0, 0, -4))
        rotMatrix = glm.rotate(glm.mat4(1.0), math.sin(ms), WORLD_AXIS_X)
        rotMatrix = glm.rotate(rotMatrix, math.cos(ms), WORLD_AXIS_Y)
        return self.projectionMatrix * viewMatrix * rotMatrix

    def create_buffers(self):
        self.vertex_buffer = utils.create_buffer_from_ndarray(
            self.device, "VERTEX", vertex_data, wgpu.BufferUsage.VERTEX
        )
        self.uniformBufferSize = 4 * 16
        self.uniformBuffer = utils.create_buffer(
            self.device,
            "Uniform buffer",
            self.uniformBufferSize,
            wgpu.BufferUsage.UNIFORM,
        )

    def render(self, renderer: Renderer):
        color_attachments = [
            wgpu.RenderPassColorAttachment(
                view=renderer.view,
                load_op=wgpu.LoadOp.CLEAR,
                store_op=wgpu.StoreOp.STORE,
                clear_color=wgpu.Color(0.5, 0.5, 0.5, 1.0),
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
        transform = self.transform_matrix
        self.device.queue.write_buffer(
            self.uniformBuffer,
            0,
            transform,
        )
        super().frame()

    '''
    def frame(self):
        transform = self.transform_matrix
        self.device.queue.write_buffer(
            self.uniformBuffer,
            0,
            as_capsule(glm.value_ptr(transform)),
            self.uniformBufferSize,
        )
        super().frame()
    '''

def main():
    CubeDemo().run()


if __name__ == "__main__":
    main()
