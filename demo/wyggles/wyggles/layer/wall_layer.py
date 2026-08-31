from crunge.engine import Scheduler

from crunge.engine.d2.scene.layer.graph_layer_2d import GraphLayer2D

from .. import engine
from ..engine import world_left, world_right, world_top, world_bottom

from ..wall import Wall

BALL_COUNT = 10

class WallLayer(GraphLayer2D):
    def __init__(self, name: str = "wall") -> None:
        super().__init__(name)
        self.walls: list[Wall] = []

    # Walls
    def spawn_wall(self, left: float, bottom: float, right: float, top: float):
        node = Wall(left, bottom, right, top)
        self.attach(node)


    def create_children(self):
        super().create_children()
        left = world_left
        bottom = world_bottom
        right = world_right
        top = world_top
        thickness = 200
        # North Wall
        self.spawn_wall(left - thickness, top, right + thickness, top + thickness)
        # South Wall
        self.spawn_wall(left - thickness, bottom - thickness, right + thickness, bottom)
        # East Wall
        self.spawn_wall(right, bottom - thickness, right + thickness, top + thickness)
        # West Wall
        self.spawn_wall(left - thickness, bottom - thickness, left, top + thickness)

    def add_wall(self, wall: Wall) -> None:
        self.walls.append(wall)
        self.add_node(wall.node)

    def remove_wall(self, wall: Wall) -> None:
        if wall in self.walls:
            self.walls.remove(wall)
            self.remove_node(wall.node)
