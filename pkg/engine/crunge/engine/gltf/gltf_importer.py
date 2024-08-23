from pathlib import Path

from ..d3.scene_3d import Scene3D

from .builder.scene_builder import SceneBuilder


class GltfImporter:
    def __init__(self) -> None:
        pass

    def load(self, scene_path:Path) -> Scene3D:
        scene = SceneBuilder().build(scene_path)
        return scene