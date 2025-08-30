from typing import List, Dict

from loguru import logger
from pytmx import TiledTileLayer, TiledObjectGroup, TiledElement, TiledImageLayer

from ..tiled_builder import TiledBuilder
from ..builder_context import BuilderContext
from ..tile_layer_builder import TileLayerBuilder
from ..object_group_builder import ObjectGroupBuilder
from ..image_layer_builder import ImageLayerBuilder

class MapBuilder(TiledBuilder):
    def __init__(self, context: BuilderContext, tile_layer_builder: TileLayerBuilder, object_group_builder: ObjectGroupBuilder, image_layer_builder: ImageLayerBuilder):
        super().__init__(context)
        self.tile_layer_builder = tile_layer_builder
        self.object_group_builder = object_group_builder
        self.image_layer_builder = image_layer_builder
        self.tile_layer_builders: Dict[str, TileLayerBuilder] = {}
        self.object_group_builders: Dict[str, ObjectGroupBuilder] = {}
        self.image_layer_builders: Dict[str, ImageLayerBuilder] = {}

    def add_tile_layer_builder(self, name: str, builder: TileLayerBuilder):
        self.tile_layer_builders[name] = builder

    def add_object_group_builder(self, name: str, builder: ObjectGroupBuilder):
        self.object_group_builders[name] = builder

    def add_image_layer_builder(self, name: str, builder: ImageLayerBuilder):
        self.image_layer_builders[name] = builder

    def add_tile_layer_builders(self, builders: Dict[str, TileLayerBuilder]):
        self.tile_layer_builders.update(builders)

    def add_object_group_builders(self, builders: Dict[str, ObjectGroupBuilder]):
        self.object_group_builders.update(builders)

    def add_image_layer_builders(self, builders: Dict[str, ImageLayerBuilder]):
        self.image_layer_builders.update(builders)

    def build(self):
        #for layer_id, layer in enumerate(self.map.visible_layers):
        for layer_id, layer in enumerate(self.map.layers):
            logger.debug(f"MapBuilder.build: {layer}")
            logger.debug(f": {layer.properties}")
            self.build_layer(layer, layer_id)
    
    def build_layer(self, layer: TiledElement, layer_id: int):
        if isinstance(layer, TiledTileLayer):
            self.build_tile_layer(layer, layer_id)
        elif isinstance(layer, TiledObjectGroup):
            self.build_object_group(layer, layer_id)
        elif isinstance(layer, TiledImageLayer):
            self.build_image_layer(layer, layer_id)
        else:
            raise ValueError(f"Unsupported element type: {type(layer)}")

    def build_tile_layer(self, layer: TiledTileLayer, layer_id: int):
        if layer.name in self.tile_layer_builders:
            self.tile_layer_builders[layer.name].build(layer, layer_id)
        else:
            self.tile_layer_builder.build(layer, layer_id)

    def build_object_group(self, group: TiledObjectGroup, layer_id: int):
        if group.name in self.object_group_builders:
            self.object_group_builders[group.name].build(group, layer_id)
        else:
            self.object_group_builder.build(group, layer_id)

    def build_image_layer(self, layer: TiledImageLayer, layer_id: int):
        if layer.name in self.image_layer_builders:
            self.image_layer_builders[layer.name].build(layer, layer_id)
        else:
            self.image_layer_builder.build(layer, layer_id)
