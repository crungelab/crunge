from loguru import logger

import glm
from pytmx import TiledTileLayer

from ..tiled_builder import TiledBuilder
from ..builder_context import BuilderContext
from ..tile_builder import TileBuilder

class TileLayerBuilder(TiledBuilder):
    def __init__(self, context: BuilderContext, tile_builder: TileBuilder):
        super().__init__(context)
        self.tile_builder = tile_builder

    def build(self, layer: TiledTileLayer, layer_id: int):
        map = self.map
        tile_width = map.tilewidth
        tile_height = map.tileheight
        half_tile_width = tile_width / 2
        half_tile_height = tile_height / 2

        '''
        for tx, ty, gid in layer.iter_data():
            properties = map.get_tile_properties_by_gid(gid)
            logger.debug(f"process_tile: {tx}, {ty}, {gid}, {properties}")
            #y = layer.height - y
            x = tx * tile_width + half_tile_width
            y = ty * tile_height + half_tile_height
            y = self.context.pixel_height - y
            self.tile_builder.build(glm.vec2(x, y), map.get_tile_image_by_gid(gid), properties)
        '''
        for x, y, image in layer.tiles():
            tile_gid = map.get_tile_gid(x, y, layer_id)
            properties = map.get_tile_properties_by_gid(tile_gid)
            #y = layer.height - y
            x = x * tile_width + half_tile_width
            y = y * tile_height + half_tile_height
            y = self.context.pixel_height - y
            #self.tile_builder.build(glm.vec2(x, y), image, layer.properties)
            self.tile_builder.build(glm.vec2(x, y), image, properties)
