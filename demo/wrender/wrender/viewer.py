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

models_root = Path(os.environ.get("GLTF_SAMPLE_ASSETS")) / "Models"


class Viewer(engine.App):
    view: View3D

    def __init__(self):
        super().__init__(title="WRender", resizable=True)
        self.delta_time = 0

    @property
    def camera(self):
        return self.view.camera
    
    def create_viewport(self):
        self.viewport = SurfaceViewport(self.size, self.window, use_depth_stencil=True, use_msaa=True)

    def create_view(self, scene: Scene3D):
        logger.debug("Creating view")
        self.view = View3D(scene).config(window=self).create()

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

        # Step 1: Calculate the size and center of the model
        bounds = self.scene.bounds
        size = bounds.size
        #center = self.scene.root.bounds.center
        center = bounds.center

        # Step 2: Determine the maximum extent of the model
        max_extent = max(size.x, size.y, size.z)
        logger.debug(f"Model size: {size}, center: {center}, max extent: {max_extent}")

        # Step 3: Set up the camera's field of view (FOV) in radians
        fov = glm.radians(45.0)  # 45 degrees

        # Step 4: Calculate the camera distance
        camera_distance = max_extent / (2 * math.tan(fov / 2))

        # Optional: Add some padding factor to move the camera further back
        padding_factor = 1.5
        camera_distance *= padding_factor

        # Step 5: Position the camera along the z-axis, looking at the model
        camera_position = glm.vec3(center.x, center.y, center.z + camera_distance)
        logger.debug(f"Camera position: {camera_position}")
        target = center

        # Step 6: Define the near and far planes
        # Set near plane based on a fraction of camera distance or a minimum value
        #near_plane = max(0.1, camera_distance * 0.01)
        near_plane = max_extent * 0.01

        # Calculate distance to farthest point from the camera to determine the far plane
        farthest_point = max_extent - center
        far_plane = glm.length(camera_position - (center + farthest_point)) + max_extent
        far_plane = far_plane * 10

        self.camera.position = camera_position
        self.camera.near = near_plane
        self.camera.far = far_plane
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
