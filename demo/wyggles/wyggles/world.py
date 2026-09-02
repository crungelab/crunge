import random
import copy

import glm

from crunge.engine.d2.physics import PhysicsWorld2D
from crunge.engine.d2.scene.layer import GraphLayer2D

from .game_entity import GameEntity
from .beacon import Beacon

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
        
        self.beacons: list[Beacon] = []

    def add_beacon(self, beacon):
        self.beacons.append(beacon)

    def remove_beacon(self, beacon):
        if beacon in self.beacons:
            self.beacons.remove(beacon)

    def query(self, x, y, distance) -> list[Beacon]:
        result = []
        for beacon in self.beacons:
            dist = glm.distance(glm.vec2(x, y), glm.vec2(beacon.x, beacon.y))
            if dist < distance:
                b = copy.copy(beacon)
                b.distance = dist
                result.append(b)
        result.sort(key=lambda x: x.distance)
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
