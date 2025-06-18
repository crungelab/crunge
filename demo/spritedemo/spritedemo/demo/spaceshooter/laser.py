import math

from loguru import logger
import glm

from crunge.engine.d2.sprite import Sprite, SpriteVu
from crunge.engine.loader.sprite.xml_sprite_atlas_loader import XmlSpriteAtlasLoader

from crunge.engine.d2.entity import DynamicEntity2D
from crunge.engine.d2.physics.geom import BoxGeom

from .collision_type import CollisionType

class Laser(DynamicEntity2D):
    def __init__(self, position: glm.vec2, angle: float, speed: glm.vec2) -> None:
        super().__init__(position, geom=BoxGeom())
        self.angle = angle
        self.speed = speed
        atlas = XmlSpriteAtlasLoader().load(":resources:/spaceshooter/sheet.xml")
        logger.debug(f"atlas: {atlas}")
        
        sprite = atlas.get("laserBlue01.png")

        self.vu = SpriteVu(sprite)
        self.ttl = 1.0

    def add_shape(self, shape):
        shape.collision_type = CollisionType.LASER
        super().add_shape(shape)

    def update(self, dt):
        super().update(dt)
        self.ttl = self.ttl - dt
        if self.ttl <= 0:
            self.destroy()
        #self.body.apply_force_at_local_point(tuple(self.force), tuple(self.position))
        rotation = self._rotation + math.pi / 2
        direction = glm.vec2(math.cos(rotation), math.sin(rotation))
        self.body.velocity = tuple(direction * self.speed)
