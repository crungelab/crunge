import glm

from .sprite_node import SpriteNode
from . import engine
from .beacon import *
from .dna import Dna

class Ball(SpriteNode):
    def __init__(self):
        super().__init__()
        self.type = 'ball'
        self.name = Dna.gen_id(self.type)
    
    def _create(self):
        super()._create()
        #
        self.beacon = Beacon(self, self.type)
        engine.sprite_engine.add_beacon(self.beacon)
        #
        mass = 1
        radius = 16
        """
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        body.node = self
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = .5
        shape.friction = .9
        engine.sprite_engine.space.add(body, shape)
        self.body = body
        """

        self.load_sprite('${images}/ball.png')
        #super()._create()
        #self.update_matrix()


    def receive_kick(self, position, strength = 200):
        impulse = glm.vec2(self.position.x - position.x, self.position.y - position.y)
        impulse = glm.normalize(impulse) * strength
        self.body.apply_impulse_at_local_point((impulse.x, impulse.y), (0, 0))        
