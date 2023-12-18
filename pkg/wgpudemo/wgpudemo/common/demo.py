import sys, time
import glfw
from loguru import logger

from crunge.core import as_capsule
from crunge import wgpu
import crunge.wgpu.utils as utils

class Demo:
    kWidth = 1024
    kHeight = 768

    device: wgpu.Device = None
    queue: wgpu.Queue = None
    pipeline: wgpu.RenderPipeline = None

    surface: wgpu.Surface = None
    swap_chain: wgpu.SwapChain = None

    def __init__(self):
        super().__init__()
        self.name = self.__class__.__name__
        self.instance = wgpu.create_instance()
        self.adapter = self.instance.request_adapter()
        self.device = self.adapter.create_device()
        self.device.set_label("Primary Device")
        self.device.enable_logging()
        self.queue = self.device.get_queue()

    def create_window(self):
        glfw.init()

        glfw.window_hint(glfw.CLIENT_API, glfw.NO_API)
        glfw.window_hint(glfw.RESIZABLE, True)

        self.window = glfw.create_window(self.kWidth, self.kHeight, self.name, None, None)

    def create_swapchain(self):
        if sys.platform == "darwin":
            handle = glfw.get_cocoa_window(self.window)
        elif sys.platform == "win32":
            wsd = wgpu.SurfaceDescriptorFromWindowsHWND()
            handle = glfw.get_win32_window(self.window)
            wsd.hwnd = as_capsule(handle)
            wsd.hinstance = None

        elif sys.platform == "linux":
            wsd = wgpu.SurfaceDescriptorFromXlibWindow()
            handle = glfw.get_x11_window(self.window)
            display = glfw.get_x11_display()
            wsd.window = handle
            wsd.display = as_capsule(display)

        sd = wgpu.SurfaceDescriptor(next_in_chain=wsd)
        self.surface = self.instance.create_surface(sd)
        logger.debug(self.surface)

        scDesc = wgpu.SwapChainDescriptor(
            usage=wgpu.TextureUsage.RENDER_ATTACHMENT,
            format=wgpu.TextureFormat.BGRA8_UNORM,
            width=self.kWidth,
            height=self.kHeight,
            present_mode=wgpu.PresentMode.MAILBOX,
        )

        self.swap_chain = self.device.create_swap_chain(self.surface, scDesc)
        logger.debug(self.swap_chain)


    def frame(self):
        pass

    def run(self):
        self.create_window()
        self.create_swapchain()

        last_time = None
        while not glfw.window_should_close(self.window):
            glfw.poll_events()

            now = time.perf_counter()
            if not last_time:
                last_time = now

            frame_time = now - last_time
            last_time = now

            self.frame()

        glfw.destroy_window(self.window)
        glfw.terminate()
