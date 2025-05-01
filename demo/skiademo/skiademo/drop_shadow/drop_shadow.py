from loguru import logger

from crunge import wgpu
from crunge import skia

from ..common import Demo


class FractalPerlinNoiseDemo(Demo):
    depth_stencil_view: wgpu.TextureView = None

    def __init__(self):
        super().__init__()
        self.skia_context = skia.create_context(
            self.context.instance, self.context.device
        )

    def render(self, view: wgpu.TextureView, depthStencilView: wgpu.TextureView):
        # Skia rendering
        recorder = self.skia_context.make_recorder(skia.RecorderOptions())
        surface_texture = wgpu.SurfaceTexture()
        self.surface.get_current_texture(surface_texture)
        backend_texture = surface_texture.texture
        skia_surface = skia.create_surface(backend_texture, recorder)

        if skia_surface:
            canvas = skia_surface.get_canvas()

            canvas.draw_color(skia.Colors.WHITE)

            filter = skia.ImageFilters.drop_shadow(3, 3, 5, 5, skia.Colors.BLACK)
            filter_paint = skia.Paint()
            filter_paint.set_image_filter(filter)

            '''
            paint = skia.Paint(
                ImageFilter=skia.ImageFilters.DropShadow(3, 3, 5, 5, skia.ColorBLACK)
            )
            blob = skia.TextBlob("Skia", skia.Font(None, 120))
            canvas.drawTextBlob(blob, 0, 160, paint)
            '''

            '''
            gradient_paint = skia.Paint()

            shader = skia.PerlinNoiseShader.make_fractal_noise(0.05, 0.05, 4, 0.0)
            #logger.debug(f"shader: {shader}")

            gradient_paint.set_shader(shader)
            canvas.draw_rect(skia.Rect(0, 0, 256, 256), gradient_paint)
            #canvas.draw_paint(paint)
            '''

            '''
            text_paint = skia.Paint()
            text_paint.set_color(0xFFFFFFFF)
            font = skia.Font()
            font.set_size(36)
            canvas.draw_string('Hello Skia!', 10, 32, font, text_paint)
            '''

            recording = recorder.snap()

            if recording:
                insert_info = skia.InsertRecordingInfo()
                insert_info.f_recording = recording
                self.skia_context.insert_recording(insert_info)
                self.skia_context.submit(skia.SyncToCpu.K_NO)


def main():
    FractalPerlinNoiseDemo().run()


if __name__ == "__main__":
    main()
