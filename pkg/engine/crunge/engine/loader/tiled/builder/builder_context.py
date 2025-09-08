import glm
from crunge import tmx

from crunge.engine.d2.scene_2d import Scene2D
from crunge.engine.d2.scene_layer_2d import SceneLayer2D
from crunge.engine.d2.sprite import Sprite

class BuilderContext:
    def __init__(self, scene: Scene2D):
        self.scene = scene
        self.layer: SceneLayer2D = None

        self._map: tmx.Map = None
        self.size = glm.ivec2()
        self.opacity: float = 1.0

        self.sprites: list[Sprite] = []

    @property
    def map(self):
        return self._map

    @map.setter
    def map(self, map: tmx.Map):
        self._map = map
        tile_size = map.tile_size
        tw = tile_size.x
        th = tile_size.y

        tile_count = map.tile_count
        mw = tile_count.x
        mh = tile_count.y - 1
        self.size = glm.ivec2(mw * tw, mh * th)

    def init_sprites(self, count: int):
        self.sprites = [None] * count