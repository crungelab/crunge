from loguru import logger

from ..scene import Scene3D
from .screen_3d import Screen3D
from ..renderer import Renderer3D
from ..view import SceneView3D


class SceneScreen3D(Screen3D):
    renderer: Renderer3D

    def __init__(self, scene: Scene3D, name: str = "SceneScreen3D", title: str = "Scene Screen 3D") -> None:
        super().__init__(name=name, title=title)
        self.scene = scene

    def create_children(self):
        logger.debug("Creating screen children")
        self.view = SceneView3D(self.scene)
        self.add_child(self.view)

    def update(self, dt: float) -> None:
        self.scene.update(dt)
        super().update(dt)
