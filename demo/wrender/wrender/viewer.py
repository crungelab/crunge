import time
import os, sys
from pathlib import Path
import tkinter
import tkinter.filedialog

from loguru import logger
import glm

from crunge import sdl
from crunge import wgpu
from crunge import imgui
from crunge import engine

from crunge.engine import Renderer

from crunge.engine.gltf import GltfImporter

from crunge.engine.d3.scene_renderer_3d import SceneRenderer3D
from crunge.engine.d3.scene_3d import Scene3D
from crunge.engine.d3.camera_3d import Camera3D
from crunge.engine.d3.controller.camera.arcball import ArcballCameraController

from .view import View

#models_root = Path(__file__).parent.parent.parent.parent / "resources" / "models"
models_root = Path(os.environ.get("GLTF_SAMPLE_MODELS"))


class Viewer(engine.App):
    renderer: SceneRenderer3D
    kWidth = 1024
    kHeight = 768

    def __init__(self):
        super().__init__(glm.ivec2(self.kWidth, self.kHeight), "WRender", resizable=True)
        self.camera: Camera3D = None
        self.delta_time = 0

    def create_renderer(self):
        self.renderer = SceneRenderer3D()

    def create_view(self, scene: Scene3D):
        logger.debug("Creating view")
        view = View(scene, self.size).create(self)
        self.show_view(view)

    def open(self):
        logger.debug("Opening scene")
        scene_path = tkinter.filedialog.askopenfilename(initialdir = models_root, title = "Select file", filetypes = (("gltf files","*.gltf"),("glb files","*.glb"),("all files","*.*")))
        if not scene_path:
            return
        scene = GltfImporter().load(scene_path)
        self.schedule_once(lambda dt: self.show(scene))

    def show(self, scene: Scene3D):
        logger.debug("Showing scene")
        self.scene = scene
        self.create_view(scene)

        self.camera = self.view.camera
        self.controller = ArcballCameraController(self, self.camera)
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
        key = event.key
        state = event.state
        if key == sdl.SDLK_ESCAPE and state == 1:
            self.quit()
