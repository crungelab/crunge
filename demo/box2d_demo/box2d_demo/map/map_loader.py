from crunge.engine.loader.tiled import TiledMapLoader, BuilderContext
from crunge.engine.d2.scene import Scene2D
from .builder.map_builder import MapBuilder

class MapLoader(TiledMapLoader):
    def __init__(self, scene: Scene2D):
        context = BuilderContext(scene)
        super().__init__(context, map_builder=MapBuilder())
