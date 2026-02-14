from typing import List, Dict

from loguru import logger
from crunge import tmx

from ..tiled_builder import TiledBuilder
from ..tile_layer_builder import TileLayerBuilder
from ..object_group_builder import ObjectGroupBuilder
from ..image_layer_builder import ImageLayerBuilder
from ..layer_group_builder import LayerGroupBuilder


class MapBuilder(TiledBuilder):
    def __init__(
        self,
        tile_layer_builder: TileLayerBuilder,
        object_group_builder: ObjectGroupBuilder,
        image_layer_builder: ImageLayerBuilder,
        layer_group_builder: LayerGroupBuilder,
    ):
        super().__init__()
        self.tile_layer_builder = tile_layer_builder
        self.tile_layer_builders: Dict[str, TileLayerBuilder] = {}

        self.object_group_builder = object_group_builder
        self.object_group_builders: Dict[str, ObjectGroupBuilder] = {}

        self.image_layer_builder = image_layer_builder
        self.image_layer_builders: Dict[str, ImageLayerBuilder] = {}

        self.layer_group_builder = layer_group_builder
        self.layer_group_builders: Dict[str, LayerGroupBuilder] = {}

    def add_tile_layer_builder(self, name: str, builder: TileLayerBuilder):
        self.tile_layer_builders[name] = builder

    def add_tile_layer_builders(self, builders: Dict[str, TileLayerBuilder]):
        self.tile_layer_builders.update(builders)

    def add_object_group_builder(self, name: str, builder: ObjectGroupBuilder):
        self.object_group_builders[name] = builder

    def add_object_group_builders(self, builders: Dict[str, ObjectGroupBuilder]):
        self.object_group_builders.update(builders)

    def add_image_layer_builder(self, name: str, builder: ImageLayerBuilder):
        self.image_layer_builders[name] = builder

    def add_image_layer_builders(self, builders: Dict[str, ImageLayerBuilder]):
        self.image_layer_builders.update(builders)

    def add_layer_group_builder(self, name: str, builder: LayerGroupBuilder):
        self.layer_group_builders[name] = builder

    def add_layer_group_builders(self, builders: Dict[str, LayerGroupBuilder]):
        self.layer_group_builders.update(builders)

    def build(self):
        self.context.map_builder = self
        # for layer in self.map.visible_layers:
        for layer in self.map.layers:
            logger.debug(f"MapBuilder.build: {layer}")
            # logger.debug(f": {layer.properties}")
            self.build_layer(layer)

    def build_layer(self, tmx_layer: tmx.Layer):
        if isinstance(tmx_layer, tmx.TileLayer):
            self.build_tile_layer(tmx_layer)
        elif isinstance(tmx_layer, tmx.ObjectGroup):
            self.build_object_group(tmx_layer)
        elif isinstance(tmx_layer, tmx.ImageLayer):
            self.build_image_layer(tmx_layer)
        elif isinstance(tmx_layer, tmx.LayerGroup):
            self.build_layer_group(tmx_layer)
        else:
            raise ValueError(f"Unsupported element type: {type(tmx_layer)}")

    def build_tile_layer(self, tmx_layer: tmx.TileLayer):
        if tmx_layer.name in self.tile_layer_builders:
            self.tile_layer_builders[tmx_layer.name].build(tmx_layer)
        else:
            self.tile_layer_builder.build(tmx_layer)

    def build_object_group(self, tmx_layer: tmx.ObjectGroup):
        if tmx_layer.name in self.object_group_builders:
            self.object_group_builders[tmx_layer.name].build(tmx_layer)
        else:
            self.object_group_builder.build(tmx_layer)

    def build_image_layer(self, tmx_layer: tmx.ImageLayer):
        if tmx_layer.name in self.image_layer_builders:
            self.image_layer_builders[tmx_layer.name].build(tmx_layer)
        else:
            self.image_layer_builder.build(tmx_layer)

    def build_layer_group(self, tmx_layer: tmx.LayerGroup):
        if tmx_layer.name in self.layer_group_builders:
            self.layer_group_builders[tmx_layer.name].build(tmx_layer)
        else:
            self.layer_group_builder.build(tmx_layer)
