from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .scene_3d import Scene3D

import glm

from ..math import Vector3, Point3
from ..node import Node
from .renderer_3d import Renderer3D
from .vu_3d import Vu3D

class Node3D(Node["Node3D", Vu3D, "Scene3D", Renderer3D]):
    def __init__(self, position = Point3()) -> None:
        super().__init__()
        self._position = position
        self._orientation = glm.quat(1.0, 0.0, 0.0, 0.0)
        self._scale = Vector3(1.0)
        self._matrix = glm.mat4(1.0)
        self.update_matrix()

    @property
    def position(self) -> glm.vec3:
        return self._position
    
    @position.setter
    def position(self, value: glm.vec3):
        self._position = value
        self.update_matrix()

    @property
    def orientation(self) -> glm.quat:
        return self._orientation
    
    @orientation.setter
    def orientation(self, value: glm.quat):
        self._orientation = value
        self.update_matrix()

    @property
    def scale(self) -> glm.vec3:
        return self._scale
    
    @scale.setter
    def scale(self, value: glm.vec3):
        self._scale = value
        self.update_matrix()

    @property
    def matrix(self) -> glm.mat4:
        return self._matrix
    
    @matrix.setter
    def matrix(self, value: glm.mat4):
        self._matrix = value

    def update_matrix(self):
        matrix = glm.mat4(1.0)
        matrix = glm.translate(matrix, glm.vec3(*self.position))
        matrix = matrix * glm.mat4_cast(self.orientation)
        matrix = glm.scale(matrix, glm.vec3(*self.scale))
        self.matrix = matrix
        
    @property
    def transform(self) -> glm.mat4:
        transform = self.matrix
        if self.parent:
            transform = self.parent.transform * transform
        return transform

        '''
        transform = glm.mat4(1.0)
        transform = glm.translate(transform, glm.vec3(*self.position))
        transform = transform * glm.mat4_cast(self.orientation)
        transform = glm.scale(transform, glm.vec3(*self.scale))
        transform = transform * self.matrix
        if self.parent:
            transform = self.parent.transform * transform
        return transform
        '''
