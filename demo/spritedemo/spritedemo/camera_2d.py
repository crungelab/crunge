import time
import math

import glm

from loguru import logger

from .constants import *
from .node_2d import Node2D

class Camera2D(Node2D):
    def __init__(
        self,
        position=glm.vec3(0.0, 0.0, 2),
        size=glm.vec2(1.0),
    ):
        super().__init__(position, size)
        self._zoom = 1.0
        self.update_matrices()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value: glm.vec2):
        self._position = value
        self.update_matrices()

    @property
    def zoom(self):
        return self._zoom
    
    @zoom.setter
    def zoom(self, value: float):
        self._zoom = value
        self.update_matrices()

    def update_matrices(self):
        ortho_left = (self.x - (self.width / self.zoom) / 2)
        ortho_right = (self.x + (self.width / self.zoom) / 2)
        ortho_bottom = (self.y - (self.height / self.zoom) / 2)
        ortho_top = (self.y + (self.height / self.zoom) / 2)

        ortho_near = -1  # Near clipping plane
        ortho_far = 1    # Far clipping plane

        self.projection_matrix = glm.ortho(ortho_left, ortho_right, ortho_bottom, ortho_top, ortho_near, ortho_far)
        self.view_matrix = glm.mat4(1.0)
        #logger.debug(f"Camera2D: {self.position}, {self.width}x{self.height}")


    @property
    def transform_matrix(self):
        return self.projection_matrix * self.view_matrix
