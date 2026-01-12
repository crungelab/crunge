import sys

from loguru import logger
import glm

from .viewport import Viewport

from crunge import wgpu
from crunge import skia
from crunge import sdl

from ..render_options import RenderOptions


class OffscreenViewport(Viewport):
    def __init__(
        self,
        size: glm.ivec2,
        render_options: RenderOptions = RenderOptions(),
    ):
        super().__init__(size, render_options)
        self.create_texture()

    def on_size(self) -> None:
        super().on_size()
        self.create_texture()

    def create_texture(self) -> None:
        logger.debug("Creating offscreen texture")
        self.color_texture = self.gfx.create_texture(
            "offscreen_color_texture",
            self.size.x,
            self.size.y,
            wgpu.TextureFormat.BGRA8_UNORM,
            wgpu.TextureUsage.RENDER_ATTACHMENT | wgpu.TextureUsage.TEXTURE_BINDING,
        )
        self.color_texture_view = self.color_texture.create_view()

    def begin_frame(self) -> None:
        # Skia
        self.skia_surface = skia.create_surface(self.color_texture, self.recorder)
        self.canvas = self.skia_surface.get_canvas()

    def end_frame(self) -> None:
        pass
