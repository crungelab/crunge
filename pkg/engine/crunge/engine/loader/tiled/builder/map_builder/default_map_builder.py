from loguru import logger

from .....math import Bounds2

from ..tile_layer_builder import TileLayerBuilder, DefaultTileLayerBuilder
from ..object_group_builder import ObjectGroupBuilder, DefaultObjectGroupBuilder
from ..image_layer_builder import ImageLayerBuilder
from ..layer_group_builder import LayerGroupBuilder

from .map_builder import MapBuilder


class DefaultMapBuilder(MapBuilder):
    def __init__(
        self,
        tile_layer_builder: TileLayerBuilder = None,
        object_group_builder: ObjectGroupBuilder = None,
        image_layer_builder: ImageLayerBuilder = None,
        layer_group_builder: LayerGroupBuilder = None,
    ):
        super().__init__(
            (
                tile_layer_builder
                if tile_layer_builder is not None
                else DefaultTileLayerBuilder()
            ),
            (
                object_group_builder
                if object_group_builder is not None
                else DefaultObjectGroupBuilder()
            ),
            (
                image_layer_builder
                if image_layer_builder is not None
                else ImageLayerBuilder()
            ),
            (
                layer_group_builder
                if layer_group_builder is not None
                else LayerGroupBuilder()
            ),
        )

    def build(self):
        super().build()
        bounds = Bounds2(0, 0, self.context.size.x, self.context.size.y)
        logger.debug(f"Setting scene bounds to: {bounds}")
        self.context.scene.bounds = bounds