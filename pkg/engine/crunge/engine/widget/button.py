from loguru import logger

from crunge import skia
from crunge import sdl
#from crunge import yoga

from . import Widget
from ..renderer import Renderer
from ..cursors import CURSOR_HAND, CURSOR_ARROW

PAINT = skia.Paint()
PAINT.set_color(0xFFF3F4F6)

BG_PAINT = skia.Paint()
BG_PAINT.set_color(0xFF23272A)

HOVER_PAINT = skia.Paint()
HOVER_PAINT.set_color(0xFF2563EB)

class Button(Widget):
    def __init__(self, text: str = "", on_click=lambda: 0, **kwargs):
        super().__init__(**kwargs)
        self.text = text
        self.on_click = on_click
        self.paint = PAINT
        self.font = skia.Font()

    def on_size(self):
        super().on_size()
        # Update the font size based on the button size
        self.font.set_size(self.size.y * 0.75)
        
    def draw(self, renderer: Renderer):
        canvas = renderer.canvas
        
        position = self.position
        size = self.size

        canvas.draw_rect(skia.Rect(position.x, position.y, size.x, size.y), BG_PAINT)
        
        self.font.set_size(self.size.y * 0.5)
        canvas.draw_string(self.text, position.x + 10, position.y + self.size.y * 0.75, self.font, self.paint)

    def on_mouse_motion(self, event: sdl.MouseMotionEvent):
        x, y = event.x, event.y
        hovering = self.hit_test(x, y)
        if hovering and not self.hovered:
            self.paint = HOVER_PAINT
            sdl.set_cursor(CURSOR_HAND)
            self.hovered = True
        elif not hovering and self.hovered:
            self.paint = PAINT
            self.hovered = False
            sdl.set_cursor(CURSOR_ARROW)
            # Don't set cursor here! Let the App handle it if needed.

    def on_mouse_button(self, event: sdl.MouseButtonEvent):
        super().on_mouse_button(event)
        if event.button == 1 and event.down: # Left mouse button
            x, y = event.x, event.y
            if self.hit_test(x, y):
                logger.debug(f"Button clicked: {self.text} at ({x}, {y})")
                self.on_click()
                return True # Indicate that the event was handled
    