from loguru import logger
import glm

from crunge import imgui
from crunge.engine import Renderer

from crunge.engine.resource.resource_manager import ResourceManager

from ..demo import Demo

from ...loader.tiled.builder.builder_context import SceneBuilderContext
from ...loader.tiled.builder.map_builder import DefaultMapBuilder
from ...loader.tiled.tiled_map_loader import TiledMapLoader
'''
from ...loader.tiled.builder.map_builder import MapBuilder
from ...loader.tiled.builder.tile_layer_builder import TileLayerBuilder
from ...loader.tiled.builder.object_group_builder import ObjectGroupBuilder
from ...loader.tiled.builder.tile_builder import DefaultTileBuilder
from ...loader.tiled.builder.object_builder import DefaultObjectBuilder
'''

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
        '''
        tile_layer_builder = TileLayerBuilder(
            context, tile_builder=DefaultTileBuilder(context)
        )
        object_group_builder = ObjectGroupBuilder(
            context, object_builder=DefaultObjectBuilder(context)
        )
        map_builder = MapBuilder(
            context,
            tile_layer_builder=tile_layer_builder,
            object_group_builder=object_group_builder,
        )
        map_loader = TiledMapLoader(context, map_builder=map_builder)
        '''
        tmx_path = ResourceManager().resolve_path(":resources:/tiled/level1.tmx")
        map_loader = TiledMapLoader(context, map_builder=DefaultMapBuilder(context))
        map_loader.load(tmx_path)

    def draw(self, renderer: Renderer):
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
