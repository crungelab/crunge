from loguru import logger
import glm

from crunge import sdl
from crunge import imgui
from crunge import box2d as b2

from box2d_demo.physics import DynamicPhysicsEngine
from crunge.engine.d2.settings_2d import Settings2D

from ..physics_demo import PhysicsDemo

from .ship import Ship
from .zone import Zone
from .explosion import Explosion

from .collision_type import CollisionType


class SpaceShooter(PhysicsDemo):
    def reset(self):
        super().reset()
        self.controller = None
        self.camera_target = glm.vec2(0, 0)

        self.create_physics_engine()

        self.create_ship(glm.vec2(0, 0))

        ppu = Settings2D().ppu
        width_units = self.width / ppu  # viewport width, converted to units
        height_units = self.height / ppu  # viewport height, converted to units

        zone = Zone(
            self.scene, glm.vec2(0, 0), glm.vec2(width_units * 2, height_units * 2)
        ).create()

    def center_camera(self):
        pass

    def create_physics_engine(self):
        self.world = DynamicPhysicsEngine(gravity=glm.vec2(0, 0))
        self.world.make_current()

    def handle_collisions(self):
        events = self.world.get_contact_events()
        destroyed = (
            set()
        )  # guard against double-destroy if a node shows up in >1 event this step

        for event in events.get_begin_events():
            shape_a = event.shape_id_a
            shape_b = event.shape_id_b

            node_a = shape_a.user_data
            node_b = shape_b.user_data

            types = {shape_a.user_material, shape_b.user_material}

            logger.debug(f"Collision between {node_a} and {node_b}, types: {types}")

            if (
                node_a is None
                or node_b is None
                or node_a in destroyed
                or node_b in destroyed
            ):
                continue

            if types == {CollisionType.LASER}:
                continue  # laser/laser: no-op, same as before

            if types == {CollisionType.LASER, CollisionType.METEOR}:
                laser = (
                    node_a if shape_a.user_material == CollisionType.LASER else node_b
                )
                asteroid = (
                    node_a if shape_a.user_material == CollisionType.METEOR else node_b
                )
                self._destroy_pair(laser, asteroid, destroyed)

            elif types == {CollisionType.SHIP, CollisionType.METEOR}:
                ship = node_a if shape_a.user_material == CollisionType.SHIP else node_b
                asteroid = (
                    node_a if shape_a.user_material == CollisionType.METEOR else node_b
                )
                self._destroy_pair(
                    ship, asteroid, destroyed, color=glm.vec4(1.0, 0.0, 0.0, 1.0)
                )

    def _destroy_pair(self, actor_node, asteroid_node, destroyed, color=None):
        logger.debug(f"Destroying {actor_node} and {asteroid_node}")
        position = asteroid_node.position
        actor_node.destroy()
        asteroid_node.destroy()
        destroyed.add(actor_node)
        destroyed.add(asteroid_node)
        explosion = Explosion(position, color) if color else Explosion(position)
        self.scene.attach(explosion)

    def create_view(self):
        super().create_view()
        self.camera.zoom = 2
        self.camera.position = glm.vec2(0, 0)

    def create_ship(self, position):
        ship = self.ship = Ship(position).create()
        self.node = ship
        self.scene.attach(ship)

    def _draw(self):
        imgui.set_next_window_pos((self.width - 256 - 16, 32), imgui.Cond.ONCE)
        imgui.set_next_window_size((256, 256), imgui.Cond.ONCE)
        imgui.begin("Ship")
        self.draw_stats()
        if imgui.button("Reset"):
            self.reset()
        imgui.end()
        super()._draw()

    def update(self, delta_time: float):
        self.world.update(delta_time)
        self.handle_collisions()

        base_lerp_factor = 5.0
        speed_factor = 0.001
        ship_speed = b2.length(self.ship.body.linear_velocity)
        threshold_distance = 400.0

        self.camera_target = self.calculate_target_position(
            self.camera.position, self.ship.position, threshold_distance
        )
        lerp_factor = base_lerp_factor + ship_speed * speed_factor
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
