from crunge import skia
#from crunge import yoga

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
        #font.set_size(36)

    def on_size(self):
        super().on_size()
        # Update the font size based on the button size
        self.font.set_size(self.size.y * 0.75)
        
    def draw(self, renderer: Renderer):
        canvas = renderer.canvas

        paint = skia.Paint()
        paint.set_color(0xFFFFFFFF)

        position = self.position
        size = self.size

        canvas.draw_rect(skia.Rect(position.x, position.y, size.x, size.y), paint)
        
        self.font.set_size(self.size.y * 0.5)
        canvas.draw_string(self.text, 10, 32, self.font, self.paint)
