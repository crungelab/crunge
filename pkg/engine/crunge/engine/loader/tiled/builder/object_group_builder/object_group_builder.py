from pytmx import TiledObjectGroup

from ..object_builder import ObjectBuilder
from ..tiled_builder import TiledBuilder
from ..builder_context import BuilderContext
from ..object_builder import ObjectBuilder

class ObjectGroupBuilder(TiledBuilder):
    def __init__(self, context: BuilderContext, object_builder: ObjectBuilder):
        super().__init__(context)
        self.object_builder = object_builder

    def build(self, layer: TiledObjectGroup):
        self.context.opacity = layer.opacity
        for obj in layer:
            self.object_builder.build(obj)
