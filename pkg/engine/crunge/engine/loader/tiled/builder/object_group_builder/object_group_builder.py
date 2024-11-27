from pytmx import TiledObjectGroup

from ..object_builder import ObjectBuilder
from ..tiled_builder import TiledBuilder
from ..builder_context import BuilderContext


class ObjectGroupBuilder(TiledBuilder):
    def __init__(self, context: BuilderContext):
        super().__init__(context)

    def build(self, layer: TiledObjectGroup):
        self.context.opacity = layer.opacity
        for obj in layer:
            self.context.object_builder.build(obj, layer.properties)
