from crunge import tmx

from ..object_builder import ObjectBuilder
from ..tiled_builder import TiledBuilder
from ..object_builder import ObjectBuilder

class ObjectGroupBuilder(TiledBuilder):
    def __init__(self, object_builder: ObjectBuilder):
        super().__init__()
        self.object_builder = object_builder

    def build(self, layer: tmx.ObjectGroup):
        self.context.opacity = layer.opacity
        for obj in layer.get_objects():
            self.object_builder.build(obj)
