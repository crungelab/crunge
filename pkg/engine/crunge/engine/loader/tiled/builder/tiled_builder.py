import glm

from crunge import tmx

from crunge.engine.scene.layer.scene_layer import SceneLayer
from crunge.engine.d2.scene.layer.parallax_layer_2d import ParallaxLayer2D

from .builder_context import BuilderContext

class TiledBuilder:
    def __init__(self):
        pass

    @property
    def context(self):
        return BuilderContext.get_current()

    @property
    def map(self):
        return self.context.map
    
    def maybe_wrap(self, tmx_layer: tmx.Layer, layer: SceneLayer):
        tmx_parallax_factor = tmx_layer.get_parallax_factor()
        parallax_factor = glm.vec2(tmx_parallax_factor.x, tmx_parallax_factor.y)

        tmx_parallax_origin = self.map.get_parallax_origin()
        parallax_origin = glm.vec2(tmx_parallax_origin.x, tmx_parallax_origin.y)

        if parallax_factor.x != 1.0 or parallax_factor.y != 1.0:
            group = ParallaxLayer2D(layer.name, parallax_factor=parallax_factor, parallax_origin=parallax_origin)
            group.add_layer(layer)
            return group
        return layer
