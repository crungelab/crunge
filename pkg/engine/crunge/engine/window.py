import sys, time
from loguru import logger
import glm


from crunge.core import as_capsule
from crunge import sdl
from crunge import wgpu
from crunge.wgpu import utils

from .frame import Frame
from .renderer import Renderer
from . import globals


class Window(Frame):
    def __init__(self, size=glm.ivec2(), title="", view=None, resizable=False):
        super().__init__(size, view=view)
        self.name = title

        self.window: sdl.Window = None

        self.surface: wgpu.Surface = None
        self.renderer: Renderer = None

        globals.set_current_window(self)

    def create(self):
        logger.debug("Window.create")
        self.create_window()
        self.create_renderer()
        self.create_device_objects()
        self.create_surface()
        return super().create()

    def create_window(self):
        self.window = sdl.create_window(
            self.name, self.width, self.height, sdl.WindowFlags.RESIZABLE
        )

    def create_renderer(self):
        self.renderer = Renderer()

    def resize(self, size: glm.ivec2):
        # super().resize(size)
        logger.debug(f"Resizing to {size}")
        if not size.x or not size.y:
            return
        if self.size == size:
            return
        self.size = size
        self.configure_surface(size)
        super().resize(size)
        logger.debug(f"Resized to {size}")

    def get_size(self):
        return sdl.get_window_size(self.window)

    def get_framebuffer_size(self):
        return sdl.get_window_size_in_pixels(self.window)

    def create_device_objects(self):
        pass

    def configure_surface(self, size: glm.ivec2):
        logger.debug("Configuring surface")

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

    def create_surface(self):
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
            wsd = wgpu.SurfaceDescriptorFromXlibWindow()
            handle = sdl.get_number_property(properties, "SDL.window.x11.window", 0)
            display = sdl.get_pointer_property(
                properties, "SDL.window.x11.display", None
            )
            wsd.window = handle
            wsd.display = display

        sd = wgpu.SurfaceDescriptor(next_in_chain=wsd)
        self.surface = self.instance.create_surface(sd)
        logger.debug(self.surface)
        self.configure_surface(self.size)

    def get_surface_view(self) -> wgpu.TextureView:
        surface_texture = wgpu.SurfaceTexture()
        self.surface.get_current_texture(surface_texture)
        surface_view: wgpu.TextureView = surface_texture.texture.create_view()
        return surface_view

    def frame(self):
        self.renderer.texture_view = self.get_surface_view()

        self.pre_draw(self.renderer)
        self.draw(self.renderer)
        self.post_draw(self.renderer)

        self.surface.present()

    def on_window(self, event: sdl.WindowEvent):
        #logger.debug("window event")
        match event.type:
            case sdl.EventType.WINDOW_RESIZED:
                self.resize(glm.ivec2(event.data1, event.data2))
            case _:
                # pass
                return super().on_window(event)
