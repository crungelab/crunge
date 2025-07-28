from loguru import logger
import glm
from pytmx import TiledTileLayer

from crunge.engine.math import Bounds2
from crunge.engine.d2.scene_layer_2d import SceneLayer2D
from crunge.engine.d2.sprite.instanced import InstancedSpriteLayer
from crunge.engine.d2.sprite.dynamic import DynamicSpriteGroup

from ..builder_context import BuilderContext
from ..tile_builder import TileBuilder, DefaultTileBuilder

from .tile_layer_builder import TileLayerBuilder


class DefaultTileLayerBuilder(TileLayerBuilder):
    def __init__(self, context: BuilderContext, tile_builder: TileBuilder = None):
        super().__init__(context, tile_builder if tile_builder is not None else DefaultTileBuilder(context))

    def build(self, layer: TiledTileLayer, layer_id: int):
        size = self.context.size
        #scene_layer = SceneLayer2D(name=layer.name)
        sprite_group = DynamicSpriteGroup(1024).enable()
        logger.debug(f"Sprite Group: {sprite_group}")
        scene_layer = InstancedSpriteLayer(name=layer.name, count=1024, sprite_group=sprite_group).enable()
        scene_layer.bounds = Bounds2(0, 0, size.x, size.y)
        self.context.layer = scene_layer
        super().build(layer, layer_id)
        self.context.scene.add_layer(self.context.layer)
