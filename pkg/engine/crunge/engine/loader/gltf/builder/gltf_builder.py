from crunge import gltf

from crunge.engine.builder import Builder
from .builder_context import BuilderContext

class GltfBuilder(Builder):
    def __init__(self, context: BuilderContext) -> None:
        super().__init__()
        self.context = context

    @property
    def scene(self):
        return self.context.scene

    @scene.setter
    def scene(self, scene):
        self.context.scene = scene

    @property
    def tf_model(self) -> gltf.Model:
        return self.context.tf_model