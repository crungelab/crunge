from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .scene import Scene

import glm

from .base import Base
from .scene_renderer import SceneRenderer


class Node(Base):
    def __init__(self) -> None:
        super().__init__()
        self.parent: "Node" = None
        self.scene: "Scene" = None
        self.children: List["Node"] = []
        self.translation = glm.vec3(0.0)
        #self.rotation = glm.mat4(1.0)
        self.rotation = glm.quat(1.0, 0.0, 0.0, 0.0)
        self.scale = glm.vec3(1.0)
        self.matrix = glm.mat4(1.0)
        #self.transform = glm.mat4(1.0)

    @property
    def transform(self):
        transform = glm.mat4(1.0)
        transform = transform * glm.mat4_cast(self.rotation)
        transform = glm.scale(transform, glm.vec3(*self.scale))
        transform = transform * self.matrix
        if self.parent:
            transform = self.parent.transform * transform
        return transform

    def add_child(self, child: "Node"):
        child.parent = self
        child.scene = self.scene
        self.children.append(child)

    def draw(self, renderer: SceneRenderer):
        for child in self.children:
            child.draw(renderer)
