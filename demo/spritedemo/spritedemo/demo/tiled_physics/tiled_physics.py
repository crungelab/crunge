from loguru import logger
import glm

from crunge import sdl
from crunge import imgui
from crunge.engine import Renderer
from crunge.engine.d2.physics import DynamicPhysicsEngine
from crunge.engine.d2.physics.draw_options import DrawOptions

from crunge.engine.resource.resource_manager import ResourceManager
from crunge.engine.loader.tiled.builder.builder_context import SceneBuilderContext
from crunge.engine.loader.tiled.tiled_map_loader import TiledMapLoader
from crunge.engine.loader.tiled.builder.map_builder import DefaultMapBuilder
from crunge.engine.loader.tiled.builder.tile_layer_builder import DefaultTileLayerBuilder
from crunge.engine.loader.tiled.builder.tile_builder import DefaultTileBuilder

from ..demo import Demo

from .ball import Ball
from .tile import Tile

class TiledPhysicsDemo(Demo):
    def __init__(self):
        super().__init__()
        self.debug_draw_enabled = False

    def create(self):
        super().create()
        self.draw_options = DrawOptions(self.view.scratch)
        self.reset()
        return self

    def create_view(self):
        super().create_view()
        self.camera.zoom = 2.0

    def reset(self):
        self.scene.clear()
        self.last_mouse = glm.vec2()
        self.physics_engine = DynamicPhysicsEngine().create()
        self.create_map()

    def on_mouse_motion(self, event: sdl.MouseMotionEvent):
        x, y = event.x, event.y
        self.last_mouse = glm.vec2(x, y)

    def on_mouse_button(self, event: sdl.MouseButtonEvent):
        super().on_mouse_button(event)
        button = event.button
        down = event.down
        if button == 1 and down:
            mouse_vec = glm.vec2(event.x, event.y)
            world_vec = self.camera.unproject(mouse_vec)
            x, y = world_vec.x, world_vec.y
            logger.debug(f"Creating ball at {x}, {y}")
            self.create_ball(world_vec)


    def create_ball(self, position):
        ball = Ball(position)
        ball.create()
        self.scene.attach(ball)

    def create_map(self):
        context = SceneBuilderContext(scene=self.scene)

        def create_node_cb(position, sprite, properties):
            return Tile(position, sprite)

        tile_layer_builder = DefaultTileLayerBuilder(context, tile_builder=DefaultTileBuilder(context, create_node_cb=create_node_cb))
        map_builder = DefaultMapBuilder(context, tile_layer_builder=tile_layer_builder)
        map_loader = TiledMapLoader(context, map_builder=map_builder)
        #map_loader = TiledMapLoader(context)

        tmx_path = ResourceManager().resolve_path(":resources:/tiled/level1.tmx")
        map_loader.load(tmx_path)

    def draw(self, renderer: Renderer):        
        imgui.begin("Tiled Physics Demo")

        imgui.text("Click to create balls")

        _, self.debug_draw_enabled = imgui.checkbox("Debug Draw", self.debug_draw_enabled)

        if imgui.button("Reset"):
            self.reset()

        imgui.end()

        if self.debug_draw_enabled:
            self.physics_engine.debug_draw(self.draw_options)

        super().draw(renderer)

    def update(self, delta_time: float):
        self.physics_engine.update(1/60)
        super().update(delta_time)

def main():
    TiledPhysicsDemo().create().run()


if __name__ == "__main__":
    main()
