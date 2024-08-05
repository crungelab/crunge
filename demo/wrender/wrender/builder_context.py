from crunge import gltf

from .scene import Scene

class BuilderContext:
    def __init__(self, scene: Scene, tf_model: gltf.Model) -> None:
        super().__init__()
        self.scene = scene
        self.tf_model = tf_model
