from crunge import gltf

from .builder import Builder


class ModelBuilder(Builder):
    tf_model: gltf.Model

    def __init__(self, tf_model: gltf.Model) -> None:
        super().__init__()
        self.tf_model = tf_model
