import math

from loguru import logger
import glm

from crunge import box2d as b2

from crunge.engine.d2.sprite import Sprite, SpriteVu
from crunge.engine.loader.sprite.xml_sprite_atlas_loader import XmlSpriteAtlasLoader

from crunge.engine.d2.entity import DynamicEntity2D
from crunge.engine.d2.physics.geom import BoxGeom

from .collision_type import CollisionType

class Laser(DynamicEntity2D):
    def __init__(self, position: glm.vec2, angle: float, speed: float) -> None:
        super().__init__(position, geom=BoxGeom())
        self.angle = angle
        self.speed = speed

        atlas = XmlSpriteAtlasLoader().load(":resources:/spaceshooter/sheet.xml")
        logger.debug(f"atlas: {atlas}")
        
        sprite = atlas.get("laserBlue01.png")

        self.vu = SpriteVu(sprite)

        self.ttl = 1.0

    def add_shape(self, shape):
        shape.user_material = CollisionType.LASER
        shape.enable_contact_events(True)
        super().add_shape(shape)

    def update(self, dt):
        super().update(dt)
        self.ttl = self.ttl - dt
        if self.ttl <= 0:
            self.destroy()
            return
        direction = self.forward
        velocity = direction * self.speed
        self.body.linear_velocity = b2.Vec2(*velocity)
