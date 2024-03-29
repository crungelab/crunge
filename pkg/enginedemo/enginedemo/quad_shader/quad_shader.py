import time
import sys

from loguru import logger

from crunge import wgpu, imgui
from crunge import as_capsule
from crunge.engine import Renderer

from ..demo import Demo, DemoView, DemoLayer

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

'''
shader_code = """
@vertex
fn vs_main(@builtin(vertex_index) idx: u32) -> @builtin(position) vec4<f32> {
    var positions = array<vec2<f32>, 4>(
        vec2<f32>(-0.5, 0.5),  // top left
        vec2<f32>(-0.5, -0.5), // bottom left
        vec2<f32>(0.5, 0.5),   // top right
        vec2<f32>(0.5, -0.5)   // bottom right
    );
    return vec4<f32>(positions[idx], 0.0, 1.0);
}
@fragment
fn fs_main() -> @location(0) vec4<f32> {
    return vec4<f32>(0.0, 0.502, 1.0, 1.0); // 0x80/0xff ~= 0.502
}
"""
'''

class QuadShaderLayer(DemoLayer):
    def __init__(self):
        super().__init__()

    def create(self, view):
        super().create(view)
        shader_module = self.gfx.create_shader_module(shader_code)

        colorTargetState = wgpu.ColorTargetState(format=wgpu.TextureFormat.BGRA8_UNORM)

        fragmentState = wgpu.FragmentState(
            module=shader_module,
            entry_point="fs_main",
            target_count=1,
            targets=colorTargetState,
        )

        depthStencilState = wgpu.DepthStencilState(
            format=wgpu.TextureFormat.DEPTH32_FLOAT,
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

    def draw(self, renderer: Renderer):
        #logger.debug("render")
        attachment = wgpu.RenderPassColorAttachment(
            view=renderer.texture_view,
            load_op=wgpu.LoadOp.CLEAR,
            store_op=wgpu.StoreOp.STORE,
            clear_value=wgpu.Color(0, 0, 0, 1),
        )

        depth_stencil_attachment = wgpu.RenderPassDepthStencilAttachment(
            view=renderer.depth_stencil_view,
            depth_load_op=wgpu.LoadOp.CLEAR,
            depth_store_op=wgpu.StoreOp.STORE,
            depth_clear_value=0,
        )

        renderpass = wgpu.RenderPassDescriptor(
            label="Main Render Pass",
            color_attachment_count=1,
            color_attachments=attachment,
            depth_stencil_attachment=depth_stencil_attachment,
        )

        encoder: wgpu.CommandEncoder = self.device.create_command_encoder()
        pass_enc: wgpu.RenderPassEncoder = encoder.begin_render_pass(renderpass)
        pass_enc.set_pipeline(self.pipeline)
        pass_enc.draw(4)
        pass_enc.end()
        commands = encoder.finish()

        self.queue.submit(1, commands)

        super().draw(renderer)


class QuadShaderDemo(Demo):
    def create_device_objects(self):
        super().create_device_objects()
        self.create_depth_stencil_view()

    def create_depth_stencil_view(self):
        descriptor = wgpu.TextureDescriptor(
            usage=wgpu.TextureUsage.RENDER_ATTACHMENT,
            size=wgpu.Extent3D(self.width, self.height, 1),
            format=wgpu.TextureFormat.DEPTH32_FLOAT,
        )
        self.renderer.depth_stencil_view = self.device.create_texture(descriptor).create_view()


def main():
    QuadShaderDemo(DemoView(layers=[QuadShaderLayer()])).create().run()


if __name__ == "__main__":
    main()
