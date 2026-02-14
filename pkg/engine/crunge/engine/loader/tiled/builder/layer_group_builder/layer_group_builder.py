from loguru import logger

from crunge import tmx

from ..tiled_builder import TiledBuilder


class LayerGroupBuilder(TiledBuilder):
    def build(self, layer: tmx.LayerGroup, layer_id: int):
        pass
