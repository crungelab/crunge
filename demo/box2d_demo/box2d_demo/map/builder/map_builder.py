import crunge.engine.loader.tiled.builder as tiled_builder

#from .tile_layer_run_builder import TileLayerRunBuilder
#from .tile_layer_chain_builder import TileLayerChainBuilder
#from .bitmap_terrain_builder import BitmapTerrainBuilder
from .polygon_terrain_builder import PolygonTerrainBuilder

from .character_layer_builder import CharacterLayerBuilder
from .static_object_group_builder import StaticObjectGroupBuilder
from .dynamic_object_group_builder import DynamicObjectGroupBuilder
from .obstacle_layer_builder import ObstacleLayerBuilder
from .flag_layer_builder import FlagLayerBuilder

class MapBuilder(tiled_builder.DefaultMapBuilder):
    def __init__(self):
        super().__init__()
        #self.add_tile_layer_builder("ground", TileLayerRunBuilder())
        #self.add_tile_layer_builder("ground", TileLayerChainBuilder())
        #self.add_tile_layer_builder("ground", BitmapTerrainBuilder())
        self.add_tile_layer_builder("ground", PolygonTerrainBuilder())
        self.add_object_group_builder("pc", CharacterLayerBuilder())
        self.add_object_group_builder("static", StaticObjectGroupBuilder())
        self.add_object_group_builder("object", DynamicObjectGroupBuilder())
        self.add_tile_layer_builder("obstacle", ObstacleLayerBuilder())
        self.add_tile_layer_builder("flags", FlagLayerBuilder())
