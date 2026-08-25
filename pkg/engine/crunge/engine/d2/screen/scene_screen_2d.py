from loguru import logger

from ..scene.scene_2d import Scene2D
from .screen_2d import Screen2D
from ..renderer import Renderer2D
from ..view.scene_view_2d import SceneView2D


class SceneScreen2D(Screen2D):
    renderer: Renderer2D

    def __init__(self, scene: Scene2D, name: str = "SceneScreen2D", title: str = "Scene Screen 2D") -> None:
        super().__init__(name=name, title=title)
        self.scene = scene

    def create_children(self):
        logger.debug("Creating screen children")
        self.view = SceneView2D(self.scene)
        self.add_child(self.view)

    def update(self, dt: float) -> None:
        self.scene.update(dt)
        super().update(dt)
