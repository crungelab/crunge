from pathlib import Path

from loguru import logger
import glm
from pytmx import TiledMap, TiledTileLayer, TiledObjectGroup

from crunge.engine.loader import Loader

from .builder.map_builder import MapBuilder
from .builder.builder_context import BuilderContext

class TiledMapLoader(Loader):
    def __init__(self, context: BuilderContext, map_builder: MapBuilder):
        super().__init__()
        self.context = context
        self.map_builder = map_builder

    def load(self, filename: Path):
        logger.debug(f"Loading map: {filename}")
        map = TiledMap(filename)
        self.context.map = map
        self.map_builder.build()
