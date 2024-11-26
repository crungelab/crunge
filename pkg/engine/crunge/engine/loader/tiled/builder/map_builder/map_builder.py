from pytmx import TiledMap, TiledTileLayer, TiledObjectGroup

from ..tile_layer_builder import TileLayerBuilder
from ..object_group_builder import ObjectGroupBuilder
from ..tiled_builder import TiledBuilder
from ..builder_context import BuilderContext

class MapBuilder(TiledBuilder):
    def __init__(self, context: BuilderContext, tile_layer_builder: TileLayerBuilder, object_group_builder: ObjectGroupBuilder):
        super().__init__(context)
        self.tile_layer_builder = tile_layer_builder
        self.object_group_builder = object_group_builder

    def build(self):
        for layer in self.map.visible_layers:
            if isinstance(layer, TiledTileLayer):
                self.tile_layer_builder.build(layer)
            elif isinstance(layer, TiledObjectGroup):
                self.object_group_builder.build(layer)
            else:
                raise ValueError(f"Unsupported layer type: {type(layer)}")
