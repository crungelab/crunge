import glm
from pytmx import TiledTileLayer

from crunge.engine.d2.scene_layer_2d import SceneLayer2D

from ..builder_context import BuilderContext
from ..tile_builder import TileBuilder, DefaultTileBuilder

from .tile_layer_builder import TileLayerBuilder


class DefaultTileLayerBuilder(TileLayerBuilder):
    def __init__(self, context: BuilderContext, tile_builder: TileBuilder = None):
        super().__init__(context, tile_builder if tile_builder is not None else DefaultTileBuilder(context))

    def build(self, layer: TiledTileLayer, layer_id: int):
        self.context.layer = SceneLayer2D(name=layer.name, size=glm.vec2(layer.width, layer.height))
        super().build(layer, layer_id)
        self.context.scene.add_layer(self.context.layer)
