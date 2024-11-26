from crunge.engine.d2.scene_2d import Scene2D
from crunge.engine.d2.scene_layer_2d import SceneLayer2D

from ..builder_context import BuilderContext


class SceneBuilderContext(BuilderContext):
    def __init__(self, scene: Scene2D):
        super().__init__()
        self.scene = scene
        self.layer: SceneLayer2D = None
