from __future__ import annotations

import math

from loguru import logger

from crunge import skia
from crunge import box2d

from crunge.engine import colors

from crunge.engine.d2.overlay.debug_overlay import DebugOverlay


from .world import PhysicsWorld2D


def hex_to_argb_int(rgb: int, a: int = 255) -> int:
    return (a << 24) | (rgb & 0xFFFFFF)


class WorldDebugOverlay(DebugOverlay, box2d.DebugDrawBase):
    """Skia renderer for b2DebugDraw.

    Callback contract after box2d #1070:

        draw_polygon(transform, vertices, color)
        draw_solid_polygon(transform, vertices, radius, color)
        draw_circle(center, radius, color)
        draw_solid_circle(transform, center, radius, color)
        draw_solid_capsule(p1, p2, radius, color)
        draw_line(p1, p2, color)
        draw_transform(transform)
        draw_point(p, size, color)
        draw_string(p, text, color)
        draw_bounds(lower, upper, color)

    `transform` is ``(x, y, angle)`` in world space, radians. Polygon vertices and
    the solid-circle center are LOCAL to that transform; everything else already
    arrives in world space. All lengths are meters.
    """

    # Length of the axes drawn by draw_transform, in meters.
    transform_axis_length = 0.25

    # Alpha applied to the fill of solid shapes, so outlines stay readable.
    fill_alpha = 96

    def __init__(self):
        super().__init__("world_debug", 700)
        box2d.DebugDrawBase.__init__(self)

        self.visible = False

        self.draw_shapes = True
        self.draw_joints = True
        self.force_scale = 1.0
        self.joint_scale = 1.0

        self.shape_outline_color = colors.PURPLE

    # ------------- paint helpers -------------

    def _stroke(self, color: int, width: float | None = None) -> skia.Paint:
        paint = skia.Paint()
        paint.set_color(hex_to_argb_int(color))
        paint.set_style(skia.Paint.Style.K_STROKE_STYLE)
        paint.set_stroke_width(
            self._scaled_stroke_width() if width is None else width
        )
        return paint

    def _fill(self, color: int, alpha: int = 255) -> skia.Paint:
        paint = skia.Paint()
        paint.set_color(hex_to_argb_int(color, alpha))
        paint.set_style(skia.Paint.Style.K_FILL_STYLE)
        return paint

    def _polygon_path(self, vertices):
        builder = skia.PathBuilder()
        builder.move_to(*vertices[0])
        for pt in vertices[1:]:
            builder.line_to(*pt)
        builder.close()
        return builder.detach()

    def _push(self, transform) -> None:
        """Move the canvas into the frame the vertices are expressed in."""
        x, y, angle = transform
        self.canvas.save()
        self.canvas.translate(x, y)
        self.canvas.rotate(math.degrees(angle))

    # ------------- Box2D -> Skia primitive callbacks -------------

    def draw_line(self, p1, p2, color: int):
        x1, y1 = p1
        x2, y2 = p2
        self.canvas.draw_line(x1, y1, x2, y2, self._stroke(color))

    def draw_polygon(self, transform, vertices, color: int):
        if not vertices:
            return

        self._push(transform)
        try:
            self.canvas.draw_path(self._polygon_path(vertices), self._stroke(color))
        finally:
            self.canvas.restore()

    def draw_solid_polygon(self, transform, vertices, radius: float, color: int):
        if not vertices:
            return

        self._push(transform)
        try:
            path = self._polygon_path(vertices)
            self.canvas.draw_path(path, self._fill(color, self.fill_alpha))

            # `radius` is the rounding on the polygon skin. Approximating it with a
            # fat stroke is not exact, but it makes rounded shapes legible.
            width = max(self._scaled_stroke_width(), radius * 2.0) if radius > 0 else None
            self.canvas.draw_path(path, self._stroke(color, width))
        finally:
            self.canvas.restore()

    def draw_circle(self, center, radius: float, color: int):
        x, y = center
        self.canvas.draw_circle(skia.Point(x, y), radius, self._stroke(color))

    def draw_solid_circle(self, transform, center, radius: float, color: int):
        # `center` is local to `transform`; resolve it to world space.
        px, py, angle = transform
        c = math.cos(angle)
        s = math.sin(angle)
        cx, cy = center
        x = px + c * cx - s * cy
        y = py + s * cx + c * cy

        point = skia.Point(x, y)
        self.canvas.draw_circle(point, radius, self._fill(color, self.fill_alpha))
        self.canvas.draw_circle(point, radius, self._stroke(color))

        # Orientation spoke along the body's local x axis.
        self.draw_line((x, y), (x + c * radius, y + s * radius), color)

    def draw_solid_capsule(self, p1, p2, radius: float, color: int):
        x1, y1 = p1
        x2, y2 = p2

        paint = self._stroke(color, max(self._scaled_stroke_width(), radius * 2.0))
        paint.set_stroke_cap(skia.Paint.Cap.K_ROUND_CAP)
        self.canvas.draw_line(x1, y1, x2, y2, paint)

    def draw_point(self, p, size: float, color: int):
        x, y = p
        # `size` is a screen-space point size; the canvas is in meters.
        r = size / self.ppu
        self.canvas.draw_circle(skia.Point(x, y), r, self._fill(color))

    def draw_transform(self, transform):
        x, y, angle = transform
        c = math.cos(angle)
        s = math.sin(angle)
        length = self.transform_axis_length

        self.draw_line((x, y), (x + c * length, y + s * length), 0xFF0000)
        self.draw_line((x, y), (x - s * length, y + c * length), 0x00FF00)

    def draw_bounds(self, lower, upper, color: int):
        lx, ly = lower
        ux, uy = upper

        builder = skia.PathBuilder()
        builder.move_to(lx, ly)
        builder.line_to(ux, ly)
        builder.line_to(ux, uy)
        builder.line_to(lx, uy)
        builder.close()
        self.canvas.draw_path(builder.detach(), self._stroke(color))

    def draw_string(self, p, s: str, color: int):
        # TODO: wire up a skia.Font and canvas text draw.
        x, y = p
        logger.debug(f"DebugDraw text @({x:.2f},{y:.2f}): {s}")

    def draw_items(self):
        world = PhysicsWorld2D.get_current()
        world.draw(self)