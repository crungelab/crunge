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
from crunge.core.signal import Signal, Pulse
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
        super()._create()
        logger.debug("Window.create")

        # Pre-pass. Unconstrained, so the root's computed size comes from
        # its style -- the width/height handed to __init__. Computes only:
        # nothing below exists yet to be notified, which is the whole
        # reason calculate and apply are separate calls.
        self.layout.calculate(math.nan, math.nan, yoga.Direction.LTR)
        #logger.debug(f"Window.size: {self.layout.size}")
        logger.debug(f"pre-pass computed: {self.layout.size}")

        # Everything from here to apply() reads geometry off the chip.
        # self.size is still zero: it is written by on_layout, and the
        # first on_layout is the apply() below.
        self.create_window()
        self.create_viewport()
        self.create_device_objects()
        self.create_renderer()

        # Safe now -- on_size needs the easel, so this cannot run any
        # earlier than the easel's own construction.

        # TODO: This used to only be called in _update.  Should it be here?
        self.layout.apply()

        #super()._create()

    @property
    def layout_size(self) -> glm.ivec2:
        """Computed size straight off the chip, in integer pixels.

        For construction-time callers that run before the first apply.
        Everything after that should read self.size.
        """
        return glm.ivec2(self.layout.width, self.layout.height)

    def create_window(self):
        size = self.layout_size
        self.sdl_window = sdl.create_window(
            self.name, size.x, size.y, sdl.WindowFlags.RESIZABLE
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

    def get_window_size(self):
        return sdl.get_window_size(self.sdl_window)

    def get_framebuffer_size(self):
        return sdl.get_window_size_in_pixels(self.sdl_window)

    def create_device_objects(self):
        pass

    def create_viewport(self):
        self.easel = SurfaceEasel(
            self.layout_size, self.sdl_window, self.render_options
        )
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
                # Writes the style, which dirties the tree. The new size
                # comes back through on_layout on the next pass -- the
                # old `self.size = ...` setter did the same thing, but
                # self.size is a plain attribute now and assigning to it
                # would be overwritten by the next apply.
                self.layout.set_size(event.data1, event.data2)
            case _:
                # pass
                return super().on_window(event)