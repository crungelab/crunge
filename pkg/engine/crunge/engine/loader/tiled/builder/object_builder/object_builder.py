from loguru import logger
from pytmx import TiledObject

from ..tiled_builder import TiledBuilder


class ObjectBuilder(TiledBuilder):
    def build(self, obj: TiledObject, properties: dict):
        #raise NotImplementedError()
        logger.debug(f"ObjectBuilder.build({obj}, {properties})")