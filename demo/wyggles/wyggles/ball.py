import glm

from crunge.engine.d2.sprite import SpriteVu
from crunge.engine.loader.sprite.sprite_loader import SpriteLoader
from crunge.engine.d2.physics.geom import BallGeom
from crunge.engine.d2.physics import DynamicPhysics
from crunge.engine.d2.entity import PhysicsEntity2D

from .game_entity import GameEntity
from . import world
from .dna import Dna


class Ball(GameEntity):
    KICK_STRENGTH = 12.0  # retuned for unit space; was 200 in pixels

    def __init__(self) -> None:
        super().__init__()
        self.type = 'ball'
        self.name = Dna.gen_id(self.type)
        self.physics = None

    def _seat(self) -> None:
        super()._seat()
        self.model = SpriteLoader().load('${images}/ball.png')
        self.physics = self.add(
            DynamicPhysics(BallGeom())
        )

    def _create(self) -> None:
        super()._create()
        world.world_instance.add_entity(self)

    def _destroy(self) -> None:
        world.world_instance.remove_entity(self)
        super()._destroy()

    def receive_kick(self, position: glm.vec2, strength: float = None) -> None:
        offset = glm.vec2(self.position) - glm.vec2(position)
        length = glm.length(offset)
        if length < 1e-6:
            return
        strength = self.KICK_STRENGTH if strength is None else strength
        self.physics.apply_impulse((offset / length) * strength)