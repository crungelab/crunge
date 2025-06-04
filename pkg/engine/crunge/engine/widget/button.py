from crunge import skia

from . import Widget
from ..renderer import Renderer

class Button(Widget):
    """
    A simple button widget.
    """
    def __init__(self, text: str = "", **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.paint = paint = skia.Paint()
        paint.set_color(0xFFFF00FF)
        self.font = font = skia.Font()
        font.set_size(36)

    def draw(self, renderer: Renderer):
        canvas = renderer.canvas
        canvas.draw_string(self.text, 10, 32, self.font, self.paint)
