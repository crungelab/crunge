from loguru import logger

from ..scene.scene_2d import Scene2D
from .screen_2d import Screen2D
from ..renderer import Renderer2D


class SceneScreen2D(Screen2D):
    renderer: Renderer2D

    def __init__(self, scene: Scene2D) -> None:
        super().__init__()
        self.scene = scene

    def update(self, dt: float) -> None:
        self.scene.update(dt)
        super().update(dt)
