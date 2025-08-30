from loguru import logger

import pymunk
from pymunk.space_debug_draw_options import SpaceDebugColor

from ... import colors
from crunge.engine.d2.scratch_layer import ScratchLayer

class DrawOptions(pymunk.SpaceDebugDrawOptions):
    def __init__(self, scratch: ScratchLayer):
        super().__init__()
        self.scratch = scratch
        #self.flags = pymunk.SpaceDebugDrawOptions.DRAW_SHAPES
        self.shape_outline_color = colors.PURPLE
        self.constraint_color = colors.BLACK
        self.collision_point_color = colors.BLACK
        self.body_outline_color = colors.BLACK
        self.body_line_color = colors.BLACK
        self.constraint_line_color = colors.BLACK
        self.collision_point_outline_color = colors.BLACK
        self.shape_sleeping_color = colors.BLUE
        self.shape_static_color = colors.GREEN
        self.shape_kinematic_color = colors.YELLOW

    def draw_circle(self, pos, angle, radius, outline_color, fill_color):
        #pass
        #logger.debug(f"pos: {pos}, angle: {angle}, radius: {radius}, outline_color: {outline_color}, fill_color: {fill_color}")
        #self.scratch.draw_circle(pos, radius, outline_color, fill_color)
        self.scratch.draw_circle(pos, radius, color=outline_color)

    def draw_segment(self, a, b, color):
        self.scratch.draw_line(a, b, color)

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
        self.scratch.draw_polygon(verts, outline_color)
        #self.scratch.draw_line(verts[-1], verts[0], outline_color)

    def draw_dot(self, size, pos, color):
        #pass
        #logger.debug(f"size: {size}, pos: {pos}, color: {color}")
        self.scratch.draw_dot(size, pos, color)

    def draw_shape(self, shape: pymunk.Shape) -> None:
        logger.debug(f"shape: {shape}")

    def draw_text(self, pos, text):
        #pass
        logger.debug(f"pos: {pos}, text: {text}")

    def draw_transform(self, transform):
        #pass
        logger.debug(f"transform: {transform}")

