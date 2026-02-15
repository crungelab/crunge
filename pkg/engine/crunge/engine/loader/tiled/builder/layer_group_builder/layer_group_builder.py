from loguru import logger

from crunge import tmx
from crunge.engine.scene.layer.layer_group import LayerGroup
from crunge.engine.d2.scene.layer.composite_layer_2d import CompositeLayer2D

from ..tiled_builder import TiledBuilder


class LayerGroupBuilder(TiledBuilder):
    def build(self, tmx_layer: tmx.LayerGroup):
        kind = tmx_layer.get_class()
        layer: LayerGroup = None
        if kind == "CompositeLayer":
            layer = CompositeLayer2D(name=tmx_layer.name)
        else:
            layer = LayerGroup(name=tmx_layer.name)
        self.context.current_layer_group.add_layer(layer)

        self.context.push_layer(layer)
        for sublayer in tmx_layer.get_layers():
            self.context.map_builder.build_layer(sublayer)
        self.context.pop_layer()
