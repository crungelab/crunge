import glm

from crunge import tmx

import crunge.engine.loader.tiled.builder as tiled_builder
from crunge.engine.loader.tiled.builder import DefaultTileBuilder

from ...objects.tile import Tile, BoxTile, GhostTile

class TileLayerBuilder(tiled_builder.DefaultTileLayerBuilder):
    def __init__(self):
        def create_node_cb(position, sprite, properties: dict):
            if properties.get("type") == "dirtCenter":
                return GhostTile(position, sprite)
            return Tile(position, sprite)

        super().__init__(tile_builder=DefaultTileBuilder(create_node_cb=create_node_cb))

    def build(self, tmx_layer: tmx.TileLayer):
        super().build(tmx_layer)

        map = self.map
        map_size = map.tile_count
        tile_size = map.tile_size
        tile_width = tile_size.x
        tile_height = tile_size.y
        half_tile_width = tile_width / 2
        half_tile_height = tile_height / 2
        tiles = tmx_layer.tiles

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

                position = glm.vec2(x, y) / self.ppu

                # ...
