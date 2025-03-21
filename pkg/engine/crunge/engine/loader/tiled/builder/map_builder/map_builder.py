from typing import List, Dict

from loguru import logger
from pytmx import TiledTileLayer, TiledObjectGroup, TiledElement

from ..tiled_builder import TiledBuilder
from ..builder_context import BuilderContext
from ..tile_layer_builder import TileLayerBuilder
from ..object_group_builder import ObjectGroupBuilder

class MapBuilder(TiledBuilder):
    def __init__(self, context: BuilderContext, tile_layer_builder: TileLayerBuilder, object_group_builder: ObjectGroupBuilder):
        super().__init__(context)
        self.tile_layer_builder = tile_layer_builder
        self.object_group_builder = object_group_builder
        self.tile_layer_builders: Dict[str, TileLayerBuilder] = {}
        self.object_group_builders: Dict[str, ObjectGroupBuilder] = {}

    def add_tile_layer_builder(self, name: str, builder: TileLayerBuilder):
        self.tile_layer_builders[name] = builder

    def add_object_group_builder(self, name: str, builder: ObjectGroupBuilder):
        self.object_group_builders[name] = builder

    def add_tile_layer_builders(self, builders: Dict[str, TileLayerBuilder]):
        self.tile_layer_builders.update(builders)

    def add_object_group_builders(self, builders: Dict[str, ObjectGroupBuilder]):
        self.object_group_builders.update(builders)

    '''
    def build(self):
        layers = list(self.map.visible_layers)
        reversed_layers = reversed(layers)
        for layer_id, layer in enumerate(reversed_layers):
            layer_id = len(layers) - layer_id - 1
            self.build_layer(layer, layer_id)
    '''

    def build(self):
        for layer_id, layer in enumerate(self.map.visible_layers):
            logger.debug(f"layer: {layer}")
            self.build_layer(layer, layer_id)
    
    def build_layer(self, layer: TiledElement, layer_id: int):
        if isinstance(layer, TiledTileLayer):
            self.build_tile_layer(layer, layer_id)
        elif isinstance(layer, TiledObjectGroup):
            self.build_object_group(layer)
        else:
            raise ValueError(f"Unsupported element type: {type(layer)}")

    def build_tile_layer(self, layer: TiledTileLayer, layer_id: int):
        if layer.name in self.tile_layer_builders:
            self.tile_layer_builders[layer.name].build(layer, layer_id)
        else:
            self.tile_layer_builder.build(layer, layer_id)

    def build_object_group(self, group: TiledObjectGroup):
        if group.name in self.object_group_builders:
            self.object_group_builders[group.name].build(group)
        else:
            self.object_group_builder.build(group)
