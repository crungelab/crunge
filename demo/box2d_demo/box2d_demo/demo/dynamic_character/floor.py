import glm

from box2d_demo.demo.dynamic_character.collision_type import CollisionType
from box2d_demo.entity import StaticEntity2D
from box2d_demo.physics.geom import BoxGeom

class Floor(StaticEntity2D):
    def __init__(self, position: glm.vec2, scale: glm.vec2) -> None:
        super().__init__(position, scale=scale, geom=BoxGeom())

    def add_shape(self, shape):
        shape.user_material = CollisionType.FLOOR
        shape.enable_contact_events(True)
        super().add_shape(shape)
