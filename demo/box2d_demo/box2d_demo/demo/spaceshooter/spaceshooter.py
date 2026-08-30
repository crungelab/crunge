from loguru import logger
import glm

from crunge import sdl
from crunge import imgui
from crunge import box2d as b2

from crunge.engine.d2.physics import PhysicsWorld2D
from crunge.engine.d2.physics.world import Contact
from crunge.engine.d2.settings_2d import Settings2D

from ..physics_demo import PhysicsDemo

from .ship import Ship
from .zone import Zone
from .explosion import Explosion

from .physics_material import SHIP, LASER, METEOR

BASE_LERP_FACTOR = 5.0
SPEED_FACTOR = 0.001
THRESHOLD_DISTANCE = 4.0

EXPLOSION_RED = glm.vec4(1.0, 0.0, 0.0, 1.0)


class SpaceShooter(PhysicsDemo):
    def reset(self):
        super().reset()
        self.controller = None
        self.camera_target = glm.vec2(0, 0)
        self._destroyed = set()

        self.create_world()
        self.create_ship(glm.vec2(0, 0))

        ppu = Settings2D().ppu
        width_units = self.width / ppu
        height_units = self.height / ppu

        Zone(
            self.scene, glm.vec2(0, 0), glm.vec2(width_units * 2, height_units * 2)
        ).create()

    def center_camera(self):
        pass

    def create_world(self):
        self.world = PhysicsWorld2D(gravity=glm.vec2(0, 0))
        self.world.make_current()
        self.world.contact_began.connect(self.on_contact_began)

    def create_ship(self, position):
        ship = self.ship = Ship(position).seat()
        self.node = ship
        self.scene.attach(ship)

    # -- collisions --------------------------------------------------------

    def on_contact_began(self, contact: Contact):
        shape_a, shape_b = contact.shape_a, contact.shape_b
        node_a, node_b = shape_a.user_data, shape_b.user_data

        if node_a is None or node_b is None:
            return
        if node_a in self._destroyed or node_b in self._destroyed:
            return

        materials = {shape_a.user_material, shape_b.user_material}
        logger.debug(f"Collision between {node_a} and {node_b}: {materials}")

        def pick(material_id):
            return node_a if shape_a.user_material == material_id else node_b

        if materials == {LASER.id, METEOR.id}:
            self._destroy_pair(pick(LASER.id), pick(METEOR.id))

        elif materials == {SHIP.id, METEOR.id}:
            self._destroy_pair(pick(SHIP.id), pick(METEOR.id), color=EXPLOSION_RED)

    def _destroy_pair(self, actor_node, asteroid_node, color=None):
        # A node can still be queued twice via two different shape pairs in
        # one batch; idempotent destroy() is the real backstop.
        if actor_node in self._destroyed or asteroid_node in self._destroyed:
            return

        logger.debug(f"Destroying {actor_node} and {asteroid_node}")
        position = asteroid_node.position

        actor_node.destroy()
        asteroid_node.destroy()
        self._destroyed.add(actor_node)
        self._destroyed.add(asteroid_node)

        explosion = Explosion(position, color) if color else Explosion(position)
        self.scene.attach(explosion)

    # -- frame -------------------------------------------------------------

    def create_display(self):
        super().create_display()
        self.camera.zoom = 2
        self.camera.position = glm.vec2(0, 0)

    def update(self, delta_time: float):
        super().update(delta_time)
        self._destroyed.clear()

        if self.ship.is_destroyed:
            return

        ship_speed = b2.length(self.ship.physics.body.linear_velocity)

        self.camera_target = self.calculate_target_position(
            self.camera.position, self.ship.position, THRESHOLD_DISTANCE
        )
        lerp_factor = BASE_LERP_FACTOR + ship_speed * SPEED_FACTOR
        self.camera.position = self.update_camera(
            self.camera.position, self.camera_target, lerp_factor, delta_time
        )

    def calculate_target_position(
        self, camera_position, ship_position, threshold_distance
    ):
        direction = ship_position - camera_position
        if glm.length(direction) > threshold_distance:
            return ship_position
        return self.camera_target

    def update_camera(self, camera_position, target_position, lerp_factor, delta_time):
        return glm.lerp(
            camera_position, target_position, lerp_factor * delta_time
        )

    def _draw(self):
        imgui.set_next_window_pos((self.width - 256 - 16, 32), imgui.Cond.ONCE)
        imgui.set_next_window_size((256, 256), imgui.Cond.ONCE)
        imgui.begin("Ship")
        self.draw_stats()
        if imgui.button("Reset"):
            self.reset()
        imgui.end()
        super()._draw()

    def on_key(self, event: sdl.KeyboardEvent):
        super().on_key(event)

        if self.ship.is_destroyed:
            return

        key, down, repeat = event.key, event.down, event.repeat

        if key == sdl.SDLK_s:
            self.ship.front_thruster.on() if down else self.ship.front_thruster.off()
        elif key == sdl.SDLK_w:
            self.ship.rear_thruster.on() if down else self.ship.rear_thruster.off()
        elif key == sdl.SDLK_a:
            self.ship.left_thruster.on() if down else self.ship.left_thruster.off()
        elif key == sdl.SDLK_d:
            self.ship.right_thruster.on() if down else self.ship.right_thruster.off()
        elif key == sdl.SDLK_SPACE:
            if down and not repeat:
                self.ship.fire()


def main():
    SpaceShooter().run()


if __name__ == "__main__":
    main()