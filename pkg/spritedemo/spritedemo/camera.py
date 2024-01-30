import time
import math

import glm

from loguru import logger

from .constants import *


class Camera:
    def __init__(
        self,
        width,
        height,
        position=glm.vec3(0.0, 0.0, 2),
    ):
        self.width = width
        self.height = height
        logger.debug(f"Camera: {width}x{height}")
        self.position = position
        self.zoom = 45.0

        viewport_width = self.width
        viewport_height = self.height
        logger.debug(f"Viewport: {viewport_width}x{viewport_height}")

        ortho_left = 0
        ortho_right = viewport_width
        ortho_bottom = 0
        ortho_top = viewport_height
        ortho_near = -1  # Near clipping plane
        ortho_far = 1    # Far clipping plane

        self.projection_matrix = glm.ortho(ortho_left, ortho_right, ortho_bottom, ortho_top, ortho_near, ortho_far)
        self.view_matrix = glm.mat4(1.0)

    @property
    def transform_matrix(self):
        return self.projection_matrix * self.view_matrix
