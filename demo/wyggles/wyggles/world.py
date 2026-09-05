import random
import copy

import glm

from crunge.engine.d2.physics import PhysicsWorld2D
from crunge.engine.d2.scene.layer import GraphLayer2D

from .game_entity import GameEntity

world_left = 0
world_bottom = 0
# world_right = 1024
#world_right = 800
world_right = 8
# world_top = 768
#world_top = 600
world_top = 6


class World(PhysicsWorld2D):
    def __init__(self):
        super().__init__(gravity=(0, 0))
        global world_instance
        world_instance = self
        
        self.entities: list[GameEntity] = []

    def add_entity(self, entity):
        self.entities.append(entity)

    def remove_entity(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)

    def proximity_query(self, origin: glm.vec2, distance: float) -> list[GameEntity]:
        result = []
        for entity in self.entities:
            dist = glm.distance(origin, entity.position)
            if dist < distance:
                result.append(entity)
        result.sort(key=lambda e: glm.distance(origin, e.position))
        return result

    def materialize_random_from_center(self, node: GameEntity, layer: GraphLayer2D):
        halfMaxX = world_right / 2
        halfMaxY = world_top / 2
        diameter = world_top
        radius = diameter / 2

        node.position = glm.vec2(
            (halfMaxX - radius) + (random.random() * diameter),
            (halfMaxY - radius) + (random.random() * diameter),
        )

        layer.attach(node)

world_instance: World = None
