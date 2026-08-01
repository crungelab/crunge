import glm

from crunge import tmx

import crunge.engine.loader.tiled.builder as tiled_builder
from crunge.engine.loader.tiled.builder import DefaultTileBuilder

from ...objects.tile import Tile, BoxTile

class TileLayerBoxBuilder(tiled_builder.DefaultTileLayerBuilder):
    def __init__(self):
        def create_node_cb(position, sprite, properties: dict):
            if properties.get("type") == "dirtCenter":
                return BoxTile(position, sprite)
            return Tile(position, sprite)

        super().__init__(tile_builder=DefaultTileBuilder(create_node_cb=create_node_cb))
