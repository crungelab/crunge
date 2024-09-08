from loguru import logger
import glm

from crunge import sdl
from crunge import imgui
from crunge.engine import Renderer

from ..demo import Demo
from ...physics import DynamicPhysicsEngine

from .ship import Ship
from .zone import Zone
from .explosion import Explosion

from .collision_type import CollisionType

class SpaceShooter(Demo):
    def __init__(self):
        super().__init__()
        self.reset()

    def reset(self):
        self.scene.clear()
        self.camera_target = glm.vec2(0, 0)

        self.create_physics_engine()

        self.create_ship(glm.vec2(0, 0))
        zone = Zone(self.scene, glm.vec2(0, 0), glm.vec2(self.width * 2, self.height * 2)).create()

    def create_physics_engine(self):
        self.physics_engine = engine = DynamicPhysicsEngine(gravity=(0, 0))
        engine.create()

        def laser_laser_collision(arbiter, space, data):
            return False
        
        def laser_asteroid_collision(arbiter, space, data):
            laser_shape, asteroid_shape = arbiter.shapes
            laser_model = laser_shape.body.model
            asteroid_model = asteroid_shape.body.model
            laser_model.destroy()
            asteroid_model.destroy()
            explosion = Explosion(asteroid_model.position, glm.vec2(100, 100))
            self.scene.root.attach(explosion)
            return False

        handler = engine.space.add_collision_handler(CollisionType.LASER, CollisionType.LASER)  # Replace with your collision types
        handler.begin = laser_laser_collision

        handler = engine.space.add_collision_handler(CollisionType.LASER, CollisionType.METEOR)  # Replace with your collision types
        handler.begin = laser_asteroid_collision

    def create_view(self):
        super().create_view()
        self.camera.zoom = .5
        self.camera.position = glm.vec2(0, 0)

    def create_ship(self, position):
        ship = self.ship = Ship(position).create()
        self.node = ship
        self.scene.root.attach(ship)

    def draw(self, renderer: Renderer):
        imgui.set_next_window_pos((self.width - 256 - 16, 32), imgui.COND_ONCE)
        imgui.set_next_window_size((256, 256), imgui.COND_ONCE)

        imgui.begin("Ship")

        if imgui.button("Reset"):
            self.reset()

        imgui.end()

        super().draw(renderer)

    def update(self, delta_time: float):
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
        key = event.key
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
