import time
import sys

from loguru import logger
import glfw
import glm

from crunge import wgpu
from crunge import skia

from ..common import Demo, Renderer

shader_code = """
@vertex
fn vs_main(@builtin(vertex_index) idx: u32) -> @builtin(position) vec4<f32> {
    var pos = array<vec2<f32>, 3>(
        vec2<f32>(0.0, 0.5), vec2<f32>(-0.5, -0.5), vec2<f32>(0.5, -0.5));
    return vec4<f32>(pos[idx], 0.0, 1.0);
}
@fragment
fn fs_main() -> @location(0) vec4<f32> {
    return vec4<f32>(0.0, 0.502, 1.0, 1.0); // 0x80/0xff ~= 0.502
}
"""


class MixedDemo(Demo):
    """Mixed demo using Skia and WGPU"""

    depth_stencil_view: wgpu.TextureView = None

    def resize(self, size: glm.ivec2):
        super().resize(size)
        self.create_depth_stencil_view()

    def create_device_objects(self):
        self.create_depth_stencil_view()
        self.create_pipeline()

    def create_depth_stencil_view(self):
        descriptor = wgpu.TextureDescriptor(
            usage=wgpu.TextureUsage.RENDER_ATTACHMENT,
            size=wgpu.Extent3D(self.size.x, self.size.y, 1),
            format=wgpu.TextureFormat.DEPTH32_FLOAT,
        )
        self.depth_stencil_view = self.device.create_texture(descriptor).create_view()

    def create_pipeline(self):
        logger.debug("Creating pipeline")

        logger.debug("Creating shader module")
        shader_module = self.create_shader_module(shader_code)

        logger.debug("Creating colorTargetState")

        colorTargetStates = [
            wgpu.ColorTargetState(format=wgpu.TextureFormat.BGRA8_UNORM)
        ]

        logger.debug("Creating fragmentState")
        fragmentState = wgpu.FragmentState(
            module=shader_module,
            entry_point="fs_main",
            target_count=1,
            targets=colorTargetStates,
        )

        logger.debug("Creating depthStencilState")
        depthStencilState = wgpu.DepthStencilState(
            format=wgpu.TextureFormat.DEPTH32_FLOAT,
            depth_write_enabled=False,
        )

        logger.debug("Creating primitive")
        primitive = wgpu.PrimitiveState(topology=wgpu.PrimitiveTopology.TRIANGLE_LIST)

        logger.debug("Creating vertex_state")
        vertex_state = wgpu.VertexState(
            module=shader_module,
            entry_point="vs_main",
        )

        logger.debug("Creating render pipeline descriptor")
        descriptor = wgpu.RenderPipelineDescriptor(
            label="Main Render Pipeline",
            vertex=vertex_state,
            primitive=primitive,
            depth_stencil=depthStencilState,
            fragment=fragmentState,
        )
        logger.debug(descriptor)

        logger.debug("Creating render pipeline")
        self.pipeline = self.device.create_render_pipeline(descriptor)
        logger.debug(self.pipeline)

    def render(self, renderer: Renderer):
        color_attachments = [
            wgpu.RenderPassColorAttachment(
                view=renderer.view,
                load_op=wgpu.LoadOp.CLEAR,
                store_op=wgpu.StoreOp.STORE,
                clear_color=wgpu.Color(0, 0, 0, 1),
            )
        ]

        depth_stencil_attachment = wgpu.RenderPassDepthStencilAttachment(
            view=renderer.depth_stencil_view,
            depth_load_op=wgpu.LoadOp.CLEAR,
            depth_store_op=wgpu.StoreOp.STORE,
            depth_clear_value=0,
        )

        renderpass = wgpu.RenderPassDescriptor(
            label="Main Render Pass",
            color_attachment_count=1,
            color_attachments=color_attachments,
            depth_stencil_attachment=depth_stencil_attachment,
        )

        encoder: wgpu.CommandEncoder = self.device.create_command_encoder()
        pass_enc: wgpu.RenderPassEncoder = encoder.begin_render_pass(renderpass)
        pass_enc.set_pipeline(self.pipeline)
        pass_enc.draw(3)
        pass_enc.end()
        commands = encoder.finish()

        self.queue.submit(1, commands)

        # Skia rendering

        with self.canvas_target() as canvas:
            paint = skia.Paint()
            paint.set_color(0xFFFFFFFF)
            canvas.draw_rect(skia.Rect(10, 10, 210, 110), paint)


def main():
    MixedDemo().run()


if __name__ == "__main__":
    main()
