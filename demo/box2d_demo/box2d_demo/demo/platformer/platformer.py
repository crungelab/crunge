from loguru import logger
import glm

from crunge import sdl
from crunge import imgui

from crunge.engine.resource.resource_manager import ResourceManager

from ...map.map_loader import MapLoader
from ...characters import Avatar
from ..physics_demo import PhysicsDemo

from .ball import Ball


class PlatformerDemo(PhysicsDemo):
    def create_view(self):
        super().create_view()
        self.camera.zoom = 2.0

    def reset(self):
        super().reset()
        self.last_mouse = glm.vec2()
        self.create_map()

    def on_mouse_button(self, event: sdl.MouseButtonEvent):
        super().on_mouse_button(event)  # right-click drag handled here
        if event.button == 1 and event.down:
            world = self.camera.unproject(glm.vec2(event.x, event.y))
            logger.debug(f"Creating box at {world}")
            self.create_ball(world)

    def create_ball(self, position):
        ball = Ball(position)
        self.scene.attach(ball)

    def create_map(self):
        map_loader = MapLoader(self.scene)

        tmx_path = ResourceManager().resolve_path(":resources:/tiled/level1.tmx")
        map_loader.load(tmx_path)

        self.character_layer = self.scene.get_layer("pc")

        self.avatar = None
        for node in self.character_layer.root.children:
            logger.debug(f"Checking node: {node}")
            if isinstance(node, Avatar):
                self.avatar = node
                break

        self.controller = self.avatar.control() if self.avatar else None


    '''
    def create_map(self):
        context = BuilderContext(self.scene)

        def create_node_cb(position, sprite, properties):
            return Tile(position, sprite)

        tile_layer_builder = DefaultTileLayerBuilder(
            tile_builder=DefaultTileBuilder(create_node_cb=create_node_cb)
        )
        map_builder = DefaultMapBuilder(tile_layer_builder=tile_layer_builder)
        map_loader = TiledMapLoader(context, map_builder=map_builder)

        tmx_path = ResourceManager().resolve_path(":resources:/tiled/level1.tmx")
        map_loader.load(tmx_path)
    '''

    def _draw(self):
        imgui.begin("Platformer Demo")
        imgui.text("Click to create balls")

        self.draw_stats()
        self.draw_physics_options()

        if imgui.button("Reset"):
            self.reset()

        imgui.end()

        super()._draw()

    '''
    def update(self, delta_time: float):
        self.world.update(1 / 60)
        super().update(delta_time)
    '''

    def recenter_camera(self):
        if self.avatar is None:
            return
        self.camera.position = self.avatar.position
        self.update_camera()
        
    def update(self, delta_time: float):
        self.update_camera(delta_time)
        self.world.update(1 / 60)
        super().update(delta_time)

    def update_camera(self, delta_time: float = 1/60):
        if self.avatar is None:
            return
        velocity = self.avatar.velocity
        #speed = glm.length(velocity) / 128
        speed = glm.length(velocity)

        #logger.debug(f"delta_time: {delta_time}")
        #logger.debug(f"velocity: {velocity}")
        #logger.debug(f"speed: {speed}")

        frustum = self.camera.frustum

        # Compute clamping limits to keep the frustum inside level bounds
        min_x = self.scene.bounds.min.x + (frustum.max.x - frustum.min.x) / 2
        max_x = self.scene.bounds.max.x - (frustum.max.x - frustum.min.x) / 2
        min_y = self.scene.bounds.min.y + (frustum.min.y - frustum.max.y) / 2
        max_y = self.scene.bounds.max.y - (frustum.min.y - frustum.max.y) / 2

        #min_y = max(self.scene.bounds.min.y, min_y)
        # TODO: Hack.
        min_y = min_y + frustum.height

        #logger.debug(f"scene bounds: {self.scene.bounds}")
        #logger.debug(f"frustum: {frustum}")
        #logger.debug(f"min_x: {min_x}")
        #logger.debug(f"max_x: {max_x}")
        #logger.debug(f"min_y: {min_y}")
        #logger.debug(f"max_y: {max_y}")

        camera_position = glm.mix(self.camera.position, self.avatar.position, speed * delta_time)
        camera_x = glm.clamp(camera_position.x, min_x, max_x)
        camera_y = glm.clamp(camera_position.y, min_y, max_y)
        self.camera.position = glm.vec2(camera_x, camera_y)

def main():
    PlatformerDemo().run()


if __name__ == "__main__":
    main()
