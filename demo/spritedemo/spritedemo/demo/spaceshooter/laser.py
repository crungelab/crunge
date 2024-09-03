import math

from loguru import logger
import glm

from crunge.engine.d2.sprite import Sprite
from crunge.engine.loader.texture_atlas_loader import TextureAtlasLoader

from ...model_2d import DynamicModel2D
from ...geom import BoxGeom
from .collision_type import CollisionType

class Laser(DynamicModel2D):
    def __init__(self, position: glm.vec2, angle: float, speed: glm.vec2) -> None:
        super().__init__(position, geom=BoxGeom)
        self.angle = angle
        self.speed = speed
        atlas = TextureAtlasLoader().load("{resources}/spaceshooter/sheet.xml")
        logger.debug(f"atlas: {atlas}")
        
        texture = atlas.get("laserBlue01.png")

        self.vu = Sprite(texture)
        self.size = texture.size
        self.ttl = 0.5

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
