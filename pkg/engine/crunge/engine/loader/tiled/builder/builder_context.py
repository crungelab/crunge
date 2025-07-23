import glm
from pytmx import TiledMap

from crunge.engine.d2.scene_2d import Scene2D
from crunge.engine.d2.scene_layer_2d import SceneLayer2D


class BuilderContext:
    def __init__(self, scene: Scene2D):
        self.scene = scene
        self.layer: SceneLayer2D = None

        self._map: TiledMap = None
        self.size = glm.ivec2()
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
        self.size = glm.ivec2(mw * tw, mh * th)
