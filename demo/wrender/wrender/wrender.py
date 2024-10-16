import os
from pathlib import Path


from crunge.engine.loader.gltf import GltfLoader

from .viewer import Viewer

#models_root = Path(__file__).parent.parent.parent.parent / "resources" / "models"
models_root = Path(os.environ.get("GLTF_SAMPLE_MODELS"))

class WRender(Viewer):
    def __init__(self):
        super().__init__()

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
        #model = "Box"
        #model = "BoxVertexColors"
        #model = "BoxTextured" #Need samplers
        #model = "BoomBox"
        #model = "Buggy"
        #model = "CesiumMan"
        model = "CesiumMilkTruck"
        #model = "Cube"
        #model = "Corset"
        #model = "DamagedHelmet"
        #model = "Duck"
        #model = "EnvironmentTest"
        #model = "FlightHelmet"
        #model = "Fox" #No normals, no indices
        #model = "GearboxAssy"
        #model = "Lantern"
        #model = "MetalRoughSpheres"
        #model = "SimpleMeshes"
        #model = "Suzanne"

        scene_path = models_root / model / "glTF" / f"{model}.gltf"
        #scene_path = models_root / model / "glTF-Embedded" / f"{model}.gltf"
        #scene_path = models_root / model / "glTF-Binary" / f"{model}.glb"

        #scene_path = models_root / "sphere.gltf"
        #scene_path = models_root / "teapot.gltf"
        #scene_path = models_root / "torusknot.gltf"

        scene = GltfLoader().load(scene_path)

        #Viewer().create().show(scene)
        #Viewer().create().show(scene).run()
        self.show(scene)
        super().run()

def main():
    WRender().create().run()

if __name__ == "__main__":
    main()
