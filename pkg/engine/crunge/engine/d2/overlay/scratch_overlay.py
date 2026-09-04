from typing import Dict
from loguru import logger
import glm

from crunge import skia

from ...renderer import Renderer

from ... import colors
from ...math import Bounds2

from .debug_overlay import DebugOverlay


class ScratchOverlay(DebugOverlay):
    """Immediate-mode debug drawing, in world units.

    Every method here takes world-space coordinates, Y-up. The canvas set up
    by DebugOverlay.world_canvas already carries the camera transform, so do
    not project before calling. draw_text is the one exception, and it undoes
    the scale locally rather than asking callers to work in a second space.
    """

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
            paint.set_style(skia.Paint.Style.K_STROKE_STYLE)
            paint.set_stroke_width(self._scaled_stroke_width())
            canvas.draw_line(begin[0], begin[1], end[0], end[1], paint)

        self.add_call(draw)

    def draw_fat_segment(
        self, a: glm.vec2, b: glm.vec2, radius: float, color=colors.WHITE
    ):
        # `radius` is world units, unlike outline_width_px — this one is
        # meant to be a thickness in the scene, not a constant on-screen one.
        def draw(canvas: skia.Canvas):
            paint = skia.Paint()
            paint.set_color(color.to_argb_int())
            paint.set_style(skia.Paint.Style.K_STROKE_STYLE)
            paint.set_stroke_width(radius * 2)
            canvas.draw_line(a[0], a[1], b[0], b[1], paint)

        self.add_call(draw)

    def draw_polygon(self, points: "list[glm.vec2]", outline_color=colors.WHITE):
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
            # Was hardcoded 1.0 — a one-metre-thick outline on a world-space
            # canvas, wider than most of what it was outlining.
            outline_paint.set_stroke_width(self._scaled_stroke_width())

            canvas.draw_path(path, outline_paint)

        self.add_call(draw)

    def draw_dot(self, size: float, position: glm.vec2, color=colors.WHITE):
        # `size` is a world-space radius, despite the name.
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
            paint.set_stroke_width(self._scaled_stroke_width())
            canvas.draw_circle(skia.Point(center.x, center.y), radius, paint)

        self.add_call(draw)

    def draw_rect(self, min_point: glm.vec2, max_point: glm.vec2, color=colors.YELLOW):
        """Axis-aligned rect. For a rotated node's extents use draw_obb()."""

        def draw(canvas: skia.Canvas):
            paint = skia.Paint()
            paint.set_color(color.to_argb_int())
            paint.set_style(skia.Paint.Style.K_STROKE_STYLE)
            paint.set_stroke_width(self._scaled_stroke_width())
            canvas.draw_rect(
                skia.Rect(min_point.x, min_point.y, max_point.x, max_point.y), paint
            )

        self.add_call(draw)

    def draw_bounds(self, bounds: Bounds2, color=colors.YELLOW):
        """Draw a world-space AABB. Convenience wrapper over draw_rect."""
        self.draw_rect(bounds.min, bounds.max, color)

    def draw_obb(
        self, local_bounds: Bounds2, transform: glm.mat4, color=colors.YELLOW
    ):
        """Draw local extents through a transform, without flattening to an AABB.

        This is what you want for a debug box that hugs a rotated node.
        Passing the node's world `bounds` to draw_rect instead gives you the
        axis-aligned enclosure, which is correct for broadphase but visibly
        too large at any rotation that is not a multiple of 90 degrees — and
        differently too large per node, since the factor depends on angle.
        """
        corners = [
            glm.vec2(transform * glm.vec4(c.x, c.y, 0.0, 1.0))
            for c in local_bounds.corners
        ]
        self.draw_polygon(corners, color)

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
            scale = self._camera_scale()

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