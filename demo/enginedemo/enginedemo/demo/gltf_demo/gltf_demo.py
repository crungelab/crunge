import os
from pathlib import Path

from crunge.engine.gltf import GltfImporter

from .viewer import Viewer


class GltfDemo:
    def __init__(self, scene_path: Path):
        self.scene_path = scene_path
        self.create_importer()

    def create_importer(self):
        return GltfImporter()

    def run(self):
        importer = self.create_importer()
        scene = importer.load(self.scene_path)
        Viewer().create().show(scene).run()
