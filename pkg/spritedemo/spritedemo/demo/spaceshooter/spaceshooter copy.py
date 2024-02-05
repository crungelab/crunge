from pathlib import Path

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
        self.alpha = 255
        self.color_enabled = True
        self.color = 1, 1, 1

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
        self.alpha = 255
        self.color_enabled = True
        self.color = 1, 1, 1

    def draw(self, renderer: Renderer):
        # imgui.set_next_window_position(288, 32, imgui.ONCE)
        imgui.set_next_window_pos((self.width - 256 - 16, 32), imgui.COND_ONCE)
        imgui.set_next_window_size((256, 256), imgui.COND_ONCE)

        imgui.begin("Ship")

        # Rotation
        '''
        changed, self.angle = imgui.drag_float(
            "Angle",
            self.angle,
        )
        self.node.angle = self.angle
        '''
        
        # Scale
        changed, self.scale = imgui.drag_float("Scale", self.scale, 0.1)
        self.node.scale = glm.vec2(self.scale, self.scale)

        #TODO: Implement alpha and color
        '''
        # Alpha
        changed, self.alpha = imgui.drag_int("Alpha", self.alpha, 1, 0, 255)
        self.sprite.alpha = self.alpha

        # Color
        _, self.color_enabled = imgui.checkbox("Tint", self.color_enabled)
        if self.color_enabled:
            changed, self.color = imgui.color_edit3("Color", *self.color)
            self.sprite.color = (
                int(self.color[0] * 255),
                int(self.color[1] * 255),
                int(self.color[2] * 255),
            )
        else:
            self.sprite.color = 255, 255, 255
        '''

        if imgui.button("Reset"):
            self.reset()

        imgui.end()

        super().draw(renderer)

    def update(self, delta_time: float):
        super().update(delta_time)
        #self.scene.update(delta_time)
        self.physics_engine.update(1/60)
        self.scene.update(delta_time)
        #self.camera.position = self.ship.position
        #self.camera.position = self.update_camera(self.camera.position, self.ship.position, 100, 0.1, delta_time)
        threshold_distance = 200
        damping_factor = 100.0

        self.camera.position = self.update_camera_with_damping(self.camera.position, self.ship.position, damping_factor, delta_time)
        #self.camera.position = self.update_camera_with_damping(self.camera.position, self.ship.position, threshold_distance, damping_factor, delta_time)

    '''
    def update_camera_with_damping(self, camera_position, ship_position, threshold_distance, damping_factor, delta_time):
        # Calculate the vector from the camera to the ship
        direction = ship_position - camera_position
        distance = glm.length(direction)
        if distance > threshold_distance and distance > 0.1:
            # Apply damping based on the delta time and damping factor
            displacement = direction * (1 - glm.exp(-damping_factor * delta_time))
            new_camera_position = camera_position + displacement

            return new_camera_position
        else:
            return camera_position
    '''
    def update_camera_with_damping(self, camera_position, ship_position, damping_factor, delta_time):
        # Calculate the vector from the camera to the ship
        direction = ship_position - camera_position
        # Apply damping based on the delta time and damping factor
        displacement = direction * (1 - glm.exp(-damping_factor * delta_time))
        new_camera_position = camera_position + displacement

        return new_camera_position

    '''
    def update_camera(self, camera_position, ship_position, threshold_distance, lerp_factor, delta_time):
        direction = ship_position - camera_position
        distance = glm.length(direction)

        #if distance > threshold_distance:
        if distance > threshold_distance and distance > 0.1:
            # Adjust lerp_factor by delta_time to make the movement frame rate independent
            adjusted_lerp = 1 - pow(1 - lerp_factor, delta_time * 60)  # Assuming 60 is your target FPS
            direction = glm.normalize(direction) * distance * adjusted_lerp
            new_camera_position = camera_position + direction
            return new_camera_position
        else:
            return camera_position
    '''

    '''
    def update_camera(self, camera_position, ship_position, threshold_distance, lerp_factor):
        # Calculate the vector from the camera to the ship
        direction = ship_position - camera_position
        distance = glm.length(direction)

        if distance > threshold_distance:
            # Normalize the direction vector and scale it by the lerp factor
            direction = glm.normalize(direction) * distance * lerp_factor
            # Update the camera position
            new_camera_position = camera_position + direction
            return new_camera_position
        else:
            # If the ship is within the threshold, don't move the camera
            return camera_position
    '''

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

def main():
    SpaceShooter().create().run()


if __name__ == "__main__":
    main()
