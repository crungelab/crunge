from .....math import Bounds2

from ..tile_layer_builder import TileLayerBuilder, DefaultTileLayerBuilder
from ..object_group_builder import ObjectGroupBuilder, DefaultObjectGroupBuilder
from ..image_layer_builder import ImageLayerBuilder

from .map_builder import MapBuilder


class DefaultMapBuilder(MapBuilder):
    def __init__(
        self,
        context,
        tile_layer_builder: TileLayerBuilder = None,
        object_group_builder: ObjectGroupBuilder = None,
        image_layer_builder: ImageLayerBuilder = None,
    ):
        super().__init__(
            context,
            (
                tile_layer_builder
                if tile_layer_builder is not None
                else DefaultTileLayerBuilder(context)
            ),
            (
                object_group_builder
                if object_group_builder is not None
                else DefaultObjectGroupBuilder(context)
            ),
            (
                image_layer_builder
                if image_layer_builder is not None
                else ImageLayerBuilder(context)
            ),
        )

    def build(self):
        super().build()
        self.context.scene.bounds = Bounds2(0, 0, self.context.size.x, self.context.size.y)
