from crunge import demo

from pathlib import Path
import timeit

from loguru import logger
import glm

from crunge import sdl
from crunge import imgui

from crunge.engine.resource.resource_manager import ResourceManager
from crunge.engine.d2.scene import Scene2D
from crunge.engine.d2.screen import SceneScreen2D


class Page(SceneScreen2D):
    def __init__(self, scene: Scene2D, name: str, title: str, version: str):
        super().__init__(scene)
        self.name = name
        self.title = title
        self.version = version

        self.repo_root = Path(__file__).parent.parent.parent.parent
        self.resource_root = self.repo_root / "resources"
        self.depot_root = self.repo_root / "depot"
        self.spine_root = self.depot_root / "spine-runtimes"

        ResourceManager().add_path_variables(
            resources=self.resource_root,
            images=self.resource_root / "images",
            spines=self.spine_root / "examples",
        )

    def on_key(self, event: sdl.KeyboardEvent):
        key = event.key
        down = event.down
        if key == sdl.SDLK_ESCAPE and down:
            self.quit()

    def draw_stats(self):
        # Display timings
        imgui.text(f"Update time: {self.update_time:.4f}")
        imgui.text(f"Frame time: {self.frame_time:.4f}")
