import sys, time
from loguru import logger


from crunge.core import as_capsule
from crunge import sdl, wgpu
import crunge.wgpu.utils as utils

class Window:
    def __init__(self, width, height, title="", resizable=False):
        super().__init__()
        self.width = width
        self.height = height
        self.name = title

        self.window = None
        
        self.instance = wgpu.create_instance()
        self.adapter = self.instance.request_adapter()
        self.device = self.adapter.create_device()
        self.device.set_label("Primary Device")
        self.device.enable_logging()
        self.queue = self.device.get_queue()

        self.depth_stencil_view: wgpu.TextureView = None

    def create(self):
        logger.debug("create")
        self.create_window()
        self.create_device_objects()
        self.create_swapchain()
        return self

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

    def create_shader_module(self, code: str) -> wgpu.ShaderModule:
        wgsl_desc = wgpu.ShaderModuleWGSLDescriptor(code=code)
        sm_descriptor = wgpu.ShaderModuleDescriptor(next_in_chain=wgsl_desc)
        shader_module = self.device.create_shader_module(sm_descriptor)
        return shader_module

    def on_draw(self):
        pass
    
    def render(self, view: wgpu.TextureView, depthStencilView: wgpu.TextureView = None):
        pass

    def frame(self):
        backbuffer: wgpu.TextureView = self.swap_chain.get_current_texture_view()
        self.render(backbuffer, self.depth_stencil_view)
        self.swap_chain.present()

    def dispatch(self, event):
        #logger.debug(event)
        match event.__class__:
            case sdl.QuitEvent:
                return False
            case sdl.WindowEvent:
                self.on_window(event)
            case sdl.MouseMotionEvent:
                self.on_mouse_motion(event)
            case sdl.MouseButtonEvent:
                self.on_mouse_button(event)
            case sdl.MouseWheelEvent:
                self.on_mouse_wheel(event)
            case _:
                pass
        return True

    def on_window(self, event: sdl.WindowEvent):
        logger.debug("window event")
        match event.type:
            case sdl.EventType.WINDOW_MOUSE_ENTER:
                self.on_mouse_enter(event)
            case sdl.EventType.WINDOW_MOUSE_LEAVE:
                self.on_mouse_leave(event)
            case _:
                pass

    def on_mouse_enter(self, event: sdl.WindowEvent):
        logger.debug("mouse enter")

    def on_mouse_leave(self, event: sdl.WindowEvent):
        logger.debug("mouse leave")

    def on_mouse_motion(self, event: sdl.MouseMotionEvent):
        logger.debug(f"mouse motion: x={event.x}, y={event.y}")

    def on_mouse_button(self, event: sdl.MouseButtonEvent):
        logger.debug(f"mouse button: button={event.button}, state={event.state}")

    def on_mouse_wheel(self, event: sdl.MouseWheelEvent):
        logger.debug(f"mouse wheel: x={event.x}, y={event.y}")
