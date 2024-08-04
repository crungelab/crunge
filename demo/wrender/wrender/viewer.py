import time
import os, sys
from pathlib import Path
import tkinter

from loguru import logger

from crunge import wgpu, sdl, engine, imgui
from crunge.engine import Renderer

import crunge.wgpu.utils as utils

from .scene_builder import SceneBuilder
from .scene_renderer import SceneRenderer
from .scene import Scene
from .view import View
from .camera import Camera
from .controller.camera import CameraController
from .controller.camera.arcball import ArcballCameraController


#models_root = Path(__file__).parent.parent.parent.parent / "resources" / "models"
models_root = Path(os.environ.get("GLTF_SAMPLE_MODELS"))


class Viewer(engine.App):
    renderer: SceneRenderer
    kWidth = 1024
    kHeight = 768

    def __init__(self):
        super().__init__(self.kWidth, self.kHeight, "WRender", resizable=True)
        self.camera: Camera = None
        self.delta_time = 0

    def create_renderer(self):
        self.renderer = SceneRenderer()

    def create_view(self, scene: Scene):
        logger.debug("Creating view")
        view = View(scene, self.kWidth, self.kHeight).create(self)
        self.show_view(view)

    def open(self):
        logger.debug("Opening scene")
        scene_path = tkinter.filedialog.askopenfilename(initialdir = models_root, title = "Select file", filetypes = (("gltf files","*.gltf"),("glb files","*.glb"),("all files","*.*")))
        scene = SceneBuilder().build(scene_path)
        self.schedule_once(lambda dt: self.show(scene))

    def show(self, scene: Scene):
        logger.debug("Showing scene")
        self.scene = scene
        self.create_view(scene)

        self.camera = self.view.camera
        self.controller = ArcballCameraController(self, self.camera)
        self.controller.activate()

        #self.run()
        return self

    def draw(self, renderer: Renderer):
        """
        imgui.begin("Example: button")
        imgui.button("Button 1")
        imgui.button("Button 2")
        imgui.end()
        """
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
        key = event.keysym.sym
        state = event.state
        if key == sdl.SDLK_ESCAPE and state == 1:
            self.quit()
