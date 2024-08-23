import os
from pathlib import Path


from crunge.engine.gltf import GltfImporter

from .viewer import Viewer

models_root = Path(__file__).parent.parent.parent.parent.parent / "resources" / "models"
#models_root = Path(os.environ.get("GLTF_SAMPLE_MODELS"))

class GltfDemo:
    def __init__(self, scene_path: Path):
        self.scene_path = scene_path

    def run(self):
        scene = GltfImporter().load(self.scene_path)
        Viewer().create().show(scene).run()
