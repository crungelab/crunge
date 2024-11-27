import glm

from ..builder_context import BuilderContext
from ..tiled_builder import TiledBuilder

class TileBuilder(TiledBuilder):
    def __init__(self, context: BuilderContext):
        super().__init__(context)

    def build(self, position: glm.vec2, image, properties):
        raise NotImplementedError()