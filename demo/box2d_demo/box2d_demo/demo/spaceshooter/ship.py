import math

from loguru import logger

import glm
from crunge import box2d as b2

from crunge.engine.d2.sprite import SpriteVu
from crunge.engine.d2.node_2d import Node2D
from crunge.engine.loader.sprite.xml_sprite_atlas_loader import XmlSpriteAtlasLoader

from box2d_demo.entity import DynamicEntity2D
from box2d_demo.physics.geom import BallGeom

from .collision_type import CollisionType
from .thruster import Thruster
from .laser import Laser


class Ship(DynamicEntity2D):
    def __init__(self, position: glm.vec2) -> None:
        atlas = XmlSpriteAtlasLoader().load(":resources:/spaceshooter/sheet.xml")
        logger.debug(f"atlas: {atlas}")
        
        sprite = atlas.get("playerShip1_orange.png")

        super().__init__(position, vu=SpriteVu(), model=sprite, geom=BallGeom())

        self.rear_thruster: Thruster = None
        self.front_thruster: Thruster = None
        self.left_thruster: Thruster = None
        self.right_thruster: Thruster = None

    def add_shape(self, shape: b2.Shape):
        #shape.collision_type = CollisionType.SHIP
        shape.user_material = CollisionType.SHIP
        shape.enable_contact_events(True)
        super().add_shape(shape)

    def _create(self):
        super()._create()
        force = 1000000
        self.front_thruster = Thruster(self.body, glm.vec2(0, self.size.y / 2), glm.vec2(0, -force))
        self.add_child(self.front_thruster)

        self.rear_thruster = Thruster(self.body, glm.vec2(0, -self.size.y / 2), glm.vec2(0, force))
        self.add_child(self.rear_thruster)

        self.left_thruster = Thruster(self.body, glm.vec2(-self.size.x / 2, 0), glm.vec2(-force, 0), 5)
        self.add_child(self.left_thruster)
        self.right_thruster = Thruster(self.body, glm.vec2(self.size.x / 2, 0), glm.vec2(force, 0), -5)
        self.add_child(self.right_thruster)

    def update(self, delta_time: float):
        super().update(delta_time)
        if not self.left_thruster.active and not self.right_thruster.active:
            self.body.angular_velocity = 0

    def fire(self):
        spawn_distance = 100  # Adjust based on your game's scale
        missile_speed = 100000  # Adjust missile speed as needed

        # Calculate the missile's spawn position
        direction = self.forward
        position = self.position + direction * spawn_distance

        laser = Laser(position, self.angle, missile_speed)
        self.layer.attach(laser)
