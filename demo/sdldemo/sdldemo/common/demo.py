import sys, time
from loguru import logger
import glm

from crunge.core import as_capsule

from crunge import sdl

from crunge import wgpu


class Demo:
    kWidth = 1024
    kHeight = 768

    device: wgpu.Device = None
    queue: wgpu.Queue = None
    pipeline: wgpu.RenderPipeline = None

    surface: wgpu.Surface = None

    depth_stencil_view: wgpu.TextureView = None

    def __init__(self):
        super().__init__()
        self.name = self.__class__.__name__
        self.size = glm.ivec2(self.kWidth, self.kHeight)
        self.window = None

        self.wgpu_context = wgpu.Context()

    @property
    def instance(self) -> wgpu.Instance:
        return self.wgpu_context.instance

    @property
    def adapter(self) -> wgpu.Adapter:
        return self.wgpu_context.adapter

    @property
    def device(self) -> wgpu.Device:
        return self.wgpu_context.device

    @property
    def queue(self) -> wgpu.Queue:
        return self.wgpu_context.queue

    def create_window(self):
        success = sdl.init(sdl.InitFlags.INIT_VIDEO)
        logger.debug(f"SDL_Init: {success}")
        self.window = sdl.create_window(
            self.name, self.size.x, self.size.y, sdl.WindowFlags.RESIZABLE
        )

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
            alpha_mode=wgpu.CompositeAlphaMode.OPAQUE,
        )
        logger.debug(config)
        self.surface.configure(config)
        logger.debug(f"Surface configured to size: {size}")

    def resize(self, size: glm.ivec2):
        logger.debug(f"Resizing to {size}")
        if not size.x or not size.y:
            return
        if self.size == size:
            return
        self.size = size
        self.configure_surface(size)
        logger.debug(f"Resized to {size}")

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
            # wsd = wgpu.SurfaceDescriptorFromXlibWindow()
            wsd = wgpu.SurfaceSourceXlibWindow()
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

    def create_shader_module(self, code: str) -> wgpu.ShaderModule:
        wgsl_desc = wgpu.ShaderSourceWGSL(code=code)
        sm_descriptor = wgpu.ShaderModuleDescriptor(next_in_chain=wgsl_desc)
        shader_module = self.device.create_shader_module(sm_descriptor)
        return shader_module

    def render(self, view: wgpu.TextureView, depthStencilView: wgpu.TextureView = None):
        pass

    def frame(self):
        backbuffer: wgpu.TextureView = self.get_surface_view()
        self.render(backbuffer, self.depth_stencil_view)
        self.surface.present()

    def get_surface_view(self) -> wgpu.TextureView:
        surface_texture = wgpu.SurfaceTexture()
        self.surface.get_current_texture(surface_texture)
        surface_view: wgpu.TextureView = surface_texture.texture.create_view()
        return surface_view

    def dispatch(self, event):
        # logger.debug(event)
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
            case sdl.EventType.WINDOW_RESIZED:
                self.resize(glm.ivec2(event.data1, event.data2))
            case _:
                pass

    def on_mouse_enter(self, event: sdl.WindowEvent):
        logger.debug("mouse enter")

    def on_mouse_leave(self, event: sdl.WindowEvent):
        logger.debug("mouse leave")

    def on_mouse_motion(self, event: sdl.MouseMotionEvent):
        logger.debug(f"mouse motion: x={event.x}, y={event.y}")

    def on_mouse_button(self, event: sdl.MouseButtonEvent):
        logger.debug(f"mouse button: button={event.button}, down={event.down}")

    def on_mouse_wheel(self, event: sdl.MouseWheelEvent):
        logger.debug(f"mouse wheel: x={event.x}, y={event.y}")

    def run(self):
        self.create_window()
        self.create_device_objects()
        self.create_surface()

        last_time = time.perf_counter()
        target_frame_time = 1 / 60  # Target frame time for 60 FPS

        running = True
        while running:
            # self.instance.process_events()

            while event := sdl.poll_event():
                if not self.dispatch(event):
                    running = False

            now = time.perf_counter()
            frame_time = now - last_time

            # Calculate how much time is left to delay to maintain 60 FPS
            time_left = target_frame_time - frame_time

            # If there's time left in this frame, delay the next frame
            if time_left > 0:
                time.sleep(time_left)

            # Update last_time for the next frame, considering the sleep
            last_time = time.perf_counter()

            self.frame()

            # TODO: Losing device on resize
            self.instance.process_events()
