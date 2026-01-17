from loguru import logger

from crunge import wgpu
from crunge.engine import Viewport

from ..demo import Demo, DemoView, DemoOverlay

shader_code = """
@vertex
fn vs_main(@builtin(vertex_index) idx: u32) -> @builtin(position) vec4<f32> {
    let x = f32((idx & 1u) << 1) - 1.0; // Generates 0 or 1, then maps to -1 or 1
    let y = f32((idx & 2u) >> 1) * 2.0 - 1.0; // Generates 0 or 1, then maps to -1 or 1
    return vec4<f32>(x * 0.5, y * 0.5, 0.0, 1.0); //Scale by 0.5 to make the quad half the size
}
@fragment
fn fs_main() -> @location(0) vec4<f32> {
    return vec4<f32>(0.0, 0.502, 1.0, 1.0); // 0x80/0xff ~= 0.502
}
"""


class QuadShaderLayer(DemoOverlay):
    def _create(self):
        super()._create()
        shader_module = self.gfx.create_shader_module(shader_code)

        color_targets = [wgpu.ColorTargetState(format=wgpu.TextureFormat.BGRA8_UNORM)]

        fragmentState = wgpu.FragmentState(
            module=shader_module,
            entry_point="fs_main",
            targets=color_targets,
        )

        depthStencilState = wgpu.DepthStencilState(
            format=wgpu.TextureFormat.DEPTH24_PLUS,
            depth_write_enabled=False,
        )

        primitive = wgpu.PrimitiveState(topology=wgpu.PrimitiveTopology.TRIANGLE_STRIP)

        vertex_state = wgpu.VertexState(
            module=shader_module,
            entry_point="vs_main",
        )

        descriptor = wgpu.RenderPipelineDescriptor(
            label="Main Render Pipeline",
            vertex=vertex_state,
            primitive=primitive,
            depth_stencil=depthStencilState,
            fragment=fragmentState,
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

        depth_stencil_attachment = wgpu.RenderPassDepthStencilAttachment(
            view=viewport.depth_stencil_texture_view,
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
        pass_enc.draw(4)
        pass_enc.end()
        command_buffer = encoder.finish()

        self.queue.submit([command_buffer])

        super()._draw()


class QuadShaderDemo(Demo):
    pass


def main():
    QuadShaderDemo(DemoView(overlays=[QuadShaderLayer()])).run()


if __name__ == "__main__":
    main()
