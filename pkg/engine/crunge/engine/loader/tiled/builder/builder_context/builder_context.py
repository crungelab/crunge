from pytmx import TiledMap


class BuilderContext:
    def __init__(self):
        self._map: TiledMap = None
        self.pixel_height: int = 0
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
        mh = map.height - 1
        self.pixel_height = mh * th
