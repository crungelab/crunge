from ..tile_layer_builder import DefaultTileLayerBuilder
from ..object_group_builder import DefaultObjectGroupBuilder

from .map_builder import MapBuilder


class DefaultMapBuilder(MapBuilder):
    def __init__(self, context):
        super().__init__(
            context,
            tile_layer_builder=DefaultTileLayerBuilder(context),
            object_group_builder=DefaultObjectGroupBuilder(context),
        )
