import sys, time
from loguru import logger
import glm

from crunge.core import as_capsule

from crunge import sdl

from crunge import wgpu


class Demo:
    kWidth = 1024
    kHeight = 768

    def __init__(self):
        super().__init__()
        self.name = self.__class__.__name__
        self.size = glm.ivec2(self.kWidth, self.kHeight)
        self.window = None

        self.pipeline: wgpu.RenderPipeline = None

        self.surface: wgpu.Surface = None
        self.surface_configured = False

        self.depth_stencil_view: wgpu.TextureView = None

        self.wgpu_context = wgpu.Context()
        self.pending_resize = False
        self.surface_lost = False

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

        if size.x <= 0 or size.y <= 0:
            return

        config = wgpu.SurfaceConfiguration(
            device=self.device,
            width=size.x,
            height=size.y,
            format=wgpu.TextureFormat.BGRA8_UNORM,
            usage=wgpu.TextureUsage.RENDER_ATTACHMENT,
            present_mode=wgpu.PresentMode.FIFO,
            alpha_mode=wgpu.CompositeAlphaMode.OPAQUE,
        )
        self.surface.configure(config)
        self.surface_configured = True
        logger.debug(f"Surface configured to size: {size}")

    def resize(self, size: glm.ivec2):
        logger.debug(f"Resize requested: {size}")
        if size.x <= 0 or size.y <= 0:
            return
        if self.size == size:
            return
        self.size = size
        self.pending_resize = True

    def recreate_surface(self):
        logger.debug("Recreating surface")
        self.surface = None
        self.create_surface()
        self.surface_lost = False
        self.pending_resize = False

    def apply_pending_resize(self):
        if not self.pending_resize:
            return
        self.configure_surface(self.size)
        self.pending_resize = False

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
            handle = sdl.get_number_property(properties, "SDL.window.x11.window", 0)
            display = sdl.get_pointer_property(
                properties, "SDL.window.x11.display", None
            )
            wsd = wgpu.SurfaceSourceXlibWindow(
                display=display,
                window=handle,
            )

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
        if self.surface_lost:
            self.recreate_surface()
            return

        if self.pending_resize:
            self.apply_pending_resize()

        surface_view = self.get_surface_view()
        if surface_view is None:
            return

        self.render(surface_view, self.depth_stencil_view)
        self.surface.present()

    def get_surface_view(self) -> wgpu.TextureView | None:
        if not self.surface_configured:
            return None

        surface_texture = wgpu.SurfaceTexture()
        self.surface.get_current_texture(surface_texture)
        status = surface_texture.status
        logger.debug(f"Surface get current texture status: {status}")

        if status == wgpu.SurfaceGetCurrentTextureStatus.SUCCESS_OPTIMAL:
            return surface_texture.texture.create_view()

        if status == wgpu.SurfaceGetCurrentTextureStatus.SUCCESS_SUBOPTIMAL:
            self.pending_resize = True
            return surface_texture.texture.create_view()

        if status == wgpu.SurfaceGetCurrentTextureStatus.OUTDATED:
            self.pending_resize = True
            return None

        if status == wgpu.SurfaceGetCurrentTextureStatus.LOST:
            self.surface_lost = True
            return None

        if status == wgpu.SurfaceGetCurrentTextureStatus.TIMEOUT:
            return None

        logger.error(f"Failed to acquire surface texture: {status}")
        return None

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
            self.instance.process_events()

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
            #self.instance.process_events()
