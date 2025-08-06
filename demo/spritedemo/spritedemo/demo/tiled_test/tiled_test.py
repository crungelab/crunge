from loguru import logger
import glm

from crunge import imgui

from crunge.engine.resource.resource_manager import ResourceManager
from crunge.engine.loader.tiled.builder import BuilderContext
from crunge.engine.loader.tiled.builder.map_builder import DefaultMapBuilder
from crunge.engine.loader.tiled.tiled_map_loader import TiledMapLoader

from ..demo import Demo


class TiledTestDemo(Demo):
    def reset(self):
        super().reset()
        self.create_map()

    def center_camera(self):
        pass
    
    def create_view(self):
        super().create_view()
        self.camera.zoom = 2.0

    def create_map(self):
        context = BuilderContext(scene=self.scene)
        tmx_path = ResourceManager().resolve_path(":resources:/tiled/test.tmx")
        map_loader = TiledMapLoader(context, map_builder=DefaultMapBuilder(context))
        map_loader.load(tmx_path)

    def _draw(self):
        self.view.scratch.draw_circle(glm.vec2(0, 0), 10, color=glm.vec4(1, 0, 0, 1))
        imgui.set_next_window_pos((self.width - 256 - 16, 32), imgui.Cond.ONCE)
        imgui.set_next_window_size((256, 256), imgui.Cond.ONCE)

        imgui.begin("Tiled")

        if imgui.button("Reset"):
            self.reset()

        imgui.end()

        super()._draw()


def main():
    TiledTestDemo().run()


if __name__ == "__main__":
    main()
