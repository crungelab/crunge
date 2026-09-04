from typing import Dict
from loguru import logger
import glm

from crunge import skia

from ...renderer import Renderer

from ... import colors
from ...math import Bounds2

from .debug_overlay import DebugOverlay

class ScratchOverlay(DebugOverlay):
    def __init__(self):
        super().__init__("ScratchOverlay", priority=900)
        self.draw_calls = []
        self.font_cache: Dict[int, skia.Font] = {}

    # TODO: Consider using a font manager or similar to handle fonts more efficiently
    def create_font(self, font_size: int) -> skia.Font:
        # font_size is a true pixel size — draw_text() cancels out the
        # world-unit -> pixel scale before drawing, so no ppu scaling here.
        if font_size in self.font_cache:
            return self.font_cache[font_size]

        font = skia.Font()
        font.set_size(font_size)
        self.font_cache[font_size] = font
        return font

    def add_call(self, call):
        self.draw_calls.append(call)

    def draw_segment(self, begin: glm.vec2, end: glm.vec2, color=colors.WHITE):
        def draw(canvas: skia.Canvas):
            paint = skia.Paint()
            paint.set_color(color.to_argb_int())
            canvas.draw_line(begin[0], begin[1], end[0], end[1], paint)

        self.add_call(draw)

    def draw_fat_segment(
        self, a: glm.vec2, b: glm.vec2, radius: float, color=colors.WHITE
    ):
        def draw(canvas: skia.Canvas):
            paint = skia.Paint()
            paint.set_color(color.to_argb_int())
            paint.set_style(skia.Paint.Style.K_STROKE_STYLE)
            paint.set_stroke_width(radius * 2)
            canvas.draw_line(a[0], a[1], b[0], b[1], paint)

        self.add_call(draw)

    def draw_polygon(self, points: list[glm.vec2], outline_color=colors.WHITE):
        def draw(canvas: skia.Canvas):
            if not points:
                return

            builder = skia.PathBuilder()
            builder.move_to(*points[0])
            for pt in points[1:]:
                builder.line_to(*pt)
            builder.close()
            path = builder.detach()

            outline_paint = skia.Paint()
            outline_paint.set_color(outline_color.to_argb_int())
            outline_paint.set_style(skia.Paint.Style.K_STROKE_STYLE)
            outline_paint.set_stroke_width(1.0)

            canvas.draw_path(path, outline_paint)

        self.add_call(draw)

    def draw_dot(self, size: float, position: glm.vec2, color=colors.WHITE):
        def draw(canvas: skia.Canvas):
            paint = skia.Paint()
            paint.set_color(color.to_argb_int())
            canvas.draw_circle(skia.Point(position.x, position.y), size, paint)

        self.add_call(draw)

    def draw_circle(
        self, center: glm.vec2, radius: float, segments: int = 32, color=colors.WHITE
    ):
        def draw(canvas: skia.Canvas):
            paint = skia.Paint()
            paint.set_color(color.to_argb_int())
            paint.set_style(skia.Paint.Style.K_STROKE_STYLE)
            paint.set_stroke_width(self._scaled_stroke_width())  # Set the outline thickness as needed
            canvas.draw_circle(skia.Point(center.x, center.y), radius, paint)

        self.add_call(draw)

    def draw_bounds_2d(self, aabb: Bounds2, color=colors.YELLOW):
        min_point = glm.vec2(aabb.min.x, aabb.min.y)
        max_point = glm.vec2(aabb.max.x, aabb.max.y)

        def draw(canvas: skia.Canvas):
            paint = skia.Paint()
            paint.set_color(color.to_argb_int())
            paint.set_style(skia.Paint.Style.K_STROKE_STYLE)
            paint.set_stroke_width(self._scaled_stroke_width())  # Set the outline thickness as needed
            canvas.draw_rect(
                skia.Rect(min_point.x, min_point.y, max_point.x, max_point.y), paint
            )

        self.add_call(draw)
        
    def draw_text(
        self, text: str, position: glm.vec2, color=colors.WHITE, font_size=36
    ):
        def draw(canvas: skia.Canvas):
            paint = skia.Paint()
            paint.set_color(color.to_argb_int())

            font = self.create_font(font_size)

            # At this point the canvas transform is:
            #   translate(viewport center) * scale(scale, -scale) * translate(-camera)
            # where scale = camera.ppu / camera.zoom, so draw calls can work
            # directly in world units. Text is the exception: we want a
            # constant pixel-sized font regardless of ppu/zoom, so cancel the
            # outer scale out locally and manually project `position`
            # (world units) into that unscaled local space.
            renderer = Renderer.get_current()
            scale = renderer.camera_2d.ppu / renderer.camera_2d.zoom

            canvas.save()
            canvas.scale(1.0 / scale, -1.0 / scale)
            canvas.draw_string(
                text, position.x * scale, -position.y * scale, font, paint
            )
            canvas.restore()

        self.add_call(draw)

    def _draw(self):
        if len(self.draw_calls) == 0:
            return
        
        super()._draw()

        self.draw_calls.clear()

    def draw_items(self):
        for call in self.draw_calls:
            call(self.canvas)
