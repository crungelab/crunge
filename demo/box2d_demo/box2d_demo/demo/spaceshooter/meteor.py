from typing import Type
import random

from loguru import logger

import glm

from crunge import box2d

from crunge.engine.loader.sprite.xml_sprite_atlas_loader import XmlSpriteAtlasLoader

from crunge.engine.d2.entity import DynamicEntity2D
from crunge.engine.d2.physics.geom import BallGeom
from crunge.engine.d2.physics import DynamicPhysics

from .physics_material import METEOR

class Meteor(DynamicEntity2D):
    geom = BallGeom()
    material = METEOR

    linear_velocity_range=((-1, 1), (-1, 1))
    angular_velocity_range=(-2, 2)

    def __init__(self, position: glm.vec2, name: str) -> None:
        atlas = XmlSpriteAtlasLoader().load("${resources}/spaceshooter/sheet.xml")
        #logger.debug(f"atlas: {atlas}")
        
        sprite = atlas.get(name)
        super().__init__(position, model=sprite)

    @classmethod
    def produce(cls, position: glm.vec2):
        meteor = cls(position).create()
        return meteor

    def _create(self):
        super()._create()
        body = self.physics.body
        linear_velocity = box2d.Vec2(random.uniform(*self.linear_velocity_range[0]), 
                           random.uniform(*self.linear_velocity_range[1]))
        body.linear_velocity = linear_velocity

        angular_velocity = random.uniform(*self.angular_velocity_range)
        body.angular_velocity = angular_velocity
        #self.body.mass = 1

    def create_fragment(self, cls: Type["Meteor"], position: glm.vec2, velocity: box2d.Vec2):
        fragment = cls(position).create()
        fragment.body.linear_velocity = velocity
        fragment.body.angular_velocity = random.uniform(*Meteor.angular_velocity_range)
        self.parent.add_child(fragment)

class MeteorGreyBig1(Meteor):
    def __init__(self, position: glm.vec2) -> None:
        super().__init__(position, "meteorGrey_big1.png")
    def _destroy(self):
        self.create_fragment(MeteorGreyMed1, self.position, self.body.linear_velocity)
        self.create_fragment(MeteorGreyMed2, self.position, self.body.linear_velocity)
        super()._destroy()

class MeteorGreyBig2(Meteor):
    def __init__(self, position: glm.vec2) -> None:
        super().__init__(position, "meteorGrey_big2.png")
    def _destroy(self):
        self.create_fragment(MeteorGreyMed1, self.position, self.body.linear_velocity)
        self.create_fragment(MeteorGreyMed2, self.position, self.body.linear_velocity)
        super()._destroy()

class MeteorGreyBig3(Meteor):
    def __init__(self, position: glm.vec2) -> None:
        super().__init__(position, "meteorGrey_big3.png")
    def _destroy(self):
        self.create_fragment(MeteorGreyMed1, self.position, self.body.linear_velocity)
        self.create_fragment(MeteorGreyMed2, self.position, self.body.linear_velocity)
        super()._destroy()

class MeteorGreyBig4(Meteor):
    def __init__(self, position: glm.vec2) -> None:
        super().__init__(position, "meteorGrey_big4.png")
    def _destroy(self):
        self.create_fragment(MeteorGreyMed1, self.position, self.body.linear_velocity)
        self.create_fragment(MeteorGreyMed2, self.position, self.body.linear_velocity)
        super()._destroy()

class MeteorGreyMed1(Meteor):
    def __init__(self, position: glm.vec2) -> None:
        super().__init__(position, "meteorGrey_med1.png")
    def _destroy(self):
        self.create_fragment(MeteorGreySmall1, self.position, self.body.linear_velocity)
        self.create_fragment(MeteorGreySmall2, self.position, self.body.linear_velocity)
        super()._destroy()

class MeteorGreyMed2(Meteor):
    def __init__(self, position: glm.vec2) -> None:
        super().__init__(position, "meteorGrey_med2.png")
    def _destroy(self):
        self.create_fragment(MeteorGreySmall1, self.position, self.body.linear_velocity)
        self.create_fragment(MeteorGreySmall2, self.position, self.body.linear_velocity)
        super()._destroy()

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
