from typing import List

import glm

from crunge import wgpu
from .base import Base
from .camera import Camera
from .scene_renderer import SceneRenderer

class Node(Base):
    def __init__(self) -> None:
        super().__init__()
        self.children: List["Node"] = []
        self.translation = glm.vec3(0.0)
        self.rotation = glm.mat4(1.0)
        self.scale = glm.vec3(1.0)
        self.matrix = glm.mat4(1.0)
        self.transform = glm.mat4(1.0)

    def add_child(self, child):
        self.children.append(child)

    def draw(self, renderer: SceneRenderer):
        for child in self.children:
            child.draw(renderer)
