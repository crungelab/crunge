import time
import sys

from loguru import logger
import glm

from crunge import wgpu
from crunge import imgui

from crunge.core import as_capsule
from crunge.engine import Renderer


from ..demo import Demo, DemoView, DemoLayer

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


class TriangleMsaaLayer(DemoLayer):
    def __init__(self):
        super().__init__()

    def create(self, view):
        super().create(view)
        self.shader_module = self.gfx.create_shader_module(shader_code)

        color_targets = [wgpu.ColorTargetState(format=wgpu.TextureFormat.BGRA8_UNORM)]

        fragmentState = wgpu.FragmentState(
            module=self.shader_module,
            entry_point="fs_main",
            target_count=1,
            targets=color_targets,
        )

        primitive = wgpu.PrimitiveState(topology=wgpu.PrimitiveTopology.TRIANGLE_LIST)

        vertex_state = wgpu.VertexState(
            module=self.shader_module,
            entry_point="vs_main",
        )

        depthStencilState = wgpu.DepthStencilState(
            format=wgpu.TextureFormat.DEPTH32_FLOAT,
        )

        multisample = wgpu.MultisampleState(
            count=4,
        )

        descriptor = wgpu.RenderPipelineDescriptor(
            label="Main Render Pipeline",
            vertex=vertex_state,
            primitive=primitive,
            depth_stencil=depthStencilState,
            fragment=fragmentState,
            multisample=multisample,
        )

        self.pipeline = self.device.create_render_pipeline(descriptor)

    def draw(self, renderer: Renderer):
        # logger.debug("draw")
        color_attachments = [
            wgpu.RenderPassColorAttachment(
                view=renderer.msaa_view,
                resolve_target=renderer.texture_view,
                load_op=wgpu.LoadOp.CLEAR,
                store_op=wgpu.StoreOp.STORE,
                clear_value=wgpu.Color(0, 0, 0, 1),
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

        super().draw(renderer)


class TriangleMsaaDemo(Demo):
    def create_device_objects(self):
        super().create_device_objects()
        self.create_depth_stencil_view()
        self.create_msaa_view()

    def create_depth_stencil_view(self):
        descriptor = wgpu.TextureDescriptor(
            usage=wgpu.TextureUsage.RENDER_ATTACHMENT,
            size=wgpu.Extent3D(self.width, self.height, 1),
            format=wgpu.TextureFormat.DEPTH32_FLOAT,
            sample_count=4,
        )
        self.renderer.depth_stencil_view = self.device.create_texture(
            descriptor
        ).create_view()

    def create_msaa_view(self):
        descriptor = wgpu.TextureDescriptor(
            usage=wgpu.TextureUsage.RENDER_ATTACHMENT,
            size=wgpu.Extent3D(self.width, self.height, 1),
            sample_count=4,
            format=wgpu.TextureFormat.BGRA8_UNORM,
            mip_level_count=1,
        )
        self.renderer.msaa_view = self.device.create_texture(
            descriptor
        ).create_view()

    def resize(self, size: glm.ivec2):
        super().resize(size)
        self.create_depth_stencil_view()
        self.create_msaa_view()


def main():
    TriangleMsaaDemo(DemoView(layers=[TriangleMsaaLayer()])).create().run()


if __name__ == "__main__":
    main()
