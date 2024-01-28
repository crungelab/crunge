import sys, time
from loguru import logger


from crunge import as_capsule
from crunge import sdl, wgpu
import crunge.wgpu.utils as utils

from .frame import Frame
from .render_context import RenderContext
from . import globals

class Window(Frame):
    def __init__(self, width, height, title="", view=None, resizable=False):
        super().__init__(width, height, view=view)
        self.name = title

        self.window = None
        
        self.context: RenderContext = RenderContext()
        globals.set_current_window(self)

    def create(self):
        #super().create()
        logger.debug("Window.create")
        self.create_window()
        self.create_device_objects()
        self.create_swapchain()
        #return self
        return super().create()

    def create_window(self):
        self.window = sdl.create_window(self.name, self.width, self.height, sdl.WindowFlags.RESIZABLE)

    def get_size(self):
        return sdl.get_window_size(self.window)
    
    def get_framebuffer_size(self):
        return sdl.get_window_size_in_pixels(self.window)
    
    def create_device_objects(self):
        pass

    def create_swapchain(self):
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
            display = sdl.get_property(properties, "SDL.window.x11.display", None)
            wsd.window = handle
            wsd.display = display

        sd = wgpu.SurfaceDescriptor(next_in_chain=wsd)
        self.surface = self.instance.create_surface(sd)
        logger.debug(self.surface)

        scDesc = wgpu.SwapChainDescriptor(
            usage=wgpu.TextureUsage.RENDER_ATTACHMENT,
            format=wgpu.TextureFormat.BGRA8_UNORM,
            width=self.width,
            height=self.height,
            present_mode=wgpu.PresentMode.MAILBOX,
        )

        self.swap_chain = self.device.create_swap_chain(self.surface, scDesc)
        logger.debug(self.swap_chain)

    def frame(self):
        self.context.texture_view = self.swap_chain.get_current_texture_view()

        self.pre_draw()
        self.draw()
        self.post_draw()

        self.swap_chain.present()
