from dataclasses import dataclass

import glm

from crunge.engine.viewport import Viewport
from crunge.engine.d2.renderer import Renderer2D
from crunge.engine.d2.camera_2d import Camera2D

from crunge.engine.scene.layer.layer_group import LayerGroup

@dataclass
class ParallaxLayer2DMemo:
    camera: Camera2D


class ParallaxLayer2D(LayerGroup):
    def __init__(self, name: str, parallax_factor=glm.vec2(1.0, 1.0), parallax_origin=glm.vec2(0.0, 0.0)):
        super().__init__(name)
        self._memo = None
        self.parallax_factor = parallax_factor
        self.parallax_origin = parallax_origin

    @property
    def memo(self):
        current_viewport = Viewport.get_current()
        current_renderer = Renderer2D.get_current()
        if self._memo is None:
            camera = Camera2D(
                leader=current_renderer.camera_2d,
                parallax_factor=self.parallax_factor,
                parallax_origin=self.parallax_origin
            )
            camera.viewport = current_viewport
            camera.enable()
            self._memo = ParallaxLayer2DMemo(camera=camera)
        return self._memo
    
    def _render(self):
        with self.memo.camera.use():
            super()._render()
