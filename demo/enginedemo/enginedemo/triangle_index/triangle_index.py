import ctypes
from ctypes import Structure, c_float, c_uint32, sizeof, c_bool, c_int, c_void_p
import time
import sys

from loguru import logger
import numpy as np

from crunge.core import as_capsule
from crunge import wgpu
import crunge.wgpu.utils as utils
from crunge.engine import Renderer

from ..demo import Demo

index_data = np.array([0, 1, 2], dtype=np.uint32)

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


class TriangleIndexDemo(Demo):
    vertex_buffer: wgpu.Buffer = None
    index_buffer: wgpu.Buffer = None

    kWidth = 1024
    kHeight = 768

    def __init__(self):
        super().__init__()

    def create_device_objects(self):
        self.create_buffers()
        self.create_pipeline()

    def create_pipeline(self):
        shader_module = self.gfx.create_shader_module(shader_code)

        # Pipeline creation

        vertAttributes = wgpu.VertexAttributes(
            [
                wgpu.VertexAttribute(
                    format=wgpu.VertexFormat.FLOAT32X4, offset=0, shader_location=0
                ),
                wgpu.VertexAttribute(
                    format=wgpu.VertexFormat.FLOAT32X4,
                    offset=4 * sizeof(c_float),
                    shader_location=1,
                ),
            ]
        )

        vb_layouts = [
            wgpu.VertexBufferLayout(
                array_stride=8 * sizeof(c_float),
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

        vertex_state = wgpu.VertexState(
            module=shader_module,
            entry_point="vs_main",
            buffer_count=1,
            buffers=vb_layouts,
        )
        descriptor = wgpu.RenderPipelineDescriptor(
            label="Main Render Pipeline", vertex=vertex_state, fragment=fragmentState
        )

        self.pipeline = self.device.create_render_pipeline(descriptor)

    def create_buffers(self):
        self.vertex_buffer = utils.create_buffer_from_ndarray(
            self.device, "VERTEX", vertex_data, wgpu.BufferUsage.VERTEX
        )
        self.index_buffer = utils.create_buffer_from_ndarray(
            self.device, "INDEX", index_data, wgpu.BufferUsage.INDEX
        )

    def draw(self, renderer: Renderer):
        color_attachments = [
            wgpu.RenderPassColorAttachment(
                #view=renderer.texture_view,
                view = renderer.viewport.color_texture_view,
                load_op=wgpu.LoadOp.CLEAR,
                store_op=wgpu.StoreOp.STORE,
                clear_value=wgpu.Color(0, 0, 0, 1),
            )
        ]

        renderpass = wgpu.RenderPassDescriptor(
            label="Main Render Pass",
            color_attachment_count=1,
            color_attachments=color_attachments,
        )

        encoder: wgpu.CommandEncoder = self.device.create_command_encoder()
        pass_enc: wgpu.RenderPassEncoder = encoder.begin_render_pass(renderpass)
        pass_enc.set_pipeline(self.pipeline)
        pass_enc.set_vertex_buffer(0, self.vertex_buffer)
        pass_enc.set_index_buffer(self.index_buffer, wgpu.IndexFormat.UINT32)
        pass_enc.draw_indexed(3)
        pass_enc.end()
        commands = encoder.finish()

        self.queue.submit(1, commands)

        super().draw(renderer)


def main():
    TriangleIndexDemo().create().run()


if __name__ == "__main__":
    main()
