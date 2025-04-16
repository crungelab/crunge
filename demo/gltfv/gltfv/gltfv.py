import os
import time
import sys
import math
import glm
from pathlib import Path

from crunge import wgpu
import crunge.wgpu.utils as utils

import gltfv.globals
from .scene_builder import SceneBuilder
from .viewer import Viewer

#models_root = Path(__file__).parent.parent.parent.parent / "resources" / "models"
models_root = Path(os.environ.get("GLTF_SAMPLE_MODELS"))

class GltfV:
    def __init__(self):
        pass

    def run(self):
        instance_capabilities = wgpu.InstanceCapabilities()
        instance_capabilities.timed_wait_any_enable = True

        instance_descriptor = wgpu.InstanceDescriptor()
        instance_descriptor.capabilities = instance_capabilities
        self.instance = wgpu.create_instance(instance_descriptor)

        #self.instance = wgpu.create_instance()
        gltfv.globals.instance = self.instance
        self.adapter = self.instance.request_adapter()
        self.device = self.adapter.create_device()
        gltfv.globals.device = self.device
        self.device.set_label("Primary Device")
        self.device.enable_logging()

        #scene_path = models_root / "BoxVertexColors" / "glTF" / "BoxVertexColors.gltf"
        #scene_path = models_root / "BoxTextured" / "glTF" / "BoxTextured.gltf"
        #scene_path = models_root / "Cube" / "glTF" / "Cube.gltf"
        #scene_path = models_root / "SimpleMeshes" / "glTF" / "SimpleMeshes.gltf"
        #scene_path = models_root / "CesiumMilkTruck" / "glTF" / "CesiumMilkTruck.gltf"
        #scene_path = models_root / "DamagedHelmet" / "glTF" / "DamagedHelmet.gltf"
        #scene_path = models_root / "Character" / "Character.gltf"
        #scene_path = models_root / "RobotCopernicus" / "scene.gltf"

        #model = "2CylinderEngine"
        #model = "Avocado"
        #model = "BoxVertexColors"
        #model = "BoxTextured"
        #model = "BoomBox"
        #model = "Buggy"
        #model = "CesiumMilkTruck"
        #model = "Cube"
        #model = "Corset"
        model = "DamagedHelmet"
        #model = "Duck"
        #model = "FlightHelmet"
        #model = "Fox" #No normals, no indices
        #model = "GearboxAssy"
        #model = "Lantern"
        #model = "SimpleMeshes"

        scene_path = models_root / model / "glTF" / f"{model}.gltf"
        #scene_path = models_root / model / "glTF-Embedded" / f"{model}.gltf"
        #scene_path = models_root / model / "glTF-Binary" / f"{model}.glb"
        scene = SceneBuilder().build(scene_path)
        #exit()
        Viewer().show(scene)
        self.device.destroy()

def main():
    GltfV().run()

if __name__ == "__main__":
    main()
