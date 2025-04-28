import time
import sys

from loguru import logger
import glfw
import glm

from crunge import wgpu
from crunge import skia

from ..common import Demo


class RectangleDemo(Demo):
    depth_stencil_view: wgpu.TextureView = None

    def __init__(self):
        super().__init__()
        self.skia_context = skia.create_context(self.context.instance, self.context.device)

    def render(self, view: wgpu.TextureView, depthStencilView: wgpu.TextureView):
        # Skia rendering
        recorder = self.skia_context.make_recorder(skia.RecorderOptions())
        surface_texture = wgpu.SurfaceTexture()
        self.surface.get_current_texture(surface_texture)
        backend_texture = surface_texture.texture
        skia_surface = skia.create_surface(backend_texture, recorder)

        if skia_surface:
            canvas = skia_surface.get_canvas()
            #skia_canvas.clear(skia.Color(0, 0, 0, 1))

            paint = skia.Paint()
            #paint.set_color(skia.Color(1, 1, 1, 1))
            paint.set_color(0xFFFFFFFF)
            #skia_canvas.draw_rect(skia.Rect(10, 10, 210, 110), paint)
            #font = skia.Font(None, 36)
            font = skia.Font()
            font.set_size(36)
            #font.set_typeface(skia.Typeface('Arial'))
            #font.set_typeface(None)
            canvas.draw_string('Hello Skia!', 10, 32, font, paint)

            recording = recorder.snap()

            if recording:
                insert_info = skia.InsertRecordingInfo()
                insert_info.f_recording = recording
                self.skia_context.insert_recording(insert_info)
                self.skia_context.submit(skia.SyncToCpu.K_NO)

def main():
    RectangleDemo().run()


if __name__ == "__main__":
    main()
