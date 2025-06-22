from loguru import logger
import glm

from crunge import wgpu
from crunge import skia
from crunge.engine import Renderer, App
from crunge.demo import PageChannel

from ..page import Page


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


class MixedPage(Page):
    """Mixed demo using Skia and WGPU"""

    depth_stencil_view: wgpu.TextureView = None


    def on_layout(self):
        super().on_layout()
        self.size = glm.vec2(self.window.width, self.window.height)
        logger.debug(f"MixedPage size: {self.size}")
        self.create_device_objects()
    '''
    def _create(self):
        super()._create()
        self.create_device_objects()
    '''

    def on_size(self):
        super().on_size()
        self.create_depth_stencil_view()

    def create_device_objects(self):
        self.create_depth_stencil_view()
        self.create_pipeline()

    def create_depth_stencil_view(self):
        logger.debug("Creating depth stencil view")
        descriptor = wgpu.TextureDescriptor(
            usage=wgpu.TextureUsage.RENDER_ATTACHMENT,
            size=wgpu.Extent3D(self.size.x, self.size.y, 1),
            format=wgpu.TextureFormat.DEPTH32_FLOAT,
        )
        self.depth_stencil_view = self.device.create_texture(descriptor).create_view()

    def create_pipeline(self):
        logger.debug("Creating pipeline")

        logger.debug("Creating shader module")
        shader_module = self.gfx.create_shader_module(shader_code)

        logger.debug("Creating colorTargetState")

        colorTargetStates = [
            wgpu.ColorTargetState(format=wgpu.TextureFormat.BGRA8_UNORM)
        ]

        logger.debug("Creating fragmentState")
        fragmentState = wgpu.FragmentState(
            module=shader_module,
            entry_point="fs_main",
            targets=colorTargetStates,
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
            fragment=fragmentState,
        )
        logger.debug(descriptor)

        logger.debug("Creating render pipeline")
        self.pipeline = self.device.create_render_pipeline(descriptor)
        logger.debug(self.pipeline)

    def draw(self, renderer: Renderer):
        color_attachments = [
            wgpu.RenderPassColorAttachment(
                view=renderer.viewport.color_texture.create_view(),
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
        pass_enc.draw(3)
        pass_enc.end()
        commands = encoder.finish()

        self.queue.submit([commands])

        # Skia rendering

        with renderer.canvas_target() as canvas:
            paint = skia.Paint()
            paint.set_color(0xFFFFFFFF)
            canvas.draw_rect(skia.Rect(10, 10, 210, 110), paint)

        super().draw(renderer)


def install(app: App):
    app.add_channel(PageChannel(MixedPage, "mixed", "Mixed Skia and WGPU"))
