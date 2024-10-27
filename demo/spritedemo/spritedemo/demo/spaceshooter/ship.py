import math

from loguru import logger
import glm

from crunge.engine.d2.sprite import Sprite, SpriteMaterial
from crunge.engine.d2.node_2d import Node2D
from crunge.engine.loader.texture_atlas_loader import TextureAtlasLoader

from ...model_2d import DynamicModel2D
from ...geom import BallGeom

from .collision_type import CollisionType
from .thruster import Thruster
from .laser import Laser

class Thruster(Node2D):
    def __init__(self, body, position: glm.vec2, force: glm.vec2, angular_velocity: float = 0) -> None:
        super().__init__(position)
        self.body = body
        self.active = False
        self.force = force
        self.angular_velocity = angular_velocity

    def on(self):
        self.active = True

    def off(self):
        self.active = False

    def update(self, dt):
        super().update(dt)
        if self.active:
            self.body.apply_force_at_local_point(tuple(self.force), tuple(self.position))
            self.body.angular_velocity = self.angular_velocity


class Ship(DynamicModel2D):
    def __init__(self, position: glm.vec2) -> None:
        super().__init__(position, geom=BallGeom)
        atlas = TextureAtlasLoader().load(":resources:/spaceshooter/sheet.xml")
        logger.debug(f"atlas: {atlas}")
        
        texture = atlas.get("playerShip1_orange.png")
        material = SpriteMaterial(texture)

        self.vu = Sprite(material)
        self.size = texture.size

        self.rear_thruster: Thruster = None
        self.front_thruster: Thruster = None
        self.left_thruster: Thruster = None
        self.right_thruster: Thruster = None

    def add_shape(self, shape):
        shape.collision_type = CollisionType.SHIP
        super().add_shape(shape)

    def _create(self):
        super()._create()
        self.front_thruster = Thruster(self.body, glm.vec2(0, self.size.y / 2), glm.vec2(0, -100))
        self.attach(self.front_thruster)

        self.rear_thruster = Thruster(self.body, glm.vec2(0, -self.size.y / 2), glm.vec2(0, 100))
        self.attach(self.rear_thruster)

        self.left_thruster = Thruster(self.body, glm.vec2(-self.size.x / 2, 0), glm.vec2(-100, 0), 5)
        self.attach(self.left_thruster)

        self.right_thruster = Thruster(self.body, glm.vec2(self.size.x / 2, 0), glm.vec2(100, 0), -5)
        self.attach(self.right_thruster)

    def update(self, delta_time: float):
        super().update(delta_time)
        if not self.left_thruster.active and not self.right_thruster.active:
            self.body.angular_velocity = 0

    def fire(self):
        spawn_distance = 100  # Adjust based on your game's scale
        missile_speed = 1000  # Adjust missile speed as needed

        # Calculate the missile's spawn position
        rotation = self._rotation + math.pi / 2
        direction = glm.vec2(math.cos(rotation), math.sin(rotation))
        position = self.position + direction * spawn_distance

        laser = Laser(position, self.angle, missile_speed).create()
        self.scene.root.attach(laser)