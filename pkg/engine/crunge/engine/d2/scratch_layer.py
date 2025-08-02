from typing import Dict
from loguru import logger
import glm

from crunge import skia

from ..renderer import Renderer
from ..view_layer import ViewLayer

from .. import colors
from ..color import rgba_tuple_to_argb_int


class ScratchLayer(ViewLayer):
    def __init__(self):
        super().__init__("ScratchLayer", priority=900)
        self.draw_calls = []
        self.font_cache: Dict[int, skia.Font] = {}

    # TODO: Consider using a font manager or similar to handle fonts more efficiently
    def create_font(self, font_size: int) -> skia.Font:
        if font_size in self.font_cache:
            return self.font_cache[font_size]

        font = skia.Font()
        font.set_size(font_size)
        self.font_cache[font_size] = font
        return font

    def add_call(self, call):
        self.draw_calls.append(call)

    def draw_line(self, begin: glm.vec2, end: glm.vec2, color=colors.WHITE):
        # logger.debug(f"DemoView.draw_line({begin}, {end}, {color})")
        def draw(canvas: skia.Canvas):
            paint = skia.Paint()
            paint.set_color(rgba_tuple_to_argb_int(color))
            canvas.draw_line(begin[0], begin[1], end[0], end[1], paint)

        self.add_call(draw)

    def draw_polygon(self, points: list[glm.vec2], outline_color=colors.WHITE):
        def draw(canvas: skia.Canvas):
            path = skia.Path()
            if not points:
                return
            path.move_to(*points[0])
            for pt in points[1:]:
                path.line_to(*pt)
            path.close()

            outline_paint = skia.Paint()
            outline_paint.set_color(rgba_tuple_to_argb_int(outline_color))
            outline_paint.set_style(skia.Paint.Style.K_STROKE_STYLE)
            outline_paint.set_stroke_width(1.0)

            canvas.draw_path(path, outline_paint)

        self.add_call(draw)

    def draw_circle(
        self, center: glm.vec2, radius: float, segments: int = 32, color=colors.WHITE
    ):
        def draw(canvas: skia.Canvas):
            # logger.debug(f"draw_circle({center}, {radius}, {segments}, {color})")
            paint = skia.Paint()
            paint.set_color(rgba_tuple_to_argb_int(color))
            paint.set_style(skia.Paint.Style.K_STROKE_STYLE)
            paint.set_stroke_width(2)  # Set the outline thickness as needed
            canvas.draw_circle(skia.Point(center.x, center.y), radius, paint)

        self.add_call(draw)

    def draw_text(
        self, text: str, position: glm.vec2, color=colors.WHITE, font_size=36
    ):
        def draw(canvas: skia.Canvas):
            paint = skia.Paint()
            paint.set_color(rgba_tuple_to_argb_int(color))

            font = self.create_font(font_size)

            # Save current canvas state
            canvas.save()
            # Flip Y back for text (since global is -scale)
            canvas.scale(1, -1)
            # Because the origin is now upside down, position.y must be negated *relative to origin*
            canvas.draw_string(text, position.x, -position.y, font, paint)
            # Restore canvas state
            canvas.restore()

        self.add_call(draw)


    def _draw(self):
        renderer = Renderer.get_current()
        
        with renderer.canvas_target() as canvas:
            canvas.save()

            canvas.translate(
                renderer.viewport.width // 2, renderer.viewport.height // 2
            )
            scale = 1 / renderer.camera_2d.zoom
            canvas.scale(scale, -scale)  # Invert Y-axis for Skia
            camera_x, camera_y = (
                renderer.camera_2d.position.x,
                renderer.camera_2d.position.y,
            )
            canvas.translate(-camera_x, -camera_y)  # pan to camera

            for call in self.draw_calls:
                call(canvas)

            canvas.restore()

        self.draw_calls.clear()
        super()._draw()
