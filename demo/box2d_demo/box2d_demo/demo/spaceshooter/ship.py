import math

from loguru import logger

import glm
from crunge import box2d as b2
from crunge.engine.d2.physics import DynamicPhysics

from crunge.engine.d2.sprite import SpriteVu
from crunge.engine.loader.sprite.xml_sprite_atlas_loader import XmlSpriteAtlasLoader

from crunge.engine.d2 import Node2D
from crunge.engine.d2.physics.geom import BallGeom

from .physics_material import SHIP
from .thruster import Thruster
from .laser import Laser


class Ship(Node2D):
    default_vu = SpriteVu
    default_geom = BallGeom
    default_physics = DynamicPhysics
    default_material = SHIP

    def __init__(self, position: glm.vec2) -> None:
        atlas = XmlSpriteAtlasLoader().load("${resources}/spaceshooter/sheet.xml")
        logger.debug(f"atlas: {atlas}")
        
        sprite = atlas.get("playerShip1_orange.png")

        super().__init__(position, model=sprite)

        self.rear_thruster: Thruster = None
        self.front_thruster: Thruster = None
        self.left_thruster: Thruster = None
        self.right_thruster: Thruster = None

    def _create(self):
        super()._create()
        self.physics = self.get(DynamicPhysics)
        body = self.physics.body
        force = 1
        self.front_thruster = Thruster(body, glm.vec2(0, self.size.y / 2), glm.vec2(0, -force))
        self.add_child(self.front_thruster)

        self.rear_thruster = Thruster(body, glm.vec2(0, -self.size.y / 2), glm.vec2(0, force))
        self.add_child(self.rear_thruster)

        self.left_thruster = Thruster(body, glm.vec2(-self.size.x / 2, 0), glm.vec2(-force, 0), 5)
        self.add_child(self.left_thruster)
        self.right_thruster = Thruster(body, glm.vec2(self.size.x / 2, 0), glm.vec2(force, 0), -5)
        self.add_child(self.right_thruster)

    def update(self, delta_time: float):
        super().update(delta_time)
        if not self.left_thruster.active and not self.right_thruster.active:
            self.physics.body.angular_velocity = 0

    def fire(self):
        if self.is_destroyed:
            return

        spawn_distance = 1  # Adjust based on your game's scale
        missile_speed = 10  # Adjust missile speed as needed

        # Calculate the missile's spawn position
        direction = self.forward
        position = self.position + direction * spawn_distance

        laser = Laser(position, self.rotation, missile_speed)
        self.layer.attach(laser)
