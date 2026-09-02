from crunge.engine import Scheduler

from crunge.engine.d2.scene.layer.graph_layer_2d import GraphLayer2D

from .. import world
from ..ball import Ball

BALL_COUNT = 10

class BallLayer(GraphLayer2D):
    def __init__(self, name: str = "ball") -> None:
        super().__init__(name)
        self.balls: list[Ball] = []

    def create_children(self):
        super().create_children()
        for _ in range(BALL_COUNT):
            self.spawn_ball()

    def spawn_ball(self):
        ball = Ball()
        world.world_instance.materialize_random_from_center(ball, self)

    def add_ball(self, ball: Ball) -> None:
        self.balls.append(ball)
        self.add_node(ball.node)

    def remove_ball(self, ball: Ball) -> None:
        if ball in self.balls:
            self.balls.remove(ball)
            self.remove_node(ball.node)
