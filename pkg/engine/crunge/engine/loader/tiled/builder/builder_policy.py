from loguru import logger
from crunge import tmx

from .tiled_builder import TiledBuilder
from .builder_context import BuilderContext
from .tile_layer_builder import TileLayerBuilder
from .object_group_builder import ObjectGroupBuilder
from .image_layer_builder import ImageLayerBuilder
from .layer_group_builder import LayerGroupBuilder


class BuilderPolicy:
    def __init__(
        self,
        context: BuilderContext,
        tile_layer_builder: TileLayerBuilder,
        object_group_builder: ObjectGroupBuilder,
        image_layer_builder: ImageLayerBuilder,
        layer_group_builder: LayerGroupBuilder,
    ):
        super().__init__(context)
        self.tile_layer_builder = tile_layer_builder
        self.tile_layer_builders: dict[str, TileLayerBuilder] = {}

        self.object_group_builder = object_group_builder
        self.object_group_builders: dict[str, ObjectGroupBuilder] = {}

        self.image_layer_builder = image_layer_builder
        self.image_layer_builders: dict[str, ImageLayerBuilder] = {}

        self.layer_group_builder = layer_group_builder
        self.layer_group_builders: dict[str, LayerGroupBuilder] = {}

    def add_tile_layer_builder(self, name: str, builder: TileLayerBuilder):
        self.tile_layer_builders[name] = builder

    def add_tile_layer_builders(self, builders: dict[str, TileLayerBuilder]):
        self.tile_layer_builders.update(builders)

    def add_object_group_builder(self, name: str, builder: ObjectGroupBuilder):
        self.object_group_builders[name] = builder

    def add_object_group_builders(self, builders: dict[str, ObjectGroupBuilder]):
        self.object_group_builders.update(builders)

    def add_image_layer_builder(self, name: str, builder: ImageLayerBuilder):
        self.image_layer_builders[name] = builder

    def add_image_layer_builders(self, builders: dict[str, ImageLayerBuilder]):
        self.image_layer_builders.update(builders)

    def add_layer_group_builder(self, name: str, builder: LayerGroupBuilder):
        self.layer_group_builders[name] = builder

    def add_layer_group_builders(self, builders: dict[str, LayerGroupBuilder]):
        self.layer_group_builders.update(builders)

    def build_layer(self, layer: tmx.Layer, layer_id: int):
        if isinstance(layer, tmx.TileLayer):
            self.build_tile_layer(layer, layer_id)
        elif isinstance(layer, tmx.ObjectGroup):
            self.build_object_group(layer, layer_id)
        elif isinstance(layer, tmx.ImageLayer):
            self.build_image_layer(layer, layer_id)
        elif isinstance(layer, tmx.LayerGroup):
            self.build_layer_group(layer, layer_id)
        else:
            raise ValueError(f"Unsupported element type: {type(layer)}")

    def build_tile_layer(self, layer: tmx.TileLayer, layer_id: int):
        if layer.name in self.tile_layer_builders:
            self.tile_layer_builders[layer.name].build(layer, layer_id)
        else:
            self.tile_layer_builder.build(layer, layer_id)

    def build_object_group(self, group: tmx.ObjectGroup, layer_id: int):
        if group.name in self.object_group_builders:
            self.object_group_builders[group.name].build(group, layer_id)
        else:
            self.object_group_builder.build(group, layer_id)

    def build_image_layer(self, layer: tmx.ImageLayer, layer_id: int):
        if layer.name in self.image_layer_builders:
            self.image_layer_builders[layer.name].build(layer, layer_id)
        else:
            self.image_layer_builder.build(layer, layer_id)

    def build_layer_group(self, layer: tmx.LayerGroup, layer_id: int):
        if layer.name in self.layer_group_builders:
            self.layer_group_builders[layer.name].build(layer, layer_id)
        else:
            self.layer_group_builder.build(layer, layer_id)
