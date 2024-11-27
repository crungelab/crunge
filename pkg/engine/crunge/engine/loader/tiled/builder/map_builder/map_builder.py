from pytmx import TiledTileLayer, TiledObjectGroup

from ..tiled_builder import TiledBuilder
from ..builder_context import BuilderContext

class MapBuilder(TiledBuilder):
    def __init__(self, context: BuilderContext):
        super().__init__(context)

    def build(self):
        for layer in self.map.visible_layers:
            if isinstance(layer, TiledTileLayer):
                self.context.tile_layer_builder.build(layer)
            elif isinstance(layer, TiledObjectGroup):
                self.context.object_group_builder.build(layer)
            else:
                raise ValueError(f"Unsupported layer type: {type(layer)}")
