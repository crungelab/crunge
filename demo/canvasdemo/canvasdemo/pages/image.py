from loguru import logger

from crunge import skia
from crunge.engine import Renderer, App
from crunge.demo import PageChannel

from ..page import Page


class ImageDemo(Page):
    def setup(self):
        super().setup()
        data = skia.Data.make_from_file_name(
            "../../depot/skia/resources/images/color_wheel.png"
        )
        logger.debug(f"data: {data}")
        self.image = skia.deferred_from_encoded_data(data)
        logger.debug(
            f"image: {self.image}, color_type: {self.image.color_type()}, alpha_type: {self.image.alpha_type()}, width: {self.image.width()}, height: {self.image.height()}"
        )

    def _draw(self):
        canvas = Renderer.get_current().canvas
        canvas.draw_image(self.image, 0, 0)
        super()._draw()


"""
data = skia.Data.make_from_file_name(
    "../../depot/skia/resources/images/color_wheel.png"
)
logger.debug(f"data: {data}")
image = skia.deferred_from_encoded_data(data)
logger.debug(
    f"image: {image}, color_type: {image.color_type()}, alpha_type: {image.alpha_type()}, width: {image.width()}, height: {image.height()}"
)

class ImageDemo(Page):
    def _draw(self):
        canvas = Renderer.get_current().canvas
        canvas.draw_image(image, 0, 0)
        super()._draw()
"""


def install(app: App):
    app.add_channel(PageChannel(ImageDemo, "image", "Image"))
