import random

from loguru import logger

import glm

from ...sprite import Sprite
from ...model_2d import DynamicModel2D
from ...texture_atlas_kit import TextureAtlasKit
from ...resource_kit import ResourceKit
from ...geom import BallGeom
from .collision_type import CollisionType

class Meteor(DynamicModel2D):
    linear_velocity_range=((-100, 100), (-100, 100))
    angular_velocity_range=(-2, 2)

    def __init__(self, position: glm.vec2) -> None:
        super().__init__(position, geom=BallGeom)
        path = ResourceKit().root / "spaceshooter" / "sheet.xml"
        atlas = TextureAtlasKit().load(path)
        logger.debug(f"atlas: {atlas}")
        
        texture = atlas.get("meteorGrey_big1.png")

        self.vu = Sprite(texture)
        self.size = texture.size

    def add_shape(self, shape):
        shape.collision_type = CollisionType.METEOR
        super().add_shape(shape)

    def _create(self):
        super()._create()
        linear_velocity = (random.uniform(*self.linear_velocity_range[0]), 
                           random.uniform(*self.linear_velocity_range[1]))
        self.body.velocity = linear_velocity

        angular_velocity = random.uniform(*self.angular_velocity_range)
        self.body.angular_velocity = angular_velocity
        #self.body.mass = 1
