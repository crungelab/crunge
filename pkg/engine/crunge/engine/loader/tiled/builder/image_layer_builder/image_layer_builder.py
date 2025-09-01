from loguru import logger

import glm
from crunge import tmx

from ..tiled_builder import TiledBuilder
from ..builder_context import BuilderContext

class ImageLayerBuilder(TiledBuilder):
    def __init__(self, context: BuilderContext):
        super().__init__(context)

    def build(self, layer: tmx.ImageLayer, layer_id: int):
        pass