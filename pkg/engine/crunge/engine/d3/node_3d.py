from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .scene_3d import Scene3D

import glm

from ..node import Node
from .renderer_3d import Renderer3D
from .vu_3d import Vu3D

class Node3D(Node["Node3D", Vu3D, "Scene3D", Renderer3D]):
    def __init__(self, translation = glm.vec3()) -> None:
        super().__init__()
        self.translation = translation
        self.rotation = glm.quat(1.0, 0.0, 0.0, 0.0)
        self.scale = glm.vec3(1.0)
        self.matrix = glm.mat4(1.0)
        #self.transform = glm.mat4(1.0)

    @property
    def transform(self):
        transform = glm.mat4(1.0)
        transform = glm.translate(transform, glm.vec3(*self.translation))
        transform = transform * glm.mat4_cast(self.rotation)
        transform = glm.scale(transform, glm.vec3(*self.scale))
        transform = transform * self.matrix
        if self.parent:
            transform = self.parent.transform * transform
        return transform
