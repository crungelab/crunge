from loguru import logger

from crunge import tmx

from crunge.engine.d2.graph_layer_2d import GraphLayer2D

from crunge.engine.scene.layer.filter.filter_layer import FilterLayer
from crunge.engine.scene.layer.filter.kawase_blur.kawase_blur_vu import KawaseBlurVu

from ..builder_context import BuilderContext
from ..object_builder import ObjectBuilder, DefaultObjectBuilder

from .object_group_builder import ObjectGroupBuilder


class DefaultObjectGroupBuilder(ObjectGroupBuilder):
    def __init__(self, context: BuilderContext, object_builder: ObjectBuilder = None):
        super().__init__(
            context,
            (
                object_builder
                if object_builder is not None
                else DefaultObjectBuilder(context)
            ),
        )

    def build(self, layer: tmx.ObjectGroup, layer_id: int):
        kind = layer.get_class()
        logger.debug(f"Building layer of kind: {kind}")
        if kind == "KawaseBlurLayer":
            self.context.layer = FilterLayer(name=layer.name, vu=KawaseBlurVu())
        else:
            self.context.layer = GraphLayer2D(name=layer.name)
        super().build(layer, layer_id)
        self.context.scene.add_layer(self.context.layer)
