from loguru import logger
import pymunk
from pymunk.space_debug_draw_options import SpaceDebugDrawOptions

from crunge import skia

from ... import colors
from ...color import rgba_tuple_to_argb_int

from ...renderer import Renderer
from ...widget import Overlay

from . import globe


class SpaceDebugOverlay(Overlay, SpaceDebugDrawOptions):
    def __init__(self):
        super().__init__("space_debug", 700)
        SpaceDebugDrawOptions.__init__(self)
        self.visible = False
        self.shape_outline_color = colors.PURPLE
        self.constraint_color = colors.BLACK
        #self.collision_point_color = colors.BLACK
        self.collision_point_color = colors.RED
        self.body_outline_color = colors.BLACK
        self.body_line_color = colors.BLACK
        self.constraint_line_color = colors.BLACK
        #self.collision_point_outline_color = colors.BLACK
        self.collision_point_outline_color = colors.RED

        self.scale = 64.0  # pixels per unit
        self.outline_width_px = 1.0  # desired constant on-screen thickness
        self.contact_indicator_px = 4.0  # size of collision point indicators in pixels

    @property
    def canvas(self) -> skia.Canvas:
        renderer = Renderer.get_current()
        return renderer.canvas

    def _scaled_stroke_width(self) -> float:
        renderer = Renderer.get_current()
        #scale = renderer.camera_2d.ppu / renderer.camera_2d.zoom
        scale = self.scale
        return self.outline_width_px / scale

    def draw_circle(self, pos, angle, radius, outline_color, fill_color):
        # logger.debug(f"pos: {pos}, angle: {angle}, radius: {radius}, outline_color: {outline_color}, fill_color: {fill_color}")
        paint = skia.Paint()
        paint.set_color(rgba_tuple_to_argb_int(outline_color))
        paint.set_style(skia.Paint.Style.K_STROKE_STYLE)
        paint.set_stroke_width(self._scaled_stroke_width())  # Set the outline thickness as needed

        self.canvas.draw_circle(skia.Point(pos.x, pos.y), radius, paint)

    def draw_segment(self, a, b, color):
        paint = skia.Paint()
        paint.set_color(rgba_tuple_to_argb_int(color))

        if color == self.collision_point_color:
            # Chipmunk pads contact segments by a fixed 2-unit world-space offset
            # (see cpSpaceDebugDraw's `d = 2.0f`), sized for old pixel-scale worlds.
            # Clamp to a constant on-screen length instead of trusting raw endpoints.
            mid_x, mid_y = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            dx, dy = b[0] - a[0], b[1] - a[1]
            length = (dx * dx + dy * dy) ** 0.5
            if length > 0:
                scale = self.scale
                half_len = (self.contact_indicator_px / scale) / 2
                ux, uy = dx / length, dy / length
                a = (mid_x - ux * half_len, mid_y - uy * half_len)
                b = (mid_x + ux * half_len, mid_y + uy * half_len)

        self.canvas.draw_line(a[0], a[1], b[0], b[1], paint)

    '''
    def draw_segment(self, a, b, color):
        logger.debug(f"a: {a}, b: {b}, color: {color}")
        paint = skia.Paint()
        paint.set_color(rgba_tuple_to_argb_int(color))
        paint.set_stroke_width(self._scaled_stroke_width())  # Set the outline thickness as needed
        self.canvas.draw_line(a[0], a[1], b[0], b[1], paint)
    '''

    def draw_fat_segment(self, a, b, radius, outline_color, fill_color):
        logger.debug(
            f"a: {a}, b: {b}, radius: {radius}, outline_color: {outline_color}, fill_color: {fill_color}"
        )

    def draw_polygon(self, verts, radius, outline_color, fill_color):
        #logger.debug(f"verts: {verts}, radius: {radius}, outline_color: {outline_color}, fill_color: {fill_color}")
        if not verts:
            return

        builder = skia.PathBuilder()
        builder.move_to(*verts[0])
        for pt in verts[1:]:
            builder.line_to(*pt)
        builder.close()
        path = builder.detach()

        outline_paint = skia.Paint()
        outline_paint.set_color(rgba_tuple_to_argb_int(outline_color))
        outline_paint.set_style(skia.Paint.Style.K_STROKE_STYLE)
        #outline_paint.set_stroke_width(1.0)
        outline_paint.set_stroke_width(self._scaled_stroke_width())  # Set the outline thickness as needed

        self.canvas.draw_path(path, outline_paint)

    def draw_dot(self, size, pos, color):
        size = size / self.scale  # Convert size from pixels to world units
        #logger.debug(f"size: {size}, pos: {pos}, color: {color}")
        paint = skia.Paint()
        paint.set_color(rgba_tuple_to_argb_int(color))
        self.canvas.draw_circle(skia.Point(pos.x, pos.y), size, paint)


    def draw_shape(self, shape: pymunk.Shape) -> None:
        logger.debug(f"shape: {shape}")

    def draw_text(self, pos, text):
        logger.debug(f"pos: {pos}, text: {text}")

    def draw_transform(self, transform):
        logger.debug(f"transform: {transform}")

    def _draw(self):
        space = globe.physics_engine.space

        renderer = Renderer.get_current()
        self.scale = renderer.camera_2d.ppu / renderer.camera_2d.zoom

        with renderer.canvas_target() as canvas:
            canvas.save()

            canvas.translate(renderer.viewport.width // 2, renderer.viewport.height // 2)

            scale = self.scale
            canvas.scale(scale, -scale)

            camera_x, camera_y = (
                renderer.camera_2d.position.x,
                renderer.camera_2d.position.y,
            )
            canvas.translate(-camera_x, -camera_y)  # pan to camera

            space.debug_draw(self)

            canvas.restore()

        super()._draw()

    '''
    def _draw(self):
        space = globe.physics_engine.space

        renderer = Renderer.get_current()

        with renderer.canvas_target() as canvas:
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

        super()._draw()
    '''