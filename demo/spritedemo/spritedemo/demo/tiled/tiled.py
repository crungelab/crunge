from loguru import logger
import glm

from crunge import imgui
from crunge.engine import Renderer

from crunge.engine.resource.resource_manager import ResourceManager
from crunge.engine.loader.tiled.builder.builder_context import SceneBuilderContext
from crunge.engine.loader.tiled.builder.map_builder import DefaultMapBuilder
from crunge.engine.loader.tiled.tiled_map_loader import TiledMapLoader

from ..demo import Demo


class TiledLoaderDemo(Demo):
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        self.scene.clear()
        self.create_map()

    def create_view(self):
        super().create_view()
        self.camera.zoom = 2.0

    def create_map(self):
        context = SceneBuilderContext(scene=self.scene)
        tmx_path = ResourceManager().resolve_path(":resources:/tiled/level1.tmx")
        map_loader = TiledMapLoader(context, map_builder=DefaultMapBuilder(context))
        map_loader.load(tmx_path)

    def draw(self, renderer: Renderer):
        self.view.scratch.draw_circle(glm.vec2(0, 0), 10, color=glm.vec4(1, 0, 0, 1))
        imgui.set_next_window_pos((self.width - 256 - 16, 32), imgui.Cond.ONCE)
        imgui.set_next_window_size((256, 256), imgui.Cond.ONCE)

        imgui.begin("Tiled")

        if imgui.button("Reset"):
            self.reset()

        imgui.end()

        super().draw(renderer)


def main():
    TiledLoaderDemo().create().run()


if __name__ == "__main__":
    main()
