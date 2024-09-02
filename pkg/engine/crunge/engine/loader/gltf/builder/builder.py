from crunge import gltf

from crunge.engine.base import Base
from .builder_context import BuilderContext

class Builder(Base):
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