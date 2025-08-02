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
image = skia.deferred_from_encoded_data(data)
logger.debug(
    f"image: {image}, color_type: {image.color_type()}, alpha_type: {image.alpha_type()}, width: {image.width()}, height: {image.height()}"
)

sampling_options = skia.SamplingOptions()
logger.debug(f"sampling_options: {sampling_options}")

matrix = skia.Matrix()
matrix.set_scale(0.75, 0.75)
matrix.pre_rotate(30.0)
logger.debug(f"matrix: {matrix}")

shader = image.make_shader(
    skia.TileMode.K_REPEAT, skia.TileMode.K_REPEAT, sampling_options, matrix
)


class ImageDemo(Page):
    def _draw(self):
        canvas = Renderer.get_current().canvas
        canvas.draw_image(image, 0, 0)
        super()._draw()


def install(app: App):
    app.add_channel(PageChannel(ImageDemo, "image", "Image"))
