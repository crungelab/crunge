import time
import sys
import math
import glm
from pathlib import Path

from crunge.core import as_capsule
from crunge import wgpu
import crunge.wgpu.utils as utils

import gltfv.globals
from .scene_builder import SceneBuilder
from .viewer import Viewer

resource_root = Path(__file__).parent.parent / "resources"

class GLTFV:
    def __init__(self):
        pass

    def run(self):
        self.instance = wgpu.create_instance()
        gltfv.globals.instance = self.instance
        self.adapter = self.instance.request_adapter()
        self.device = self.adapter.create_device()
        gltfv.globals.device = self.device
        self.device.set_label("Primary Device")
        self.device.enable_logging()

        #scene_path = resource_root / "models" / "BoxTextured" / "glTF" / "BoxTextured.gltf"
        #scene_path = resource_root / "models" / "Cube" / "glTF" / "Cube.gltf"
        #scene_path = resource_root / "models" / "CesiumMilkTruck" / "glTF" / "CesiumMilkTruck.gltf"
        scene_path = resource_root / "models" / "DamagedHelmet" / "glTF" / "DamagedHelmet.gltf"

        scene = SceneBuilder().load(scene_path)
        Viewer().show(scene)

def main():
    GLTFV().run()

if __name__ == "__main__":
    main()
