from loguru import logger

from crunge import skia
from crunge.engine import Renderer, App
from crunge.demo import PageChannel

from ..page import Page


info = skia.ImageInfo()
data = skia.Data.make_from_file_name(
    "../../depot/skia/resources/images/color_wheel.png"
)
logger.debug(f"data: {data}")
# image = skia.raster_from_data(info, data, 3)
image = skia.deferred_from_encoded_data(data)
logger.debug(f"image: {image}")

sampling_options = skia.SamplingOptions()

matrix = skia.Matrix()
matrix.set_scale(0.75, 0.75)
matrix.pre_rotate(30.0)

shader = image.make_shader(
    skia.TileMode.K_REPEAT, skia.TileMode.K_REPEAT, sampling_options, matrix
)


class ImageShaderPage(Page):
    def _draw(self):
        renderer = Renderer.get_current()
        with renderer.canvas_target() as canvas:
            canvas.clear(skia.colors.WHITE)

            paint = skia.Paint()
            paint.set_shader(shader)
            canvas.draw_paint(paint)
        super()._draw()


def install(app: App):
    app.add_channel(PageChannel(ImageShaderPage, "image_shader", "Image Shader"))
