from pathlib import Path
import math

from loguru import logger
import glm

from crunge import sdl, imgui
from crunge.engine import Renderer

from ..demo import Demo
from ...sprite import Sprite
from ...node_2d import Node2D
from ...texture_atlas_kit import TextureAtlasKit
from ...physics import DynamicPhysicsEngine

from .ship import Ship
from .meteor import Meteor


class SpaceShooter(Demo):
    def __init__(self):
        super().__init__()
        self.scale = 1.0
        self.camera_target = glm.vec2(self.width / 2, self.height / 2)

        self.physics_engine = DynamicPhysicsEngine(gravity=(0, 0))
        self.physics_engine.create()

        self.create_ship(glm.vec2(self.width / 2, self.height / 2))
        self.create_meteor(glm.vec2(self.width / 4, self.height / 4))

    def create_ship(self, position):
        ship = self.ship = Ship(position).create()
        self.node = ship
        self.scene.add_child(ship)

    def create_meteor(self, position):
        meteor = Meteor(position).create()
        self.scene.add_child(meteor)

    def reset(self):
        self.scale = 1.0

    def draw(self, renderer: Renderer):
        # imgui.set_next_window_position(288, 32, imgui.ONCE)
        imgui.set_next_window_pos((self.width - 256 - 16, 32), imgui.COND_ONCE)
        imgui.set_next_window_size((256, 256), imgui.COND_ONCE)

        imgui.begin("Ship")

        # Scale
        changed, self.scale = imgui.drag_float("Scale", self.scale, 0.1)
        self.node.scale = glm.vec2(self.scale, self.scale)

        if imgui.button("Reset"):
            self.reset()

        imgui.end()

        super().draw(renderer)

    def update(self, delta_time: float):
        # super().update(delta_time)
        self.physics_engine.update(1 / 60)
        self.scene.update(delta_time)
        threshold_distance = 200.0
        lerp_factor = 10  # Speed of camera movement towards the target

        # Calculate the target position based on the ship's position and the dead zone
        self.camera_target = self.calculate_target_position(
            self.camera.position, self.ship.position, threshold_distance
        )

        # Update the camera position towards the target
        self.camera.position = self.update_camera(
            self.camera.position, self.camera_target, lerp_factor, delta_time
        )
        super().update(delta_time)

    def calculate_target_position(
        self, camera_position, ship_position, threshold_distance
    ):
        direction = ship_position - camera_position
        distance_from_camera = glm.length(direction)

        if distance_from_camera > threshold_distance:
            return ship_position
        else:
            return self.camera_target

    def update_camera(self, camera_position, target_position, lerp_factor, delta_time):
        camera_position = glm.lerp(
            camera_position, target_position, lerp_factor * delta_time
        )
        camera_position.x = round(camera_position.x, 2)
        camera_position.y = round(camera_position.y, 2)
        return camera_position

    def on_key(self, event: sdl.KeyboardEvent):
        key = event.keysym.sym
        state = event.state
        if key == sdl.SDLK_s:
            if state == 1:
                self.ship.front_thruster.on()
            else:
                self.ship.front_thruster.off()
        if key == sdl.SDLK_w:
            if state == 1:
                self.ship.rear_thruster.on()
            else:
                self.ship.rear_thruster.off()
        elif key == sdl.SDLK_a:
            if state == 1:
                self.ship.left_thruster.on()
            else:
                self.ship.left_thruster.off()
        elif key == sdl.SDLK_d:
            if state == 1:
                self.ship.right_thruster.on()
            else:
                self.ship.right_thruster.off()
        elif key == sdl.SDLK_SPACE:
            if state == 1:
                self.ship.fire()


def main():
    SpaceShooter().create().run()


if __name__ == "__main__":
    main()
