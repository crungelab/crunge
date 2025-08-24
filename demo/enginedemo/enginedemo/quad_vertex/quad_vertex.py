from ctypes import c_float, sizeof

from loguru import logger

from crunge import wgpu
import crunge.wgpu.utils as utils
from crunge.engine import Viewport

from ..demo import Demo

from .data import vertex_data

shader_code = """
struct VertexInput {
  @location(0) pos: vec4<f32>,
  @location(1) color: vec4<f32>,
}

struct VertexOutput {
  @builtin(position) pos: vec4<f32>,
  @location(0) color: vec4<f32>,
}

@vertex
fn vs_main(in : VertexInput) -> VertexOutput {
  return VertexOutput(in.pos, in.color);
}

@fragment
fn fs_main(in : VertexOutput) -> @location(0) vec4<f32> {
  return in.color;
}
"""


class QuadVertexDemo(Demo):
    vertex_buffer: wgpu.Buffer = None

    kWidth = 1024
    kHeight = 768

    def create_device_objects(self):
        self.create_buffers()
        self.create_pipeline()

    def create_buffers(self):
        self.vertex_buffer = utils.create_buffer_from_ndarray(
            self.device, "VERTEX", vertex_data, wgpu.BufferUsage.VERTEX
        )

    def create_pipeline(self):
        shader_module = self.gfx.create_shader_module(shader_code)

        # Pipeline creation

        vertAttributes = [
            wgpu.VertexAttribute(
                format=wgpu.VertexFormat.FLOAT32X2, offset=0, shader_location=0
            ),
            wgpu.VertexAttribute(
                format=wgpu.VertexFormat.FLOAT32X3,
                offset=2 * sizeof(c_float),
                shader_location=1,
            ),
        ]

        vb_layouts = [
            wgpu.VertexBufferLayout(
                array_stride=5 * sizeof(c_float),
                attributes=vertAttributes,
            )
        ]

        color_targets = [wgpu.ColorTargetState(format=wgpu.TextureFormat.BGRA8_UNORM)]

        fragmentState = wgpu.FragmentState(
            module=shader_module,
            entry_point="fs_main",
            targets=color_targets,
        )

        vertex_state = wgpu.VertexState(
            module=shader_module,
            entry_point="vs_main",
            buffers=vb_layouts,
        )
        descriptor = wgpu.RenderPipelineDescriptor(
            label="Main Render Pipeline", vertex=vertex_state, fragment=fragmentState
        )

        self.pipeline = self.device.create_render_pipeline(descriptor)

    def _draw(self):
        viewport = Viewport.get_current()

        color_attachments = [
            wgpu.RenderPassColorAttachment(
                view=viewport.color_texture_view,
                load_op=wgpu.LoadOp.CLEAR,
                store_op=wgpu.StoreOp.STORE,
                clear_value=wgpu.Color(0, 0, 0, 1),
            )
        ]

        renderpass = wgpu.RenderPassDescriptor(
            label="Main Render Pass",
            color_attachments=color_attachments,
        )

        encoder: wgpu.CommandEncoder = self.device.create_command_encoder()
        pass_enc: wgpu.RenderPassEncoder = encoder.begin_render_pass(renderpass)
        pass_enc.set_pipeline(self.pipeline)
        pass_enc.set_vertex_buffer(0, self.vertex_buffer)
        pass_enc.draw(6)
        pass_enc.end()
        command_buffer = encoder.finish()

        self.queue.submit([command_buffer])

        super()._draw()


def main():
    QuadVertexDemo().run()


if __name__ == "__main__":
    main()
