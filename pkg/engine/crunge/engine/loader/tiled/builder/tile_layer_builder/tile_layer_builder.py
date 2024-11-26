import glm
from pytmx import TiledTileLayer

from ..tiled_builder import TiledBuilder
from ..tile_builder import TileBuilder
from ..builder_context import BuilderContext

class TileLayerBuilder(TiledBuilder):
    def __init__(self, context: BuilderContext, tile_builder: TileBuilder):
        super().__init__(context)
        self.tile_builder = tile_builder

    def build(self, layer: TiledTileLayer):
        map = self.map
        for x, y, image in layer.tiles():
            y = layer.height - y
            x = x * map.tilewidth
            y = y * map.tileheight
            self.tile_builder.build(glm.vec2(x, y), image, layer.properties)
