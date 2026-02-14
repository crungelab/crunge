from loguru import logger

import glm
from crunge import tmx

from ..tiled_builder import TiledBuilder
from ..tile_builder import TileBuilder

class TileLayerBuilder(TiledBuilder):
    def __init__(self, tile_builder: TileBuilder):
        super().__init__()
        self.tile_builder = tile_builder

    def build(self, layer: tmx.TileLayer, layer_id: int):
        map = self.map
        map_size = map.tile_count
        tile_size = map.tile_size
        tile_width = tile_size.x
        tile_height = tile_size.y
        half_tile_width = tile_width / 2
        half_tile_height = tile_height / 2
        tiles = layer.tiles

        for j in range(map_size.y):
            for i in range(map_size.x):
                tile_gid = tiles[j * map_size.x + i].id
                tile = map.get_tile(tile_gid)
                if tile is None:
                    continue
                properties = tile.properties
                x = i * tile_width + half_tile_width
                y = (j - 1) * tile_height + half_tile_height
                y = self.context.size.y - y

                self.tile_builder.build(glm.vec2(x, y), tile, tile_gid, properties)
