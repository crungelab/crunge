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

    def __init__(self, name: str, title: str):
        super().__init__(name, title)

    def _create(self):
        super()._create()
        self.create_device_objects()

    def on_size(self):
        super().on_size()

    def create_device_objects(self):
        super().create_device_objects()
        self.create_pipeline()

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

    def _draw(self):
        renderer = Renderer.get_current()

        with renderer.frame():
            with renderer.render_pass():
                pass_enc = renderer.pass_enc
                pass_enc.set_pipeline(self.pipeline)
                pass_enc.draw(3)

        # Skia rendering

        canvas = renderer.canvas

        paint = skia.Paint()
        paint.set_color(0xFFFFFFFF)
        canvas.draw_rect(skia.Rect(10, 10, 210, 110), paint)

        super()._draw()


def install(app: App):
    app.add_channel(PageChannel(MixedPage, "mixed", "Mixed Skia and WGPU"))
