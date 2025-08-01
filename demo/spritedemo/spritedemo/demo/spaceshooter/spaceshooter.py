from loguru import logger
import glm

from crunge import sdl
from crunge import imgui
from crunge.engine import Renderer
from crunge.engine.d2.physics import DynamicPhysicsEngine

from ..demo import Demo

from .ship import Ship
from .zone import Zone
from .explosion import Explosion

from .collision_type import CollisionType


class SpaceShooter(Demo):
    def reset(self):
        super().reset()
        #self.scene.clear()
        self.camera_target = glm.vec2(0, 0)

        self.create_physics_engine()

        self.create_ship(glm.vec2(0, 0))
        zone = Zone(
            self.scene, glm.vec2(0, 0), glm.vec2(self.width * 2, self.height * 2)
        ).create()

    def center_camera(self):
        pass

    def create_physics_engine(self):
        self.physics_engine = engine = DynamicPhysicsEngine(gravity=(0, 0))
        engine.create()

        def laser_laser_collision(arbiter, space, data):
            return False

        def laser_asteroid_collision(arbiter, space, data):
            laser_shape, asteroid_shape = arbiter.shapes
            laser_node = laser_shape.body.node
            asteroid_node = asteroid_shape.body.node
            laser_node.destroy()
            asteroid_node.destroy()
            explosion = Explosion(asteroid_node.position)
            self.scene.attach(explosion)
            return False

        def ship_asteroid_collision(arbiter, space, data):
            ship_shape, asteroid_shape = arbiter.shapes
            ship_node = ship_shape.body.node
            asteroid_node = asteroid_shape.body.node
            ship_node.destroy()
            asteroid_node.destroy()
            explosion = Explosion(asteroid_node.position, glm.vec4(1.0, 0.0, 0.0, 1.0))
            self.scene.attach(explosion)
            return False

        engine.space.on_collision(
            CollisionType.LASER, CollisionType.LASER, begin=laser_laser_collision
        )

        engine.space.on_collision(
            CollisionType.LASER, CollisionType.METEOR, begin=laser_asteroid_collision
        )

        engine.space.on_collision(
            CollisionType.SHIP, CollisionType.METEOR, begin=ship_asteroid_collision
        )

    def create_view(self):
        super().create_view()
        self.camera.zoom = 2
        self.camera.position = glm.vec2(0, 0)

    def create_ship(self, position):
        ship = self.ship = Ship(position).create()
        self.node = ship
        self.scene.attach(ship)

    def draw(self, renderer: Renderer):
        imgui.set_next_window_pos((self.width - 256 - 16, 32), imgui.Cond.ONCE)
        imgui.set_next_window_size((256, 256), imgui.Cond.ONCE)

        imgui.begin("Ship")

        self.draw_stats()
        
        if imgui.button("Reset"):
            self.reset()

        imgui.end()

        super().draw(renderer)

    def update(self, delta_time: float):
        self.physics_engine.update(1 / 60)

        base_lerp_factor = 5.0  # Base speed of camera movement
        # speed_factor = 0.01      # Factor to scale with ship's speed
        speed_factor = 0.001  # Factor to scale with ship's speed

        # Get the ship's speed
        ship_speed = glm.length(self.ship.body.velocity)

        # threshold_distance = 200.0
        threshold_distance = 400.0

        # Calculate the target position based on the ship's position and the dead zone
        self.camera_target = self.calculate_target_position(
            self.camera.position, self.ship.position, threshold_distance
        )

        # Adjust lerp_factor based on the ship's speed
        lerp_factor = base_lerp_factor + ship_speed * speed_factor

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
        return camera_position

    def on_key(self, event: sdl.KeyboardEvent):
        super().on_key(event)
        key = event.key
        down = event.down
        repeat = event.repeat
        if key == sdl.SDLK_s:
            if down:
                self.ship.front_thruster.on()
            else:
                self.ship.front_thruster.off()
        if key == sdl.SDLK_w:
            if down:
                self.ship.rear_thruster.on()
            else:
                self.ship.rear_thruster.off()
        elif key == sdl.SDLK_a:
            if down:
                self.ship.left_thruster.on()
            else:
                self.ship.left_thruster.off()
        elif key == sdl.SDLK_d:
            if down:
                self.ship.right_thruster.on()
            else:
                self.ship.right_thruster.off()
        elif key == sdl.SDLK_SPACE:
            if down and not repeat:
                self.ship.fire()


def main():
    SpaceShooter().run()


if __name__ == "__main__":
    main()
