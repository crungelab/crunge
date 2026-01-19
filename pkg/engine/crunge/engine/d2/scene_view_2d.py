from loguru import logger

from .scene_2d import Scene2D
from .view_2d import View2D
from .renderer import SceneRenderer2D

class SceneView2D(View2D):
    renderer: SceneRenderer2D

    def __init__(self, scene: Scene2D) -> None:
        super().__init__()
        self.scene = scene

    def create_renderer(self) -> None:
        self.renderer = SceneRenderer2D(self.scene, viewport=self.viewport, camera=self.camera)
    
    def _draw(self):
        self.renderer.render()

        with self.renderer.use():
            super()._draw()

    '''
    def _draw(self):
        with self.renderer.render_pass():
            self.scene.draw()

        with self.renderer.use():
            super()._draw()
    '''

    def update(self, dt: float) -> None:
        self.scene.update(dt)
        super().update(dt)
