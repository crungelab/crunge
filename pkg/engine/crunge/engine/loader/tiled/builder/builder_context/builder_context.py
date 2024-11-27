from typing import TYPE_CHECKING
    
from pytmx import TiledMap

if TYPE_CHECKING:
    from ..tile_layer_builder import TileLayerBuilder
    from ..object_group_builder import ObjectGroupBuilder
    from ..tile_builder import TileBuilder
    from ..object_builder import ObjectBuilder


class BuilderContext:
    def __init__(self):
        self._map: TiledMap = None
        self.pixel_height: int = 0
        self.tile_layer_builder: 'TileLayerBuilder' = None
        self.object_group_builder: 'ObjectGroupBuilder' = None
        self.tile_builder: 'TileBuilder' = None
        self.object_builder: 'ObjectBuilder' = None

        self.opacity: float = 1.0

    @property
    def map(self):
        return self._map

    @map.setter
    def map(self, map: TiledMap):
        self._map = map
        tw = map.tilewidth
        th = map.tileheight
        mw = map.width
        #mh = map.height - 1
        mh = map.height - 1
        self.pixel_height = mh * th
