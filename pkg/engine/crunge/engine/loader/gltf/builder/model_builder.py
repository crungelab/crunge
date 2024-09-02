from crunge import gltf

from . import Builder
from .builder_context import BuilderContext

class ModelBuilder(Builder):
    #tf_model: gltf.Model

    def __init__(self, context: BuilderContext) -> None:
        #super().__init__(context)
        super().__init__()
        self.context = context

    @property
    def scene(self):
        return self.context.scene

    @property
    def tf_model(self) -> gltf.Model:
        return self.context.tf_model