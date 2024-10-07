from loguru import logger
import glm

from .viewport import Viewport

from crunge import wgpu


class SurfaceViewport(Viewport):
    def __init__(self, width: int, height: int, surface: wgpu.Surface):
        super().__init__(width, height, surface)

    def on_size(self):
        self.configure_surface()

    def configure_surface(self):
        logger.debug("Configuring surface")
        size = self.size
        if not size.x or not size.y:
            return

        logger.debug("Creating surface configuration")
        config = wgpu.SurfaceConfiguration(
            device=self.device,
            width=size.x,
            height=size.y,
            format=wgpu.TextureFormat.BGRA8_UNORM,
            usage=wgpu.TextureUsage.RENDER_ATTACHMENT,
            present_mode=wgpu.PresentMode.FIFO,
            # present_mode=wgpu.PresentMode.MAILBOX,
            view_format_count=0,
            # view_formats=None,
            alpha_mode=wgpu.CompositeAlphaMode.OPAQUE,
        )
        logger.debug(config)
        self.surface.configure(config)
        logger.debug(f"Surface configured to size: {size}")
