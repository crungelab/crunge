from dataclasses import dataclass

from glm import ivec2

from crunge.engine.viewport import Viewport
from crunge.engine.d2.renderer import Renderer2D
from crunge.engine.d2.camera_2d import Camera2D

from .compound_layer_2d import CompoundLayer2D, CompoundLayer2DMemo

class ParallaxLayer2D(CompoundLayer2D):
    def __init__(self, name: str, parallax_factor: float = 1.0):
        super().__init__(name)
        self.parallax_factor = parallax_factor

    @property
    def memo(self):
        current_viewport = Viewport.get_current()
        current_renderer = Renderer2D.get_current()
        if self._memo is None:
            camera = Camera2D(
                leader=current_renderer.camera_2d,
                parallax_factor=self.parallax_factor
            )
            renderer = Renderer2D(current_viewport, camera=camera, clear=False)
            self._memo = CompoundLayer2DMemo(camera=camera, renderer=renderer)
        return self._memo