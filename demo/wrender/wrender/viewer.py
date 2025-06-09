import time
import os, sys
import math
from pathlib import Path
import tkinter
import tkinter.filedialog

from loguru import logger
import glm

from crunge import sdl
from crunge import imgui
from crunge import engine

from crunge.engine.viewport import SurfaceViewport
from crunge.engine import Renderer, Scheduler

from crunge.engine.loader.gltf import GltfLoader

from crunge.engine.d3.scene_3d import Scene3D
from crunge.engine.d3.controller.camera.arcball import ArcballCameraController
from crunge.engine.d3.view_3d import View3D
from crunge.engine.d3.director_3d import Director3D

models_root = Path(os.environ.get("GLTF_SAMPLE_ASSETS")) / "Models"


class Viewer(engine.App):
    view: View3D

    def __init__(self):
        super().__init__(title="WRender", resizable=True)
        self.delta_time = 0
        self.director: Director3D = None

    @property
    def camera(self):
        return self.view.camera

    def create_viewport(self):
        self.viewport = SurfaceViewport(
            self.size, self.window, use_depth_stencil=True, use_msaa=True
        )

    def create_view(self, scene: Scene3D):
        logger.debug("Creating view")
        self.view = View3D(scene).config(window=self).create()

    def open(self):
        logger.debug("Opening scene")
        scene_path = tkinter.filedialog.askopenfilename(
            initialdir=models_root,
            title="Select file",
            filetypes=(
                ("gltf files", "*.gltf"),
                ("glb files", "*.glb"),
                ("all files", "*.*"),
            ),
        )
        if not scene_path:
            return
        scene = GltfLoader().load(scene_path)
        Scheduler().schedule_once(lambda dt: self.show(scene))

    def show(self, scene: Scene3D):
        logger.debug("Showing scene")
        self.scene = scene
        self.create_view(scene)

        self.director = Director3D(scene)

        light = self.scene.lighting.lights[0]

        self.director.place_camera_and_light(self.camera, light)
        target = self.director.get_target_position()
        max_extent = self.director.get_max_extent()
        self.controller = ArcballCameraController(self, self.camera, target, max_extent)
        self.controller.activate()

        return self

    def draw(self, renderer: Renderer):
        self.draw_mainmenu()

        imgui.begin("Scene Properties")

        light = self.scene.lighting.lights[0]

        changed, position = imgui.drag_float3("Diffuse Position", tuple(light.position))
        if changed:
            light.position = glm.vec3(position)

        changed, color = imgui.color_edit3("Diffuse Color", list(light.color))
        if changed:
            light.color = glm.vec3(color)

        changed, energy = imgui.slider_float("Diffuse Energy", light.energy, 0.0, 100.0)
        if changed:
            light.energy = energy

        changed, range = imgui.slider_float("Diffuse Range", light.range, 1.0, 20.0)
        if changed:
            light.range = range

        imgui.end()

        super().draw(renderer)

    def draw_mainmenu(self):
        if imgui.begin_main_menu_bar():
            # File
            if imgui.begin_menu("File", True):
                clicked_open, selected_open = imgui.menu_item(
                    "Open", "Ctrl+O", False, True
                )

                if clicked_open:
                    self.open()

                imgui.separator()

                clicked_exit, selected_exit = imgui.menu_item(
                    "Exit", "Ctrl+Q", False, True
                )
                if clicked_exit:
                    self.quit()

                imgui.end_menu()

            # View
            if imgui.begin_menu("View", True):
                imgui.end_menu()

            imgui.end_main_menu_bar()

    def on_key(self, event: sdl.KeyboardEvent):
        key = event.key
        down = event.down
        if key == sdl.SDLK_ESCAPE and down:
            self.quit()
