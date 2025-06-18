import os
from pathlib import Path

import glfw

from crunge import wgpu

import gltfv.globals
from .scene_builder import SceneBuilder
from .viewer import Viewer

#models_root = Path(__file__).parent.parent.parent.parent / "resources" / "models"
models_root = Path(os.environ.get("GLTF_SAMPLE_ASSETS"))  / "Models"

class GltfV:
    def __init__(self):
        self.context = wgpu.Context()
        gltfv.globals.instance = self.instance
        gltfv.globals.device = self.device

    @property
    def instance(self) -> wgpu.Instance:
        return self.context.instance
    
    @property
    def adapter(self) -> wgpu.Adapter:
        return self.context.adapter
    
    @property
    def device(self) -> wgpu.Device:
        return self.context.device
    
    @property
    def queue(self) -> wgpu.Queue:
        return self.context.queue

    def run(self):
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
        #self.device.destroy()

def main():
    GltfV().run()
    glfw.terminate()

if __name__ == "__main__":
    main()
