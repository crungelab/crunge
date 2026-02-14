import glm

from ..tiled_builder import TiledBuilder

class TileBuilder(TiledBuilder):
    def build(self, position: glm.vec2, image, properties):
        raise NotImplementedError()