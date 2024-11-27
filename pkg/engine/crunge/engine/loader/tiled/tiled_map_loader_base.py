from pathlib import Path

from loguru import logger

from pytmx import TiledMap

from crunge.engine.loader import Loader

from .builder.builder_context import BuilderContext
from .builder.map_builder import MapBuilder
from .builder.tile_layer_builder import TileLayerBuilder
from .builder.object_group_builder import ObjectGroupBuilder
from .builder.tile_builder import TileBuilder
from .builder.object_builder import ObjectBuilder


class TiledMapLoaderBase(Loader):
    def __init__(
        self,
        context: BuilderContext,
        map_builder: MapBuilder,
        tile_layer_builder: TileLayerBuilder,
        object_group_builder: ObjectGroupBuilder,
        tile_builder: TileBuilder,
        object_builder: ObjectBuilder,
    ):
        super().__init__()
        self.context = context
        context.tile_layer_builder = tile_layer_builder
        context.object_group_builder = object_group_builder
        context.tile_builder = tile_builder
        context.object_builder = object_builder

        self.map_builder = map_builder

    def load(self, filename: Path):
        logger.debug(f"Loading map: {filename}")
        map = TiledMap(filename)
        self.context.map = map
        self.map_builder.build()
