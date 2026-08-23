from loguru import logger

from crunge import wgpu

from crunge.engine import Viewport
from crunge.engine.math import (
    Rect2i,
)  # ASSUMPTION: same import path as viewport.py uses

from ..demo import Demo, DemoView, DemoOverlay

shader_code = """
@vertex
fn vs_main(@builtin(vertex_index) idx: u32) -> @builtin(position) vec4<f32> {
    var pos = array<vec2<f32>, 3>(
        vec2<f32>(0.0, 0.5), vec2<f32>(-0.5, -0.5), vec2<f32>(0.5, -0.5));
    return vec4<f32>(pos[idx], 0.0, 1.0);
}
@fragment
fn fs_main() -> @location(0) vec4<f32> {
    return vec4<f32>(0.0, 0.502, 1.0, 1.0);
}
"""


class SplitScreenOverlay(DemoOverlay):
    def _create(self):
        super()._create()
        self.shader_module = self.gfx.create_shader_module(shader_code)

        color_targets = [wgpu.ColorTargetState(format=wgpu.TextureFormat.BGRA8_UNORM)]

        fragmentState = wgpu.FragmentState(
            module=self.shader_module,
            entry_point="fs_main",
            targets=color_targets,
        )

        primitive = wgpu.PrimitiveState(topology=wgpu.PrimitiveTopology.TRIANGLE_LIST)

        vertex_state = wgpu.VertexState(
            module=self.shader_module,
            entry_point="vs_main",
        )

        depthStencilState = wgpu.DepthStencilState(
            format=wgpu.TextureFormat.DEPTH24_PLUS,
            depth_write_enabled=False,
        )

        descriptor = wgpu.RenderPipelineDescriptor(
            label="Main Render Pipeline",
            vertex=vertex_state,
            primitive=primitive,
            depth_stencil=depthStencilState,
            fragment=fragmentState,
        )

        self.pipeline = self.device.create_render_pipeline(descriptor)

        # -- split the current viewport in half ------------------------
        parent = Viewport.get_current()
        self.left = parent.add_child(Viewport())
        self.right = parent.add_child(Viewport())

        parent.rect_changed.connect(self.on_parent_rect)
        self.on_parent_rect(parent.global_rect)

    def on_parent_rect(self, rect: Rect2i):
        """Reflow the halves whenever the parent viewport changes."""
        half = rect.width // 2
        self.left.rect = Rect2i(0, 0, half, rect.height)
        self.right.rect = Rect2i(half, 0, rect.width - half, rect.height)

    def _draw(self):
        viewport = Viewport.get_current()
        easel = viewport.easel

        color_attachments = [
            wgpu.RenderPassColorAttachment(
                view=easel.color_texture_view,
                load_op=wgpu.LoadOp.CLEAR,
                store_op=wgpu.StoreOp.STORE,
                clear_value=wgpu.Color(0, 0, 0, 1),
            )
        ]

        depth_stencil_attachment = wgpu.RenderPassDepthStencilAttachment(
            view=easel.depth_stencil_texture_view,
            depth_load_op=wgpu.LoadOp.CLEAR,
            depth_store_op=wgpu.StoreOp.STORE,
            depth_clear_value=0,
        )

        renderpass = wgpu.RenderPassDescriptor(
            label="Main Render Pass",
            color_attachments=color_attachments,
            depth_stencil_attachment=depth_stencil_attachment,
        )

        encoder: wgpu.CommandEncoder = self.device.create_command_encoder()
        pass_enc: wgpu.RenderPassEncoder = encoder.begin_render_pass(renderpass)
        pass_enc.set_pipeline(self.pipeline)

        for vp in (self.left, self.right):
            r = vp.global_rect
            pass_enc.set_viewport(r.x, r.y, r.width, r.height, 0.0, 1.0)
            pass_enc.set_scissor_rect(r.x, r.y, r.width, r.height)
            pass_enc.draw(3)

        pass_enc.end()
        command_buffer = encoder.finish()
        self.queue.submit([command_buffer])

        super()._draw()


def main():
    Demo(DemoView(overlays=[SplitScreenOverlay()])).run()


if __name__ == "__main__":
    main()
