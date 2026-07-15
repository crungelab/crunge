from __future__ import annotations

from loguru import logger
import glm

from crunge import box2d
from crunge import skia

from crunge.engine import Renderer, colors


def hex_to_argb_int(rgb: int, a: int = 255) -> int:
    return (a << 24) | (rgb & 0xFFFFFF)


def transform_pos(transform: tuple[float, float, float, float]) -> tuple[float, float]:
    """(px, py, c, s) -> (px, py)"""
    return (transform[0], transform[1])


class DebugDraw(box2d.DebugDrawBase):
    def __init__(self):
        super().__init__()  # IMPORTANT: sets up C++ context + cache
        # self.canvas: skia.SkiaCanvas = None

        # Use the new C++ exposed properties/flags if you bound them
        # (from the full file: draw_shapes/draw_joints/force_scale/joint_scale)
        self.draw_shapes = True
        self.draw_joints = True
        self.force_scale = 1.0
        self.joint_scale = 1.0

        # Your engine palette (RGBA tuples)
        self.shape_outline_color = colors.PURPLE

    @property
    def canvas(self) -> skia.Canvas:
        renderer = Renderer.get_current()
        return renderer.canvas

    # ------------- Box2D -> Skia primitive callbacks -------------

    def draw_line(self, p1, p2, color: int):
        x1, y1 = p1
        x2, y2 = p2
        paint = skia.Paint()
        paint.set_color(hex_to_argb_int(color))
        paint.set_style(skia.Paint.Style.K_STROKE_STYLE)
        paint.set_stroke_width(1.0)
        self.canvas.draw_line(x1, y1, x2, y2, paint)

    def draw_polygon(self, vertices, color: int):
        # vertices: list[(x,y), ...]
        if not vertices:
            return

        builder = skia.PathBuilder()
        builder.move_to(*vertices[0])
        for pt in vertices[1:]:
            builder.line_to(*pt)
        builder.close()
        path = builder.detach()

        outline_paint = skia.Paint()
        outline_paint.set_color(hex_to_argb_int(color))
        outline_paint.set_style(skia.Paint.Style.K_STROKE_STYLE)
        outline_paint.set_stroke_width(1.0)

        self.canvas.draw_path(path, outline_paint)

    def draw_solid_polygon(
        self, transform: box2d.Transform, vertices, radius: float, color: int
    ):
        # If you want, you can apply transform (px,py,c,s) to vertices here.
        # Box2D often provides local verts + transform; if your verts are already world-space, skip it.
        # For now, we just draw outline in world-space as given.

        self.canvas.save()

        self.canvas.translate(transform[0], transform[1])
        # self.canvas.rotate(transform[2])
        self.canvas.rotate(glm.degrees(transform[2]))

        self.draw_polygon(vertices, color)

        # Optional: visualize "radius" as stroke width
        # (This is NOT physically accurate; just helps you see rounded polygons.)
        if radius > 0 and vertices:
            builder = skia.PathBuilder()
            builder.move_to(*vertices[0])
            for pt in vertices[1:]:
                builder.line_to(*pt)
            builder.close()
            path = builder.detach()

            paint = skia.Paint()
            paint.set_color(hex_to_argb_int(color))
            paint.set_style(skia.Paint.Style.K_STROKE_STYLE)
            paint.set_stroke_width(max(1.0, radius * 2.0))
            self.canvas.draw_path(path, paint)

        self.canvas.restore()

    def draw_circle(self, center, radius: float, color: int):
        x, y = center
        paint = skia.Paint()
        paint.set_color(hex_to_argb_int(color))
        paint.set_style(skia.Paint.Style.K_STROKE_STYLE)
        paint.set_stroke_width(2.0)
        self.canvas.draw_circle(skia.Point(x, y), radius, paint)

    def draw_solid_circle(self, transform, radius: float, color: int):
        # C++ passes only transform + radius + color; center is transform.p
        x, y = transform_pos(transform)

        fill = skia.Paint()
        fill.set_color(hex_to_argb_int(color))
        # fill.set_color(rgba_tuple_to_argb_int(colors.RED))
        fill.set_style(skia.Paint.Style.K_FILL_STYLE)
        self.canvas.draw_circle(skia.Point(x, y), radius, fill)

        stroke = skia.Paint()
        stroke.set_color(hex_to_argb_int(color))
        # stroke.set_color(rgba_tuple_to_argb_int(colors.PINK))
        stroke.set_style(skia.Paint.Style.K_STROKE_STYLE)
        stroke.set_stroke_width(2.0)
        self.canvas.draw_circle(skia.Point(x, y), radius, stroke)

        # Optional: draw an orientation “radius line” using c/s
        try:
            _, _, c, s = transform
            x2 = x + c * radius
            y2 = y + s * radius
            self.draw_line((x, y), (x2, y2), color)
        except Exception:
            pass

    def draw_solid_capsule(self, p1, p2, radius: float, color: int):
        # A capsule is basically a fat segment + circles at endpoints.
        # Render as: thick line + endpoint circles.
        x1, y1 = p1
        x2, y2 = p2

        paint = skia.Paint()
        paint.set_color(hex_to_argb_int(color))
        paint.set_style(skia.Paint.Style.K_STROKE_STYLE)
        paint.set_stroke_width(max(1.0, radius * 2.0))
        paint.set_stroke_cap(
            skia.Paint.Cap.K_ROUND_CAP
        )  # if available in your skia binding
        self.canvas.draw_line(x1, y1, x2, y2, paint)

        # End caps (optional, since round cap already draws them)
        self.draw_circle(p1, radius, color)
        self.draw_circle(p2, radius, color)

    def draw_point(self, p, size: float, color: int):
        x, y = p
        paint = skia.Paint()
        paint.set_color(hex_to_argb_int(color))
        paint.set_style(skia.Paint.Style.K_FILL_STYLE)
        r = max(1.0, size * 0.5)
        self.canvas.draw_circle(skia.Point(x, y), r, paint)

    def draw_transform(self, transform):
        # Visualize transform axes at position, scaled by some constant.
        # transform: (px, py, c, s) where (c,s) is x-axis direction.
        x, y = transform_pos(transform)
        _, _, c, s = transform

        axis_len = 20.0
        # x-axis in red, y-axis in green (if you want strict, pick engine colors instead)
        self.draw_line((x, y), (x + c * axis_len, y + s * axis_len), 0xFF0000)
        self.draw_line((x, y), (x - s * axis_len, y + c * axis_len), 0x00FF00)

    def draw_string(self, p, s: str, color: int):
        # If your skia binding has text APIs, draw it. Otherwise log.
        # Many Skia wrappers need a Font object. If you have that, wire it in here.
        x, y = p
        try:
            paint = skia.Paint()
            paint.set_color(hex_to_argb_int(color))
            # TODO: replace with your skia text draw call
            # self.canvas.draw_string(s, x, y, font, paint)
            logger.debug(f"DebugDraw text @({x:.1f},{y:.1f}): {s}")
        except Exception:
            logger.debug(f"DebugDraw text @({x},{y}): {s}")
