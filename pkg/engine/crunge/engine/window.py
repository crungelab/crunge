from typing import List, Dict
import math

from loguru import logger
import glm

from crunge import sdl
from crunge import yoga

from . import globals
from .scheduler import Scheduler
from .frame import Frame
from .viewport import SurfaceViewport
from .renderer import Renderer
from .render_options import RenderOptions
from .channel import Channel

DEFAULT_WIDTH = 1280
DEFAULT_HEIGHT = 720

class Window(Frame):
    def __init__(
        self, width: int = DEFAULT_WIDTH, height: int = DEFAULT_HEIGHT, title="", view=None, resizable=False
    ):
        style = yoga.StyleBuilder().size(width, height).build()
        super().__init__(style, view=view)
        globals.set_current_window(self)
        self.name = title

        self.window: sdl.Window = None
        #self.render_options = RenderOptions(use_depth_stencil=True, use_msaa=True, use_snapshot=True)
        self.render_options = RenderOptions(use_depth_stencil=True, use_snapshot=True)
        self.viewport: SurfaceViewport = None
        self.renderer: Renderer = None

        self._channel: Channel = None
        self.channels: Dict[str, Channel] = {}

    @property
    def channel(self) -> Channel:
        return self._channel

    @channel.setter
    def channel(self, channel: Channel):
        self._channel = channel
        view = channel()
        view.config(window=self)
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
        #self.viewport.size = size
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

    def frame(self):
        try:
            with self.viewport as viewport:
                self.pre_draw(self.renderer)
                self.draw(self.renderer)
                self.post_draw(self.renderer)
        except Exception as e:
            logger.error(f"Error during frame: {e}")
            raise e

    def on_window(self, event: sdl.WindowEvent):
        # logger.debug("window event")
        match event.type:
            case sdl.EventType.WINDOW_RESIZED:
                #self.size = glm.ivec2(event.data1, event.data2)
                self.size = glm.ivec2(self.get_framebuffer_size())
            case _:
                # pass
                return super().on_window(event)
