import time
import sys

from loguru import logger
import glfw
import glm

from crunge import wgpu
from crunge import skia

from ..common import Demo


class TextDemo(Demo):
    def __init__(self):
        super().__init__()
        self.skia_context = skia.create_context(self.context.instance, self.context.device)
        self.recorder = self.skia_context.make_recorder(skia.RecorderOptions())

    def render(self, view: wgpu.TextureView, depthStencilView: wgpu.TextureView):
        surface_texture = wgpu.SurfaceTexture()
        self.surface.get_current_texture(surface_texture)
        backend_texture = surface_texture.texture
        skia_surface = skia.create_surface(backend_texture, self.recorder)

        if skia_surface:
            canvas = skia_surface.get_canvas()
            #canvas.clear(0xFF00FF00)  # Clear with a color

            paint = skia.Paint()
            paint.set_color(0xFFFF00FF)
            #font = skia.Font(None, 36)
            font = skia.Font()
            font.set_size(36)
            #font.set_typeface(skia.Typeface('Arial'))
            #font.set_typeface(None)
            canvas.draw_string('Hello Skia!', 10, 32, font, paint)

            recording = self.recorder.snap()

            if recording:
                insert_info = skia.InsertRecordingInfo()
                insert_info.f_recording = recording
                self.skia_context.insert_recording(insert_info)
                self.skia_context.submit(skia.SyncToCpu.K_NO)

def main():
    TextDemo().run()


if __name__ == "__main__":
    main()
