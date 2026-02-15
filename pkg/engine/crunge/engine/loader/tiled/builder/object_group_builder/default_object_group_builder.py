from loguru import logger

from crunge import tmx

from crunge.engine.d2.scene.layer.graph_layer_2d import GraphLayer2D

from crunge.engine.scene.layer.scene_layer import SceneLayer
from crunge.engine.scene.layer.filter.filter_layer import FilterLayer
from crunge.engine.scene.layer.filter.kawase_blur.kawase_blur_vu import KawaseBlurVu

from ..object_builder import ObjectBuilder, DefaultObjectBuilder

from .object_group_builder import ObjectGroupBuilder


class DefaultObjectGroupBuilder(ObjectGroupBuilder):
    def __init__(self, object_builder: ObjectBuilder = None):
        super().__init__(
            (
                object_builder
                if object_builder is not None
                else DefaultObjectBuilder()
            ),
        )

    def build(self, tmx_layer: tmx.ObjectGroup):
        kind = tmx_layer.get_class()
        logger.debug(f"Building layer of kind: {kind}")
        layer: SceneLayer = None
        if kind == "KawaseBlurLayer":
            layer = FilterLayer(name=tmx_layer.name, vu=KawaseBlurVu())
        else:
            layer = GraphLayer2D(name=tmx_layer.name)
        self.context.push_layer(layer)
        super().build(tmx_layer)
        self.context.pop_layer()
        self.context.current_layer_group.add_layer(layer)
