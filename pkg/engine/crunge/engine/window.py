from typing import Optional
import math

import contextlib
from contextvars import ContextVar

from loguru import logger
import glm

from crunge import sdl
from crunge import yoga

from . import globals, SurfaceEasel, Viewport, Renderer, RenderOptions, compose
from .math import Rect2i
from .signal import Signal, Pulse
from .scheduler import Scheduler
from .frame import Frame

DEFAULT_WIDTH = 1280
DEFAULT_HEIGHT = 720

current_window: ContextVar[Optional["Window"]] = ContextVar(
    "current_window", default=None
)


class Window(Frame):
    def __init__(
        self,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
        title="",
        display=None,
        resizable=False,
    ):
        style = yoga.StyleBuilder().size(width, height).build()
        super().__init__(style, display=display)
        globals.set_current_window(self)
        self.name = title

        self.sdl_window: sdl.Window = None
        # self.render_options = RenderOptions(use_depth_stencil=True, use_msaa=True, use_snapshot=True)
        self.render_options = RenderOptions(use_depth_stencil=True, use_snapshot=True)
        self.viewport: Viewport = None
        self.easel: SurfaceEasel = None
        self.renderer: Renderer = None

        self.update_time: float = 0.0
        self.render_time: float = 0.0
        self.frame_time: float = 0.0

        self.resize_pending = False
        self.window_size: Signal[glm.ivec2] = Signal()
        self.pre_frame: Pulse = Pulse()
        self.post_frame: Pulse = Pulse()

    def on_display(self):
        super().on_display()
        gui = self.display.gui

    def make_current(self) -> Optional["Window"]:
        super().make_current()
        return current_window.set(self)

    @classmethod
    def get_current(cls) -> Optional["Window"]:
        return current_window.get()

    @contextlib.contextmanager
    def use(self):
        token = self.make_current()
        try:
            yield self
        finally:
            current_window.reset(token)

    def _create(self):
        logger.debug("Window.create")
        self.layout.calculate_bounds(math.nan, math.nan, yoga.Direction.LTR)
        logger.debug(f"Window.size: {self.size}")
        self.create_window()
        self.create_viewport()
        self.create_device_objects()
        self.create_renderer()
        super()._create()

    def create_window(self):
        self.sdl_window = sdl.create_window(
            self.name, self.width, self.height, sdl.WindowFlags.RESIZABLE
        )

    def create_renderer(self):
        self.renderer = Renderer(self.viewport)

    def _enable(self):
        self.viewport.make_current()
        super()._enable()

    def on_size(self):
        super().on_size()
        size = self.size
        if not size.x or not size.y:
            return

        self.easel.size = glm.ivec2(self.get_framebuffer_size())

        logger.debug(f"Window size: {size}")
        logger.debug(f"Framebuffer size: {self.easel.size}")

        self.resize_pending = True

    """
    def on_resize(self):
        self.viewport.size = glm.ivec2(self.get_framebuffer_size())
        self.resize_pending = False
    """

    def get_window_size(self):
        return sdl.get_window_size(self.sdl_window)

    def get_framebuffer_size(self):
        return sdl.get_window_size_in_pixels(self.sdl_window)

    def create_device_objects(self):
        pass

    def create_viewport(self):
        self.easel = SurfaceEasel(self.size, self.sdl_window, self.render_options)
        self.viewport = Viewport(easel=self.easel, rect=None)
        self.viewport.make_current()

    def frame(self):
        if self.resize_pending:
            self.resize_pending = False
            return
        self.pre_frame.emit()
        with compose(self.easel):
            with self.renderer.use():
                self.draw()
        self.post_frame.emit()
        self.instance.process_events()

    def on_window(self, event: sdl.WindowEvent):
        # logger.debug("window event")
        match event.type:
            case sdl.EventType.WINDOW_RESIZED:
                self.size = glm.ivec2(event.data1, event.data2)
            case _:
                # pass
                return super().on_window(event)
