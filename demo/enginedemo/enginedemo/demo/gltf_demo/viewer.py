import os
import math
from pathlib import Path
import tkinter
import tkinter.filedialog

from loguru import logger
import glm

from crunge import sdl
from crunge import engine
from crunge import imgui

from crunge.engine import RenderOptions, Renderer, Scheduler
from crunge.engine.viewport import SurfaceViewport

from crunge.engine.loader.gltf import GltfLoader

from crunge.engine.d3.scene_3d import Scene3D
from crunge.engine.d3.camera_3d import Camera3D
from crunge.engine.d3.controller.camera.arcball import ArcballCameraController

from crunge.engine.d3.view_3d import View3D
from crunge.engine.d3.director_3d import Director3D

#models_root = Path(__file__).parent.parent.parent.parent / "resources" / "models"
models_root = Path(os.environ.get("GLTF_SAMPLE_ASSETS"))


class Viewer(engine.App):
    view: View3D

    def __init__(self):
        super().__init__(title="Gltf Viewer", resizable=True)
        self.render_options = RenderOptions(use_depth_stencil=True, use_msaa=True)
        self.delta_time = 0

    @property
    def camera(self):
        return self.view.camera

    def create_viewport(self):
        self.viewport = SurfaceViewport(self.size, self.window, self.render_options)

    def create_view(self, scene: Scene3D):
        logger.debug("Creating view")
        self.view = View3D(scene)

    def open(self):
        logger.debug("Opening scene")
        scene_path = tkinter.filedialog.askopenfilename(initialdir = models_root, title = "Select file", filetypes = (("gltf files","*.gltf"),("glb files","*.glb"),("all files","*.*")))
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
                    exit(1)

                imgui.end_menu()

            # View
            if imgui.begin_menu("View", True):
                imgui.end_menu()

            imgui.end_main_menu_bar()

    def on_key(self, event: sdl.KeyboardEvent):
        super().on_key(event)
        key = event.key
        down = event.down
        if key == sdl.SDLK_ESCAPE and down:
            self.quit()
