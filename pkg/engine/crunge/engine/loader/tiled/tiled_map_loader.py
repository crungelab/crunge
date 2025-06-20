from pathlib import Path

from loguru import logger

from pytmx import TiledMap

from crunge.engine.loader import Loader
from crunge.engine.resource.resource_manager import ResourceManager

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
    ):
        super().__init__()
        self.context = context
        self.map_builder = map_builder if map_builder is not None else DefaultMapBuilder(context)
        


    def load(self, path: Path):
        path = ResourceManager().resolve_path(path)
        logger.debug(f"Loading map: {path}")
        map = TiledMap(path)
        self.context.map = map
        self.map_builder.build()
