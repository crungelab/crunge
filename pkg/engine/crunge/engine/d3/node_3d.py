from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .scene_3d import Scene3D

import glm

from crunge.engine.base import Base
from .renderer_3d import Renderer3D


class Node3D(Base):
    def __init__(self) -> None:
        super().__init__()
        self.parent: "Node3D" = None
        self.scene: "Scene3D" = None
        self.children: List["Node3D"] = []
        self.translation = glm.vec3(0.0)
        #self.rotation = glm.mat4(1.0)
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

    def attach(self, child: "Node3D"):
        child.parent = self
        child.scene = self.scene
        self.children.append(child)
        child.on_attached()

    def on_attached(self):
        pass

    def detach(self, child: "Node3D"):
        self.children.remove(child)
        child.on_detached()

    def on_detached(self):
        pass

    def draw(self, renderer: Renderer3D):
        for child in self.children:
            child.draw(renderer)
