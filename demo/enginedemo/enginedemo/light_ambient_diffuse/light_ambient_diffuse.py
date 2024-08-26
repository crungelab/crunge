import os
from pathlib import Path

from jinja2 import FileSystemLoader
import glm

from crunge import imgui

from crunge.engine.renderer import Renderer
from crunge.engine.gltf import GltfImporter

from ..demo.gltf_demo import GltfDemo


class AmbientDiffuseLightDemo(GltfDemo):
    title = "Ambient Diffuse Light Demo"
    def create_importer(self):
        module_path = Path(__file__).resolve()
        template_dir = module_path.parent / 'templates'
        importer = GltfImporter(template_loaders=[FileSystemLoader(template_dir)])
        return importer

    def draw(self, renderer: Renderer):
        imgui.begin(self.title)

        imgui.begin_group()
        ambient_light = self.scene.ambient_light
        changed, newColor = imgui.color_edit3("Ambient Color", list(ambient_light.color))
        if changed:
            ambient_light.color = glm.vec3(newColor)
        imgui.end_group()

        for diffuse_light in self.scene.lighting.lights:
            imgui.begin_group()
            #diffuse_light = self.scene.lighting.lights[0]
            changed, newColor = imgui.color_edit3("Diffuse Color", list(diffuse_light.color))
            if changed:
                diffuse_light.color = glm.vec3(newColor)
            imgui.end_group()

        imgui.end()

        super().draw(renderer)


def main():
    models_root = (
        Path(__file__).parent.parent.parent.parent.parent / "resources" / "models"
    )
    # models_root = Path(os.environ.get("GLTF_SAMPLE_MODELS"))

    # model = "2CylinderEngine"
    # model = "Avocado"
    # model = "Box"
    # model = "BoxVertexColors"
    # model = "BoxTextured" #Need samplers
    # model = "BoomBox"
    # model = "Buggy"
    # model = "CesiumMan"
    # model = "CesiumMilkTruck"
    # model = "Cube"
    # model = "Corset"
    model = "DamagedHelmet"
    # model = "Duck"
    # model = "EnvironmentTest"
    # model = "FlightHelmet"
    # model = "Fox" #No normals, no indices
    # model = "GearboxAssy"
    # model = "Lantern"
    # model = "MetalRoughSpheres"
    # model = "SimpleMeshes"
    # model = "Suzanne"

    scene_path = models_root / model / "glTF" / f"{model}.gltf"
    # scene_path = models_root / model / "glTF-Embedded" / f"{model}.gltf"
    # scene_path = models_root / model / "glTF-Binary" / f"{model}.glb"

    # scene_path = models_root / "BoxVertexColors" / "glTF" / "BoxVertexColors.gltf"
    # scene_path = models_root / "BoxTextured" / "glTF" / "BoxTextured.gltf"
    # scene_path = models_root / "Cube" / "glTF" / "Cube.gltf"
    # scene_path = models_root / "SimpleMeshes" / "glTF" / "SimpleMeshes.gltf"
    # scene_path = models_root / "CesiumMilkTruck" / "glTF" / "CesiumMilkTruck.gltf"
    # scene_path = models_root / "DamagedHelmet" / "glTF" / "DamagedHelmet.gltf"
    # scene_path = models_root / "Character" / "Character.gltf"
    # scene_path = models_root / "RobotCopernicus" / "scene.gltf"

    # scene_path = models_root / "sphere.gltf"
    # scene_path = models_root / "teapot.gltf"
    # scene_path = models_root / "torusknot.gltf"
    scene_path = models_root / "Fourareen" / "fourareen.gltf"

    AmbientDiffuseLightDemo(scene_path=scene_path).create().run()


if __name__ == "__main__":
    main()
