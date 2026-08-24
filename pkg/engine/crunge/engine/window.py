from typing import Optional
import math

import contextlib
from contextvars import ContextVar

from loguru import logger
import glm

from crunge import sdl
from crunge import yoga

from . import globals
from .math import Rect2i
from .signal import Signal, Pulse
from .scheduler import Scheduler
from .frame import Frame
from .viewport import Viewport
from .easel import SurfaceEasel
from .renderer import Renderer, RenderFrame
from .render_options import RenderOptions
from .channel import Channel

DEFAULT_WIDTH = 1280
DEFAULT_HEIGHT = 720

current_window: ContextVar[Optional["Window"]] = ContextVar("current_window", default=None)

class Window(Frame):
    def __init__(
        self,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
        title="",
        screen=None,
        resizable=False,
    ):
        style = yoga.StyleBuilder().size(width, height).build()
        super().__init__(style, screen=screen)
        globals.set_current_window(self)
        self.name = title

        self.window: sdl.Window = None
        # self.render_options = RenderOptions(use_depth_stencil=True, use_msaa=True, use_snapshot=True)
        self.render_options = RenderOptions(use_depth_stencil=True, use_snapshot=True)
        self.viewport: Viewport = None
        self.easel: SurfaceEasel = None
        self.renderer: Renderer = None

        # TODO: This should go in the Frame class
        self._channel: Channel = None
        self.channels: dict[str, Channel] = {}

        self.update_time: float = 0.0
        self.render_time: float = 0.0
        self.frame_time: float = 0.0

        self.resize_pending = False
        self.window_size: Signal[glm.ivec2] = Signal()
        self.pre_frame: Pulse = Pulse()
        self.post_frame: Pulse = Pulse()
        self.channel_changed: Signal[Channel] = Signal()

    def make_current(self):
        current_window.set(self)

    @classmethod
    def get_current(cls) -> Optional["Window"]:
        return current_window.get()

    @contextlib.contextmanager
    def use(self):
        prev_window = self.get_current()
        self.make_current()
        yield self
        if prev_window is not None:
            prev_window.make_current()

    @property
    def channel(self) -> Channel:
        return self._channel

    @channel.setter
    def channel(self, channel: Channel):
        self._channel = channel
        view = channel()
        self.screen = view
        self.channel_changed.emit(channel)

    def add_channel(self, channel: Channel):
        if channel.name in self.channels:
            raise ValueError(f"Channel already exists for name: {channel.name}")
        self.channels[channel.name] = channel

    def add_channels(self, channels: list[Channel]):
        for channel in channels:
            self.add_channel(channel)

    def show_channel(self, name: str):
        # logger.debug(f"show {name}")
        def callback(delta_time: float):
            channel = self.channels.get(name)
            if channel is None:
                raise ValueError(f"Channel not found for name: {name}")

            self.channel = channel

        Scheduler().schedule_once(callback, 0)

    def reshow_channel(self):
        if self.channel is not None:
            self.show_channel(self.channel.name)

    def show_next_channel(self):
        self.show_channel(self.channel.next_channel)

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
        self.window = sdl.create_window(
            self.name, self.width, self.height, sdl.WindowFlags.RESIZABLE
        )

    def create_renderer(self):
        self.renderer = Renderer(self.viewport)

    def on_size(self):
        super().on_size()
        size = self.size
        if not size.x or not size.y:
            return

        self.easel.size = glm.ivec2(self.get_framebuffer_size())

        logger.debug(f"Resized to {size}")
        self.resize_pending = True

    """
    def on_resize(self):
        self.viewport.size = glm.ivec2(self.get_framebuffer_size())
        self.resize_pending = False
    """

    def get_window_size(self):
        return sdl.get_window_size(self.window)

    def get_framebuffer_size(self):
        return sdl.get_window_size_in_pixels(self.window)

    def create_device_objects(self):
        pass

    def create_viewport(self):
        self.easel = SurfaceEasel(self.size, self.window, self.render_options)
        self.viewport = Viewport(easel=self.easel, rect=None)
        self.viewport.make_current()

    def frame(self):
        if self.resize_pending:
            self.resize_pending = False
            return

        self.pre_frame.emit()

        with self.easel.frame():
            encoder = self.device.create_command_encoder()
            frame = RenderFrame(self.easel, encoder)

            with self.renderer.use():
                with frame.use():
                    self.draw()
            self.queue.submit([encoder.finish()])

        self.post_frame.emit()
        self.instance.process_events()

    """
    def frame(self):
        if self.resize_pending:
            self.resize_pending = False
            return

        self.pre_frame.emit()

        with self.easel.frame():
            with self.renderer.use():
                self.draw()

        self.post_frame.emit()
        self.instance.process_events()
    """

    def on_window(self, event: sdl.WindowEvent):
        # logger.debug("window event")
        match event.type:
            case sdl.EventType.WINDOW_RESIZED:
                self.size = glm.ivec2(event.data1, event.data2)
                # self.size = glm.ivec2(self.get_framebuffer_size())
            case _:
                # pass
                return super().on_window(event)
