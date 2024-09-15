import time
import math

import glm

from loguru import logger

from .node_2d import Node2D
from ..math.rect import RectF


class Camera2D(Node2D):
    def __init__(
        self,
        position=glm.vec3(0.0, 0.0, 2),
        size=glm.vec2(1.0),
    ):
        self._zoom = 1.0
        super().__init__(position, size)

    @property
    def zoom(self):
        return self._zoom
    
    @zoom.setter
    def zoom(self, value: float):
        self._zoom = value
        #self.update_matrices()
        self.update_transform()

    def resize(self, size: glm.ivec2) -> None:
        self.size = glm.vec2(size)
        self.update_transform()

    def update_transform(self):
        super().update_transform()
        ortho_left = (self.x - (self.width / self.zoom) / 2)
        ortho_right = (self.x + (self.width / self.zoom) / 2)
        ortho_bottom = (self.y - (self.height / self.zoom) / 2)
        ortho_top = (self.y + (self.height / self.zoom) / 2)

        self.frustrum = RectF(ortho_left, ortho_bottom, ortho_right - ortho_left, ortho_top - ortho_bottom)

        ortho_near = -1  # Near clipping plane
        ortho_far = 1    # Far clipping plane

        self.projection_matrix = glm.ortho(ortho_left, ortho_right, ortho_bottom, ortho_top, ortho_near, ortho_far)
        self.view_matrix = glm.mat4(1.0)
        #logger.debug(f"Camera2D: {self.position}, {self.width}x{self.height}")


    @property
    def transform_matrix(self):
        return self.projection_matrix * self.view_matrix
