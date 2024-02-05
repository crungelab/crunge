from typing import TYPE_CHECKING, Type, Dict, List, Any, Callable

if TYPE_CHECKING:
    from .scene import Scene

import glm

from crunge.engine import Vu

from .base import Base
from .scene_renderer import SceneRenderer


class Node(Base):
    def __init__(self, vu: Vu = None) -> None:
        super().__init__()
        self.vu = vu
        self.scene: "Scene" = None
        self.parent: "Node" = None
        self.children: List["Node"] = []

    def add_child(self, child: "Node"):
        child.parent = self
        child.scene = self.scene
        self.children.append(child)

    def draw(self, renderer: SceneRenderer):
        if self.vu is not None:
            self.vu.draw(renderer)
        for child in self.children:
            child.draw(renderer)

    def update(self, delta_time: float):
        for child in self.children:
            child.update(delta_time)