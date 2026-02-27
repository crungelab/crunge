from __future__ import annotations

from loguru import logger
import glm

from crunge import box2d
from crunge import skia

from crunge.engine import colors
from crunge.engine.color import rgba_tuple_to_argb_int


def hex_to_rgba_tuple(rgb: int, a: int = 255) -> tuple[int, int, int, int]:
    """
    Convert 0xRRGGBB (Box2D b2HexColor) -> (r,g,b,a).
    If your b2HexColor is different (e.g. ABGR), swap channels here.
    """
    r = (rgb >> 16) & 0xFF
    g = (rgb >> 8) & 0xFF
    b = (rgb >> 0) & 0xFF
    return (r, g, b, a)


def transform_pos(transform: tuple[float, float, float, float]) -> tuple[float, float]:
    """(px, py, c, s) -> (px, py)"""
    return (transform[0], transform[1])


class DebugDraw(box2d.DebugDrawBase):
    """
    Engine-facing debug drawer.

    C++ calls into these methods with:
      - points as (x, y)
      - transform as (px, py, c, s)
      - color as 0xRRGGBB int
    """

    def __init__(self):
        super().__init__()  # IMPORTANT: sets up C++ context + cache
        self.canvas: skia.SkiaCanvas = None

        # Use the new C++ exposed properties/flags if you bound them
        # (from the full file: draw_shapes/draw_joints/force_scale/joint_scale)
        self.draw_shapes = True
        self.draw_joints = True
        self.force_scale = 1.0
        self.joint_scale = 1.0

        # Your engine palette (RGBA tuples)
        self.shape_outline_color = colors.PURPLE

        # These were in your old version but rely on SpaceDebugColor etc.
        # Keep if you still use them elsewhere; they are not used by the new callbacks.
        # self.constraint_color = ...
        # ...

    # ------------- Box2D -> Skia primitive callbacks -------------

    def draw_line(self, p1, p2, color: int):
        (x1, y1) = p1
        (x2, y2) = p2
        paint = skia.Paint()
        paint.set_color(rgba_tuple_to_argb_int(hex_to_rgba_tuple(color)))
        paint.set_style(skia.Paint.Style.K_STROKE_STYLE)
        paint.set_stroke_width(1.0)
        self.canvas.draw_line(x1, y1, x2, y2, paint)

    def draw_polygon(self, vertices, color: int):
        # vertices: list[(x,y), ...]
        if not vertices:
            return

        path = skia.Path()
        path.move_to(*vertices[0])
        for pt in vertices[1:]:
            path.line_to(*pt)
        path.close()

        outline_paint = skia.Paint()
        #outline_paint.set_color(rgba_tuple_to_argb_int(hex_to_rgba_tuple(color)))
        outline_paint.set_color(rgba_tuple_to_argb_int(colors.GREEN))
        outline_paint.set_style(skia.Paint.Style.K_STROKE_STYLE)
        outline_paint.set_stroke_width(1.0)

        self.canvas.draw_path(path, outline_paint)

        """
        // 1. Save the current state (identity matrix)
        canvas->save(); 

            // 2. Move and rotate the drawing surface
            canvas->translate(50, 50);
            canvas->rotate(30);

            // 3. Draw the path at "local" coordinates (0,0)
            canvas->drawPath(path, paint); 

        // 4. Restore to the state before the translate/rotate
        canvas->restore();
        """

    def draw_solid_polygon(self, transform: box2d.Transform, vertices, radius: float, color: int):
        # If you want, you can apply transform (px,py,c,s) to vertices here.
        # Box2D often provides local verts + transform; if your verts are already world-space, skip it.
        # For now, we just draw outline in world-space as given.

        self.canvas.save()

        self.canvas.translate(transform[0], transform[1])
        #self.canvas.rotate(transform[2])
        self.canvas.rotate(glm.degrees(transform[2]))

        self.draw_polygon(vertices, color)

        # Optional: visualize "radius" as stroke width
        # (This is NOT physically accurate; just helps you see rounded polygons.)
        if radius > 0 and vertices:
            path = skia.Path()
            path.move_to(*vertices[0])
            for pt in vertices[1:]:
                path.line_to(*pt)
            path.close()

            paint = skia.Paint()
            #paint.set_color(rgba_tuple_to_argb_int(hex_to_rgba_tuple(color, 128)))
            paint.set_color(rgba_tuple_to_argb_int(colors.PURPLE))
            paint.set_style(skia.Paint.Style.K_STROKE_STYLE)
            paint.set_stroke_width(max(1.0, radius * 2.0))
            self.canvas.draw_path(path, paint)

        self.canvas.restore()

    """
    def draw_solid_polygon(self, transform, vertices, radius: float, color: int):
        # If you want, you can apply transform (px,py,c,s) to vertices here.
        # Box2D often provides local verts + transform; if your verts are already world-space, skip it.
        # For now, we just draw outline in world-space as given.
        self.draw_polygon(vertices, color)

        # Optional: visualize "radius" as stroke width
        # (This is NOT physically accurate; just helps you see rounded polygons.)
        if radius > 0 and vertices:
            path = skia.Path()
            path.move_to(*vertices[0])
            for pt in vertices[1:]:
                path.line_to(*pt)
            path.close()

            paint = skia.Paint()
            #paint.set_color(rgba_tuple_to_argb_int(hex_to_rgba_tuple(color, 128)))
            paint.set_color(rgba_tuple_to_argb_int(colors.PURPLE))
            paint.set_style(skia.Paint.Style.K_STROKE_STYLE)
            paint.set_stroke_width(max(1.0, radius * 2.0))
            self.canvas.draw_path(path, paint)
    """

    def draw_circle(self, center, radius: float, color: int):
        (x, y) = center
        paint = skia.Paint()
        paint.set_color(rgba_tuple_to_argb_int(hex_to_rgba_tuple(color)))
        paint.set_style(skia.Paint.Style.K_STROKE_STYLE)
        paint.set_stroke_width(2.0)
        self.canvas.draw_circle(skia.Point(x, y), radius, paint)

    def draw_solid_circle(self, transform, radius: float, color: int):
        # C++ passes only transform + radius + color; center is transform.p
        (x, y) = transform_pos(transform)

        fill = skia.Paint()
        #fill.set_color(rgba_tuple_to_argb_int(hex_to_rgba_tuple(color, 64)))
        fill.set_color(rgba_tuple_to_argb_int(colors.RED))
        fill.set_style(skia.Paint.Style.K_FILL_STYLE)
        self.canvas.draw_circle(skia.Point(x, y), radius, fill)

        stroke = skia.Paint()
        #stroke.set_color(rgba_tuple_to_argb_int(hex_to_rgba_tuple(color, 255)))
        stroke.set_color(rgba_tuple_to_argb_int(colors.PINK))
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
        (x1, y1) = p1
        (x2, y2) = p2

        paint = skia.Paint()
        paint.set_color(rgba_tuple_to_argb_int(hex_to_rgba_tuple(color, 128)))
        paint.set_style(skia.Paint.Style.K_STROKE_STYLE)
        paint.set_stroke_width(max(1.0, radius * 2.0))
        paint.set_stroke_cap(skia.Paint.Cap.K_ROUND_CAP)  # if available in your skia binding
        self.canvas.draw_line(x1, y1, x2, y2, paint)

        # End caps (optional, since round cap already draws them)
        self.draw_circle(p1, radius, color)
        self.draw_circle(p2, radius, color)

    def draw_point(self, p, size: float, color: int):
        (x, y) = p
        paint = skia.Paint()
        paint.set_color(rgba_tuple_to_argb_int(hex_to_rgba_tuple(color)))
        paint.set_style(skia.Paint.Style.K_FILL_STYLE)
        r = max(1.0, size * 0.5)
        self.canvas.draw_circle(skia.Point(x, y), r, paint)

    def draw_transform(self, transform):
        # Visualize transform axes at position, scaled by some constant.
        # transform: (px, py, c, s) where (c,s) is x-axis direction.
        (x, y) = transform_pos(transform)
        _, _, c, s = transform

        axis_len = 20.0
        # x-axis in red, y-axis in green (if you want strict, pick engine colors instead)
        self.draw_line((x, y), (x + c * axis_len, y + s * axis_len), 0xFF0000)
        self.draw_line((x, y), (x - s * axis_len, y + c * axis_len), 0x00FF00)

    def draw_string(self, p, s: str, color: int):
        # If your skia binding has text APIs, draw it. Otherwise log.
        # Many Skia wrappers need a Font object. If you have that, wire it in here.
        (x, y) = p
        try:
            paint = skia.Paint()
            paint.set_color(rgba_tuple_to_argb_int(hex_to_rgba_tuple(color)))
            # TODO: replace with your skia text draw call
            # self.canvas.draw_string(s, x, y, font, paint)
            logger.debug(f"DebugDraw text @({x:.1f},{y:.1f}): {s}")
        except Exception:
            logger.debug(f"DebugDraw text @({x},{y}): {s}")