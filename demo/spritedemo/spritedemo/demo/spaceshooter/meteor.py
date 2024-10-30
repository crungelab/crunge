import random

from loguru import logger

import glm

from crunge.engine.d2.sprite import Sprite, SpriteMaterial
from crunge.engine.loader.texture_atlas_loader import TextureAtlasLoader

from ...model_2d import DynamicModel2D
from ...geom import BallGeom
from .collision_type import CollisionType

class Meteor(DynamicModel2D):
    linear_velocity_range=((-100, 100), (-100, 100))
    angular_velocity_range=(-2, 2)

    def __init__(self, position: glm.vec2, name: str) -> None:
        super().__init__(position, geom=BallGeom)
        atlas = TextureAtlasLoader().load(":resources:/spaceshooter/sheet.xml")
        #logger.debug(f"atlas: {atlas}")
        
        texture = atlas.get(name)
        material = SpriteMaterial(texture)
        self.vu = Sprite(material).create()
        self.size = texture.size

    @classmethod
    def produce(cls, position: glm.vec2):
        meteor = cls(position).create()
        return meteor

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

    def create_fragment(self, cls, position, velocity):
        fragment = cls(position).create()
        fragment.body.velocity = velocity
        fragment.body.angular_velocity = random.uniform(*Meteor.angular_velocity_range)
        self.parent.attach(fragment)

class MeteorGreyBig1(Meteor):
    def __init__(self, position: glm.vec2) -> None:
        super().__init__(position, "meteorGrey_big1.png")
    def destroy(self):
        self.create_fragment(MeteorGreyMed1, self.position, self.body.velocity)
        self.create_fragment(MeteorGreyMed2, self.position, self.body.velocity)
        super().destroy()

class MeteorGreyBig2(Meteor):
    def __init__(self, position: glm.vec2) -> None:
        super().__init__(position, "meteorGrey_big2.png")
    def destroy(self):
        self.create_fragment(MeteorGreyMed1, self.position, self.body.velocity)
        self.create_fragment(MeteorGreyMed2, self.position, self.body.velocity)
        super().destroy()

class MeteorGreyBig3(Meteor):
    def __init__(self, position: glm.vec2) -> None:
        super().__init__(position, "meteorGrey_big3.png")
    def destroy(self):
        self.create_fragment(MeteorGreyMed1, self.position, self.body.velocity)
        self.create_fragment(MeteorGreyMed2, self.position, self.body.velocity)
        super().destroy()

class MeteorGreyBig4(Meteor):
    def __init__(self, position: glm.vec2) -> None:
        super().__init__(position, "meteorGrey_big4.png")
    def destroy(self):
        self.create_fragment(MeteorGreyMed1, self.position, self.body.velocity)
        self.create_fragment(MeteorGreyMed2, self.position, self.body.velocity)
        super().destroy()

class MeteorGreyMed1(Meteor):
    def __init__(self, position: glm.vec2) -> None:
        super().__init__(position, "meteorGrey_med1.png")
    def destroy(self):
        self.create_fragment(MeteorGreySmall1, self.position, self.body.velocity)
        self.create_fragment(MeteorGreySmall2, self.position, self.body.velocity)
        super().destroy()

class MeteorGreyMed2(Meteor):
    def __init__(self, position: glm.vec2) -> None:
        super().__init__(position, "meteorGrey_med2.png")
    def destroy(self):
        self.create_fragment(MeteorGreySmall1, self.position, self.body.velocity)
        self.create_fragment(MeteorGreySmall2, self.position, self.body.velocity)
        super().destroy()

class MeteorGreySmall1(Meteor):
    def __init__(self, position: glm.vec2) -> None:
        super().__init__(position, "meteorGrey_small1.png")

class MeteorGreySmall2(Meteor):
    def __init__(self, position: glm.vec2) -> None:
        super().__init__(position, "meteorGrey_small2.png")

class MeteorGreyTiny1(Meteor):
    def __init__(self, position: glm.vec2) -> None:
        super().__init__(position, "meteorGrey_tiny1.png")

class MeteorGreyTiny2(Meteor):
    def __init__(self, position: glm.vec2) -> None:
        super().__init__(position, "meteorGrey_tiny2.png")
