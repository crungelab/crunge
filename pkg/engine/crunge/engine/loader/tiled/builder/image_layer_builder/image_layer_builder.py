from loguru import logger

import glm
from pytmx import TiledImageLayer

from ..tiled_builder import TiledBuilder
from ..builder_context import BuilderContext

class ImageLayerBuilder(TiledBuilder):
    def __init__(self, context: BuilderContext):
        super().__init__(context)

    def build(self, layer: TiledImageLayer, layer_id: int):
        pass