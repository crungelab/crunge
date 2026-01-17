from loguru import logger
import pymunk
from pymunk.space_debug_draw_options import SpaceDebugDrawOptions

from crunge import skia

from ... import colors
from ...color import rgba_tuple_to_argb_int

from ...renderer import Renderer
from ...view.overlay import Overlay

from . import globe


class SpaceDebugOverlay(Overlay, SpaceDebugDrawOptions):
    def __init__(self):
        super().__init__("space_debug", 700)
        SpaceDebugDrawOptions.__init__(self)
        self.visible = False

        self.canvas: skia.SkiaCanvas = None

        # self.flags = SpaceDebugDrawOptions.DRAW_SHAPES

        self.shape_outline_color = colors.PURPLE
        self.constraint_color = colors.BLACK
        self.collision_point_color = colors.BLACK
        self.body_outline_color = colors.BLACK
        self.body_line_color = colors.BLACK
        self.constraint_line_color = colors.BLACK
        self.collision_point_outline_color = colors.BLACK

    def draw_circle(self, pos, angle, radius, outline_color, fill_color):
        # logger.debug(f"pos: {pos}, angle: {angle}, radius: {radius}, outline_color: {outline_color}, fill_color: {fill_color}")
        paint = skia.Paint()
        paint.set_color(rgba_tuple_to_argb_int(outline_color))
        paint.set_style(skia.Paint.Style.K_STROKE_STYLE)
        paint.set_stroke_width(2)  # Set the outline thickness as needed
        self.canvas.draw_circle(skia.Point(pos.x, pos.y), radius, paint)

    def draw_segment(self, a, b, color):
        paint = skia.Paint()
        paint.set_color(rgba_tuple_to_argb_int(color))
        self.canvas.draw_line(a[0], a[1], b[0], b[1], paint)

    def draw_fat_segment(self, a, b, radius, outline_color, fill_color):
        logger.debug(
            f"a: {a}, b: {b}, radius: {radius}, outline_color: {outline_color}, fill_color: {fill_color}"
        )

    def draw_polygon(self, verts, radius, outline_color, fill_color):
        # logger.debug(f"verts: {verts}, radius: {radius}, outline_color: {outline_color}, fill_color: {fill_color}")
        path = skia.Path()
        if not verts:
            return
        path.move_to(*verts[0])
        for pt in verts[1:]:
            path.line_to(*pt)
        path.close()

        outline_paint = skia.Paint()
        outline_paint.set_color(rgba_tuple_to_argb_int(outline_color))
        outline_paint.set_style(skia.Paint.Style.K_STROKE_STYLE)
        outline_paint.set_stroke_width(1.0)

        self.canvas.draw_path(path, outline_paint)

    def draw_dot(self, size, pos, color):
        logger.debug(f"size: {size}, pos: {pos}, color: {color}")

    def draw_shape(self, shape: pymunk.Shape) -> None:
        logger.debug(f"shape: {shape}")

    def draw_text(self, pos, text):
        logger.debug(f"pos: {pos}, text: {text}")

    def draw_transform(self, transform):
        logger.debug(f"transform: {transform}")

    def _draw(self):
        space = globe.physics_engine.space

        renderer = Renderer.get_current()

        canvas = renderer.canvas
        self.canvas = canvas

        canvas.save()

        canvas.translate(renderer.viewport.width // 2, renderer.viewport.height // 2)
        scale = 1 / renderer.camera_2d.zoom
        canvas.scale(scale, -scale)  # Invert Y-axis for Skia
        camera_x, camera_y = (
            renderer.camera_2d.position.x,
            renderer.camera_2d.position.y,
        )
        canvas.translate(-camera_x, -camera_y)  # pan to camera

        space.debug_draw(self)

        canvas.restore()

        self.canvas = None

        super()._draw()
