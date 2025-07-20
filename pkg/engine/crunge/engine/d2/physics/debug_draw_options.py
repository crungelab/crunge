from loguru import logger

import pymunk
from pymunk.space_debug_draw_options import SpaceDebugColor

from crunge import skia

from ... import colors
from ...color import rgba_tuple_to_argb_int


class DebugDrawOptions(pymunk.SpaceDebugDrawOptions):
    def __init__(self, canvas: skia.SkiaCanvas):
        super().__init__()
        self.canvas = canvas

        self.flags = pymunk.SpaceDebugDrawOptions.DRAW_SHAPES
        #self.shape_outline_color = SpaceDebugColor(255, 0, 255, 255)
        self.shape_outline_color = colors.PURPLE
        self.constraint_color = SpaceDebugColor(0, 0, 0, 255)
        self.collision_point_color = SpaceDebugColor(0, 0, 0, 255)
        self.body_outline_color = SpaceDebugColor(0, 0, 0, 255)
        self.body_line_color = SpaceDebugColor(0, 0, 0, 255)
        self.constraint_line_color = SpaceDebugColor(0, 0, 0, 255)
        self.collision_point_outline_color = SpaceDebugColor(0, 0, 0, 255)
        self.data = None

    def draw_circle(self, pos, angle, radius, outline_color, fill_color):
        #pass
        #logger.debug(f"pos: {pos}, angle: {angle}, radius: {radius}, outline_color: {outline_color}, fill_color: {fill_color}")
        #self.scratch.draw_circle(pos, radius, outline_color, fill_color)
        #self.scratch.draw_circle(pos, radius, color=outline_color)
        paint = skia.Paint()
        paint.set_color(rgba_tuple_to_argb_int(outline_color))
        paint.set_style(skia.Paint.Style.K_STROKE_STYLE)
        paint.set_stroke_width(2)  # Set the outline thickness as needed
        self.canvas.draw_circle(skia.Point(pos.x, pos.y), radius, paint)


    def draw_segment(self, a, b, color):
        #self.scratch.draw_line(a, b, color)
        paint = skia.Paint()
        paint.set_color(rgba_tuple_to_argb_int(color))
        self.canvas.draw_line(a[0], a[1], b[0], b[1], paint)


    def draw_fat_segment(self, a, b, radius, outline_color, fill_color):
        #pass
        logger.debug(f"a: {a}, b: {b}, radius: {radius}, outline_color: {outline_color}, fill_color: {fill_color}")

    def draw_polygon(self, verts, radius, outline_color, fill_color):
        #pass
        #logger.debug(f"verts: {verts}, radius: {radius}, outline_color: {outline_color}, fill_color: {fill_color}")
        #self.scratch.draw_polygon(verts, outline_color, fill_color)
        '''
        for i in range(len(verts) - 1):
            self.draw_segment(verts[i], verts[i + 1], outline_color)
        '''
        #self.scratch.draw_polygon(verts, outline_color)
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
        #pass
        logger.debug(f"size: {size}, pos: {pos}, color: {color}")

    def draw_shape(self, shape: pymunk.Shape) -> None:
        logger.debug(f"shape: {shape}")

    def draw_text(self, pos, text):
        #pass
        logger.debug(f"pos: {pos}, text: {text}")

    def draw_transform(self, transform):
        #pass
        logger.debug(f"transform: {transform}")

