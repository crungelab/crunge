import glm
from pytmx import TiledTileLayer

from ..tiled_builder import TiledBuilder
from ..builder_context import BuilderContext

class TileLayerBuilder(TiledBuilder):
    def __init__(self, context: BuilderContext):
        super().__init__(context)

    def build(self, layer: TiledTileLayer):
        map = self.map
        tile_width = map.tilewidth
        tile_height = map.tileheight
        half_tile_width = tile_width / 2
        half_tile_height = tile_height / 2

        for x, y, image in layer.tiles():
            #y = layer.height - y
            x = x * tile_width + half_tile_width
            y = y * tile_height + half_tile_height
            y = self.context.pixel_height - y
            self.context.tile_builder.build(glm.vec2(x, y), image, layer.properties)
