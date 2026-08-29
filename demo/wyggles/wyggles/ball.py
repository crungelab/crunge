import glm

from crunge.engine.d2.sprite import SpriteVu
from crunge.engine.loader.sprite.sprite_loader import SpriteLoader
from crunge.engine.d2.physics.geom import BallGeom
from crunge.engine.d2.physics import PhysicsChip

from .sprite_node import SpriteNode
from . import engine
from .beacon import *
from .dna import Dna


class Ball(SpriteNode):
    KICK_STRENGTH = 12.0  # retuned for unit space; was 200 in pixels

    def __init__(self) -> None:
        super().__init__()
        self.type = 'ball'
        self.name = Dna.gen_id(self.type)
        self.physics = None

    def _seat(self) -> None:
        super()._seat()
        self.model = SpriteLoader().load('${images}/ball.png')
        self.add(SpriteVu())
        self.physics = self.add(
            PhysicsChip(BallGeom(restitution=0.5, friction=0.9))
        )

    def _create(self) -> None:
        super()._create()
        self.beacon = Beacon(self, self.type)
        engine.sprite_engine.add_beacon(self.beacon)

    def _destroy(self) -> None:
        engine.sprite_engine.remove_beacon(self.beacon)
        super()._destroy()

    def receive_kick(self, position: glm.vec2, strength: float = None) -> None:
        offset = glm.vec2(self.position) - glm.vec2(position)
        length = glm.length(offset)
        if length < 1e-6:
            return
        strength = self.KICK_STRENGTH if strength is None else strength
        self.physics.apply_impulse((offset / length) * strength)