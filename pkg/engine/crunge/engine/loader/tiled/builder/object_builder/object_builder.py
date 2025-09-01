from loguru import logger
from crunge import tmx

from ..tiled_builder import TiledBuilder


class ObjectBuilder(TiledBuilder):
    def build(self, obj: tmx.Object):
        #raise NotImplementedError()
        logger.debug(f"ObjectBuilder.build({obj})")