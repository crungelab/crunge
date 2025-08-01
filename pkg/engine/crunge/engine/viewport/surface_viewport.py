import sys

from loguru import logger
import glm

from .viewport import Viewport

from crunge import wgpu
from crunge import skia
from crunge import sdl

from ..render_options import RenderOptions

class SurfaceViewport(Viewport):
    def __init__(
        self,
        size: glm.ivec2,
        window: sdl.Window,
        render_options: RenderOptions = RenderOptions(),
    ):
        super().__init__(size, render_options)
        self.window = window
        self.surface: wgpu.Surface = None
        self.create_surface()

    def on_size(self) -> None:
        super().on_size()
        self.configure_surface()

    def create_surface(self) -> None:
        logger.debug("Creating surface")
        properties = sdl.get_window_properties(self.window)
        if sys.platform == "darwin":
            handle = glfw.get_cocoa_window(self.window)
        elif sys.platform == "win32":
            wsd = wgpu.SurfaceDescriptorFromWindowsHWND()
            handle = glfw.get_win32_window(self.window)
            wsd.hwnd = as_capsule(handle)
            wsd.hinstance = None

        elif sys.platform == "linux":
            handle = sdl.get_number_property(properties, "SDL.window.x11.window", 0)
            display = sdl.get_pointer_property(
                properties, "SDL.window.x11.display", None
            )
            wsd = wgpu.SurfaceSourceXlibWindow(
                display=display,
                window=handle,
            )

        sd = wgpu.SurfaceDescriptor(next_in_chain=wsd)
        self.surface = self.instance.create_surface(sd)
        logger.debug(self.surface)
        self.configure_surface()

    def configure_surface(self) -> None:
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
            #usage=wgpu.TextureUsage.RENDER_ATTACHMENT,
            #usage=wgpu.TextureUsage.RENDER_ATTACHMENT | wgpu.TextureUsage.TEXTURE_BINDING, #Needed for Skia
            usage=wgpu.TextureUsage.RENDER_ATTACHMENT | wgpu.TextureUsage.TEXTURE_BINDING | wgpu.TextureUsage.COPY_SRC,
            present_mode=wgpu.PresentMode.FIFO,
            alpha_mode=wgpu.CompositeAlphaMode.OPAQUE,
        )
        logger.debug(config)
        self.surface.configure(config)
        logger.debug(f"Surface configured to size: {size}")

    def frame(self) -> None:
        surface_texture = wgpu.SurfaceTexture()
        self.surface.get_current_texture(surface_texture)
        self.color_texture = surface_texture.texture
        self.color_texture_view = surface_texture.texture.create_view()

        # Skia
        self.skia_surface = skia.create_surface(self.color_texture, self.recorder)
        self.canvas = self.skia_surface.get_canvas()


    def present(self) -> None:
        self.surface.present()
