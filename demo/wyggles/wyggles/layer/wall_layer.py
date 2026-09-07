from crunge.engine.d2.scene.layer.graph_layer_2d import GraphLayer2D

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
        bounds = self.bounds
        left, bottom = bounds.left, bounds.bottom
        right, top = bounds.right, bounds.top

        thickness = 1.0  # meters

        # North
        self.spawn_wall(left - thickness, top, right + thickness, top + thickness)
        # South
        self.spawn_wall(left - thickness, bottom - thickness, right + thickness, bottom)
        # East
        self.spawn_wall(right, bottom, right + thickness, top)
        # West
        self.spawn_wall(left - thickness, bottom, left, top)

    def add_wall(self, wall: Wall) -> None:
        self.walls.append(wall)
        self.add_node(wall.node)

    def remove_wall(self, wall: Wall) -> None:
        if wall in self.walls:
            self.walls.remove(wall)
            self.remove_node(wall.node)
