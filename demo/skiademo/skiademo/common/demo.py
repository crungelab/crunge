import sys, time
import contextlib

import glm
import glfw
from loguru import logger

from crunge.core import as_capsule
from crunge import wgpu
from crunge import skia

from .renderer import Renderer

class Demo:
    kWidth = 1024
    kHeight = 768

    device: wgpu.Device = None
    queue: wgpu.Queue = None
    pipeline: wgpu.RenderPipeline = None

    surface: wgpu.Surface = None

    def __init__(self):
        super().__init__()
        self.name = self.__class__.__name__
        self.size = glm.ivec2(self.kWidth, self.kHeight)
        self.wgpu_context = wgpu.Context()
        self.skia_context = skia.create_context(self.wgpu_context.instance, self.wgpu_context.device)
        recorder_options = skia.create_standard_recorder_options()
        self.recorder = self.skia_context.make_recorder(recorder_options)


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
    
    @contextlib.contextmanager
    def canvas_target(self, target: wgpu.Texture = None) :
        if target is None:
            surface_texture = wgpu.SurfaceTexture()
            self.surface.get_current_texture(surface_texture)
            target = surface_texture.texture
        skia_surface = skia.create_surface(target, self.recorder)
        canvas = skia_surface.get_canvas()
        yield canvas
        recording = self.recorder.snap()
        if recording:
            insert_info = skia.InsertRecordingInfo()
            insert_info.f_recording = recording
            self.skia_context.insert_recording(insert_info)
            self.skia_context.submit(skia.SyncToCpu.K_NO)

    def create_window(self):
        glfw.init()

        glfw.window_hint(glfw.CLIENT_API, glfw.NO_API)
        glfw.window_hint(glfw.RESIZABLE, True)

        self.window = glfw.create_window(self.size.x, self.size.y, self.name, None, None)

        def resize_cb(window, w, h):
            self.resize(glm.ivec2(w, h))
        glfw.set_window_size_callback(self.window, resize_cb)


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
            #present_mode=wgpu.PresentMode.MAILBOX,
            alpha_mode=wgpu.CompositeAlphaMode.OPAQUE,
        )
        logger.debug(config)
        self.surface.configure(config)
        logger.debug(f"Surface configured to size: {size}")

    def create_surface(self):
        logger.debug("Creating surface")
        if sys.platform == "darwin":
            handle = glfw.get_cocoa_window(self.window)
            #TODO: Implement SurfaceDescriptorFromMetalLayer
        elif sys.platform == "win32":
            wsd = wgpu.SurfaceDescriptorFromWindowsHWND()
            handle = glfw.get_win32_window(self.window)
            wsd.hwnd = as_capsule(handle)
            wsd.hinstance = None

        elif sys.platform == "linux":
            handle = glfw.get_x11_window(self.window)
            display = glfw.get_x11_display()
            wsd = wgpu.SurfaceSourceXlibWindow(
                window=handle,
                display=as_capsule(display)
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

    def render(self, renderer: Renderer):
        pass

    def frame(self):
        surface_texture = wgpu.SurfaceTexture()
        self.surface.get_current_texture(surface_texture)
        backbufferView: wgpu.TextureView = surface_texture.texture.create_view()

        renderer = Renderer(backbufferView)
        self.render(renderer)
        self.surface.present()

    def run(self):
        self.create_window()
        self.create_device_objects()
        self.create_surface()

        last_time = time.perf_counter()
        target_frame_time = 1 / 60  # Target frame time for 60 FPS

        while not glfw.window_should_close(self.window):
            self.instance.process_events()
            glfw.poll_events()
            #self.instance.process_events()

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


    def resize(self, size: glm.ivec2):
        logger.debug(f"Resizing to {size}")
        if not size.x or not size.y:
            return
        if self.size == size:
            return
        self.size = size
        self.configure_surface(size)
        logger.debug(f"Resized to {size}")
