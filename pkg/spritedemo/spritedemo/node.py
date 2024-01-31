from typing import List

import glm

from .base import Base
from .scene_renderer import SceneRenderer

class Node(Base):
    def __init__(self) -> None:
        super().__init__()
        self.children: List["Node"] = []
        self.transform = glm.mat4(1.0)

    def add_child(self, child):
        self.children.append(child)

    def draw(self, renderer: SceneRenderer):
        for child in self.children:
            child.draw(renderer)
