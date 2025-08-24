from typing import List, Dict
import math

from loguru import logger
import glm

from crunge import sdl
from crunge import yoga

from . import globals
from .scheduler import Scheduler
from .node import NodeListener
from .frame import Frame
from .viewport import SurfaceViewport
from .renderer import Renderer
from .render_options import RenderOptions
from .channel import Channel

DEFAULT_WIDTH = 1280
DEFAULT_HEIGHT = 720


class WindowListener(NodeListener):
    def on_window_size(self, size: glm.ivec2):
        pass

    def on_pre_frame(self):
        pass

    def on_post_frame(self):
        pass

    def on_channel(self, channel: Channel):
        pass


class Window(Frame):
    def __init__(
        self,
        width: int = DEFAULT_WIDTH,
        height: int = DEFAULT_HEIGHT,
        title="",
        view=None,
        resizable=False,
    ):
        style = yoga.StyleBuilder().size(width, height).build()
        super().__init__(style, view=view)
        globals.set_current_window(self)
        self.name = title
        self.listeners: List[WindowListener] = []

        self.window: sdl.Window = None
        # self.render_options = RenderOptions(use_depth_stencil=True, use_msaa=True, use_snapshot=True)
        self.render_options = RenderOptions(use_depth_stencil=True, use_snapshot=True)
        self.viewport: SurfaceViewport = None
        self.renderer: Renderer = None

        # TODO: This should go in the Frame class
        self._channel: Channel = None
        self.channels: Dict[str, Channel] = {}

        self.update_time: float = 0.0
        self.frame_time: float = 0.0

    @property
    def channel(self) -> Channel:
        return self._channel

    @channel.setter
    def channel(self, channel: Channel):
        self._channel = channel
        view = channel()
        self.view = view

    def add_channel(self, channel: Channel):
        if channel.name in self.channels:
            raise ValueError(f"Channel already exists for name: {channel.name}")
        self.channels[channel.name] = channel

    def show_channel(self, name: str):
        # logger.debug(f"show {name}")
        def callback(delta_time: float):
            channel = self.channels.get(name)
            if channel is None:
                raise ValueError(f"Channel not found for name: {name}")

            self.channel = channel

        Scheduler().schedule_once(callback, 0)

    def _create(self):
        logger.debug("Window.create")
        self.layout.calculate_bounds(math.nan, math.nan, yoga.Direction.LTR)
        logger.debug(f"Window.size: {self.size}")
        self.create_window()
        self.create_device_objects()
        self.create_viewport()
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
        # self.viewport.size = size
        self.viewport.size = glm.ivec2(self.get_framebuffer_size())

        logger.debug(f"Resized to {size}")

    def get_window_size(self):
        return sdl.get_window_size(self.window)

    def get_framebuffer_size(self):
        return sdl.get_window_size_in_pixels(self.window)

    def create_device_objects(self):
        pass

    def create_viewport(self):
        self.viewport = SurfaceViewport(self.size, self.window, self.render_options)

    def pre_frame(self):
        for listener in self.listeners:
            if isinstance(listener, WindowListener):
                listener.on_pre_frame()

    def post_frame(self):
        for listener in self.listeners:
            if isinstance(listener, WindowListener):
                listener.on_post_frame()

    def frame(self):
        self.pre_frame()
        with self.viewport.frame():
            with self.renderer.use():
                self.draw()
        self.post_frame()

    '''
    def frame(self):
        self.pre_frame()
        with self.viewport:
            self.renderer.make_current()
            self.draw()
        self.post_frame()
    '''

    def on_window(self, event: sdl.WindowEvent):
        # logger.debug("window event")
        match event.type:
            case sdl.EventType.WINDOW_RESIZED:
                # self.size = glm.ivec2(event.data1, event.data2)
                self.size = glm.ivec2(self.get_framebuffer_size())
            case _:
                # pass
                return super().on_window(event)
