import time
import sys
import math
import glm
from pathlib import Path

from crunge import as_capsule
from crunge import wgpu
import crunge.wgpu.utils as utils

import trimeshv.globals
from .scene_builder import SceneBuilder
from .viewer import Viewer

resource_root = Path(__file__).parent.parent / "resources"

class TrimeshV:
    def __init__(self):
        pass

    def run(self):
        self.instance = wgpu.create_instance()
        trimeshv.globals.instance = self.instance
        self.adapter = self.instance.request_adapter()
        self.device = self.adapter.create_device()
        trimeshv.globals.device = self.device
        self.device.set_label("Primary Device")
        self.device.enable_logging()

        #scene_path = resource_root / "models" / "BoxVertexColors" / "glTF" / "BoxVertexColors.gltf"
        #scene_path = resource_root / "models" / "BoxTextured" / "glTF" / "BoxTextured.gltf"
        #scene_path = resource_root / "models" / "Cube" / "glTF" / "Cube.gltf"
        #scene_path = resource_root / "models" / "SimpleMeshes" / "glTF" / "SimpleMeshes.gltf"
        #scene_path = resource_root / "models" / "CesiumMilkTruck" / "glTF" / "CesiumMilkTruck.gltf"
        scene_path = resource_root / "models" / "DamagedHelmet" / "glTF" / "DamagedHelmet.gltf"
        #scene_path = resource_root / "models" / "Character" / "Character.gltf"
        #scene_path = resource_root / "models" / "RobotCopernicus" / "scene.gltf"

        scene = SceneBuilder().load(scene_path)
        Viewer().show(scene)

def main():
    TrimeshV().run()

if __name__ == "__main__":
    main()
