import math

from loguru import logger
import glm

from crunge import box2d as b2

from crunge.engine.d2.sprite import Sprite, SpriteVu
from crunge.engine.loader.sprite.xml_sprite_atlas_loader import XmlSpriteAtlasLoader

from crunge.engine.d2 import Node2D
from crunge.engine.d2.physics.geom import BoxGeom
from crunge.engine.d2.physics import DynamicPhysics

from .physics_material import LASER


class Laser(Node2D):
    default_vu = SpriteVu
    default_geom = BoxGeom
    default_physics = DynamicPhysics
    default_material = LASER

    def __init__(self, position: glm.vec2, rotation: float, speed: float) -> None:
        self.speed = speed

        atlas = XmlSpriteAtlasLoader().load("${resources}/spaceshooter/sheet.xml")
        logger.debug(f"atlas: {atlas}")

        sprite = atlas.get("laserBlue01.png")
        super().__init__(position, rotation=rotation, model=sprite)

        self.ttl = 1.0

    def _create(self):
        super()._create()
        self.physics = self.get(DynamicPhysics)
        self.body = self.physics.body
        direction = self.forward
        velocity = direction * self.speed
        self.body.linear_velocity = b2.Vec2(*velocity)


    def update(self, dt):
        super().update(dt)
        self.ttl = self.ttl - dt
        if self.ttl <= 0:
            self.destroy()
            return
        direction = self.forward
        velocity = direction * self.speed
        self.physics.body.linear_velocity = b2.Vec2(*velocity)
