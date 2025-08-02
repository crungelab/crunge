from loguru import logger
import glm

from crunge import imgui
from crunge.engine import Renderer

from crunge.engine.resource.resource_manager import ResourceManager

from crunge.engine.loader.tiled.builder import BuilderContext
from crunge.engine.loader.tiled.tiled_map_loader import TiledMapLoader

from ..demo import Demo


class StickerKnightDemo(Demo):
    def reset(self):
        super().reset()
        self.create_map()

    def create_view(self):
        super().create_view()
        self.camera.zoom = 2.0

    def create_map(self):
        context = BuilderContext(scene=self.scene)
        map_loader = TiledMapLoader(context)
        tmx_path = ResourceManager().resolve_path(":resources:/sticker-knight/map/sandbox.tmx")
        #tmx_path = ResourceManager().resolve_path(":resources:/sticker-knight/map/sandbox2.tmx")
        map_loader.load(tmx_path)

    def _draw(self):
        imgui.set_next_window_pos((self.width - 256 - 16, 32), imgui.Cond.ONCE)
        imgui.set_next_window_size((256, 256), imgui.Cond.ONCE)

        imgui.begin("Sticker Knight")

        if imgui.button("Reset"):
            self.reset()

        imgui.end()

        super()._draw()


def main():
    StickerKnightDemo().run()


if __name__ == "__main__":
    main()
