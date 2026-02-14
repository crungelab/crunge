from loguru import logger

from crunge import tmx

from ..tiled_builder import TiledBuilder
from ..builder_context import BuilderContext

class LayerGroupBuilder(TiledBuilder):
    def __init__(self, context: BuilderContext):
        super().__init__(context)

    def build(self, layer: tmx.LayerGroup, layer_id: int):
        pass