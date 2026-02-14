from loguru import logger

from crunge import tmx

from ..tiled_builder import TiledBuilder


class ImageLayerBuilder(TiledBuilder):
    def build(self, layer: tmx.ImageLayer, layer_id: int):
        pass