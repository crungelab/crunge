import time
import sys
import math
import glm
from pathlib import Path

resource_root = Path(__file__).parent.parent / "resources"

from .scene import Scene
from .viewer import Viewer

class GLTFV:
    def __init__(self):
        pass

    def run(self):
        scene = Scene()
        viewer = Viewer()
        #scene_path = resource_root / "models" / "BoxTextured" / "glTF" / "BoxTextured.gltf"
        #scene_path = resource_root / "models" / "Cube" / "glTF" / "Cube.gltf"
        #scene_path = resource_root / "models" / "CesiumMilkTruck" / "glTF" / "CesiumMilkTruck.gltf"
        scene_path = resource_root / "models" / "DamagedHelmet" / "glTF" / "DamagedHelmet.gltf"
        scene.load(scene_path)
        viewer.view(scene)

def main():
    GLTFV().run()

if __name__ == "__main__":
    main()
