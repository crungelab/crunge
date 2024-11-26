import glm
from pytmx import TiledObjectGroup

from crunge.engine.d2.scene_layer_2d import SceneLayer2D

from ..builder_context import BuilderContext
from ..object_builder import DefaultObjectBuilder

from .object_group_builder import ObjectGroupBuilder


class DefaultObjectGroupBuilder(ObjectGroupBuilder):
    def __init__(self, context: BuilderContext):
        super().__init__(context, object_builder=DefaultObjectBuilder(context))

    def build(self, layer: TiledObjectGroup):
        self.context.layer = SceneLayer2D(name=layer.name)
        super().build(layer)
        self.context.scene.add_layer(self.context.layer)
