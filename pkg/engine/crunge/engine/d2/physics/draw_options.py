from loguru import logger

import glm

import pymunk
from pymunk.space_debug_draw_options import SpaceDebugColor
from pymunk.vec2d import Vec2d

from crunge.engine.d2.scratch_layer import ScratchLayer

class DrawOptions(pymunk.SpaceDebugDrawOptions):
    def __init__(self, scratch: ScratchLayer):
        super().__init__()
        self.scratch = scratch
        self.flags = pymunk.SpaceDebugDrawOptions.DRAW_SHAPES
        self.shape_outline_color = SpaceDebugColor(1, 0, 1, 255)
        self.constraint_color = SpaceDebugColor(0, 0, 0, 255)
        self.collision_point_color = SpaceDebugColor(0, 0, 0, 255)
        self.body_outline_color = SpaceDebugColor(0, 0, 0, 255)
        self.body_line_color = SpaceDebugColor(0, 0, 0, 255)
        self.constraint_line_color = SpaceDebugColor(0, 0, 0, 255)
        self.collision_point_outline_color = SpaceDebugColor(0, 0, 0, 255)
        self.data = None

    def draw_circle(self, pos, angle, radius, outline_color, fill_color):
        #pass
        logger.debug(f"pos: {pos}, angle: {angle}, radius: {radius}, outline_color: {outline_color}, fill_color: {fill_color}")

    def draw_segment(self, a, b, color):
        self.scratch.draw_line(a, b, color)

    def draw_fat_segment(self, a, b, radius, outline_color, fill_color):
        #pass
        logger.debug(f"a: {a}, b: {b}, radius: {radius}, outline_color: {outline_color}, fill_color: {fill_color}")

    def draw_dot(self, size, pos, color):
        #pass
        logger.debug(f"size: {size}, pos: {pos}, color: {color}")

    def draw_polygon(self, verts, radius, outline_color, fill_color):
        #pass
        #logger.debug(f"verts: {verts}, radius: {radius}, outline_color: {outline_color}, fill_color: {fill_color}")
        #self.scratch.draw_polygon(verts, outline_color, fill_color)
        '''
        for i in range(len(verts) - 1):
            self.draw_segment(verts[i], verts[i + 1], outline_color)
        '''
        outline_color = glm.vec4(outline_color.r, outline_color.g, outline_color.b, outline_color.a)
        self.scratch.draw_polygon(verts, outline_color)
        #self.scratch.draw_line(verts[-1], verts[0], outline_color)

    def draw_dot(self, size, pos, color):
        #pass
        logger.debug(f"size: {size}, pos: {pos}, color: {color}")

    def draw_text(self, pos, text):
        #pass
        logger.debug(f"pos: {pos}, text: {text}")

    def draw_transform(self, transform):
        #pass
        logger.debug(f"transform: {transform}")

