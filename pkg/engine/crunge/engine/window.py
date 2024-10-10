from loguru import logger
import glm


from crunge import sdl

from .frame import Frame
from .viewport import SurfaceViewport
from .renderer import Renderer
from . import globals


class Window(Frame):
    def __init__(self, size=glm.ivec2(), title="", view=None, resizable=False):
        super().__init__(size, view=view)
        self.name = title

        self.window: sdl.Window = None
        self.viewport: SurfaceViewport = None
        self.renderer: Renderer = None

        globals.set_current_window(self)

    def _create(self):
        logger.debug("Window.create")
        self.create_window()
        self.create_device_objects()
        self.create_viewport()
        self.create_renderer()
        return super()._create()

    def create_window(self):
        self.window = sdl.create_window(
            self.name, self.width, self.height, sdl.WindowFlags.RESIZABLE
        )

    def create_renderer(self):
        self.renderer = Renderer(self.viewport)

    def on_size(self):
        super().on_size()
        size = self.size
        logger.debug(f"Resizing to {size}")
        if not size.x or not size.y:
            return
        self.viewport.size = size
        logger.debug(f"Resized to {size}")

    def get_size(self):
        return sdl.get_window_size(self.window)

    def get_framebuffer_size(self):
        return sdl.get_window_size_in_pixels(self.window)

    def create_device_objects(self):
        pass

    def create_viewport(self):
        #self.viewport = SurfaceViewport(self.width, self.height, self.window)
        self.viewport = SurfaceViewport(self.width, self.height, self.window, use_depth_stencil=True)

    def frame(self):
        self.viewport.frame()
        self.renderer.viewport = self.viewport

        self.pre_draw(self.renderer)
        self.draw(self.renderer)
        self.post_draw(self.renderer)

        self.viewport.present()

    def on_window(self, event: sdl.WindowEvent):
        #logger.debug("window event")
        match event.type:
            case sdl.EventType.WINDOW_RESIZED:
                self.size = glm.ivec2(event.data1, event.data2)
            case _:
                # pass
                return super().on_window(event)
