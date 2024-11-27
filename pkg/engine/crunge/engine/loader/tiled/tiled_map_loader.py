from pathlib import Path

from loguru import logger

from pytmx import TiledMap

from crunge.engine.loader import Loader

from .builder.builder_context import BuilderContext
from .builder.map_builder import MapBuilder, DefaultMapBuilder
from .builder.tile_layer_builder import TileLayerBuilder, DefaultTileLayerBuilder
from .builder.object_group_builder import ObjectGroupBuilder, DefaultObjectGroupBuilder
from .builder.tile_builder import TileBuilder, DefaultTileBuilder
from .builder.object_builder import ObjectBuilder, DefaultObjectBuilder


class TiledMapLoader(Loader):
    def __init__(
        self,
        context: BuilderContext,
        map_builder: MapBuilder = None,
        tile_layer_builder: TileLayerBuilder = None,
        object_group_builder: ObjectGroupBuilder = None,
        tile_builder: TileBuilder = None,
        object_builder: ObjectBuilder = None,
    ):
        super().__init__()
        context.tile_layer_builder = tile_layer_builder if tile_layer_builder is not None else DefaultTileLayerBuilder(context)
        context.object_group_builder = object_group_builder if object_group_builder is not None else DefaultObjectGroupBuilder(context)
        context.tile_builder = tile_builder if tile_builder is not None else DefaultTileBuilder(context)
        context.object_builder = object_builder if object_builder is not None else DefaultObjectBuilder(context)

        self.context = context
        self.map_builder = map_builder if map_builder is not None else DefaultMapBuilder(context)

    def load(self, filename: Path):
        logger.debug(f"Loading map: {filename}")
        map = TiledMap(filename)
        self.context.map = map
        self.map_builder.build()
