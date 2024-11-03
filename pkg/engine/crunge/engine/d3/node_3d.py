from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .scene_3d import Scene3D
    from .vu_3d import Vu3D

from loguru import logger
import glm

from ..math import Vector3, Point3, Bounds3
from ..scene_node import SceneNode
#from .vu_3d import Vu3D

class Node3D(SceneNode["Node3D", "Vu3D", "Scene3D"]):
    def __init__(self, position = Point3()) -> None:
        super().__init__()
        self.bounds = Bounds3()
        self._position = position
        self._orientation = glm.quat(1.0, 0.0, 0.0, 0.0)
        self._scale = Vector3(1.0)
        self._matrix = glm.mat4(1.0)
        self._transform = glm.mat4(1.0)
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
        self.update_transform()

    @property
    def transform(self) -> glm.mat4:
        return self._transform
    
    @transform.setter
    def transform(self, value: glm.mat4):
        self._transform = value
        self.on_transform()

    def on_attached(self):
        self.parent.update_global_bounds()
        super().on_attached()

    def on_transform(self):
        self.update_bounds()
        self.gpu_update_model()

        for listener in self.listeners:
            listener.on_node_transform(self)

    def gpu_update_model(self):
        pass

    def on_attached(self):
        self.update_transform()
        self.update_bounds()
        self.parent.update_bounds()

    def update_matrix(self):
        matrix = glm.mat4(1.0)
        matrix = glm.translate(matrix, glm.vec3(*self.position))
        matrix = matrix * glm.mat4_cast(self.orientation)
        matrix = glm.scale(matrix, glm.vec3(*self.scale))
        self.matrix = matrix

    def update_transform(self):
        transform = self.matrix
        if self.parent:
            transform = self.parent.transform * transform
        self.transform = transform
        for child in self.children:
            child.update_transform()

    def update_bounds(self):
        for child in self.children:
            self.bounds.merge(child.bounds)
        #logger.debug(f"{self.__class__.__name__} bounds: {self.bounds}")
