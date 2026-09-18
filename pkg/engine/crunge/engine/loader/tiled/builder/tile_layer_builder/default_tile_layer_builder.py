from loguru import logger
from crunge import tmx

from crunge.engine.math import Bounds2
from crunge.engine.d2.sprite.sprite_render_layer import SpriteRenderLayer
from crunge.engine.d2.sprite.dynamic import DynamicSpriteGroup

from ..tile_builder import TileBuilder, DefaultTileBuilder

from .tile_layer_builder import TileLayerBuilder


class DefaultTileLayerBuilder(TileLayerBuilder):
    def __init__(self, tile_builder: TileBuilder = None):
        super().__init__(tile_builder if tile_builder is not None else DefaultTileBuilder())
        self.layer = None

    def build(self, tmx_layer: tmx.TileLayer):
        size = self.context.size
        sprite_group = DynamicSpriteGroup(1024).enable()
        self.layer = SpriteRenderLayer(name=tmx_layer.name, count=1024, sprite_group=sprite_group).enable()
        self.context.push_layer(self.layer)
        super().build(tmx_layer)
        self.build_runs(tmx_layer)
        self.build_terrain(tmx_layer)
        self.context.pop_layer()
        self.context.current_layer_group.add_layer(self.layer)

    def build_runs(self, tmx_layer: tmx.TileLayer):
        # Placeholder for run-building logic, if needed.
        pass

    def build_terrain(self, tmx_layer: tmx.TileLayer):
        # Placeholder for terrain-building logic, if needed.
        pass