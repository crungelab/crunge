from crunge.engine import Scheduler

from crunge.engine.d2.scene.layer.graph_layer_2d import GraphLayer2D

from .. import engine
from ..ball import Ball

BALL_COUNT = 10

class BallLayer(GraphLayer2D):
    def __init__(self, name: str = "ball") -> None:
        super().__init__(name)
        self.balls: list[Ball] = []
        self.respawning_balls = False

    def create_children(self):
        super().create_children()
        for _ in range(BALL_COUNT):
            self.spawn_ball()

    def spawn_ball(self):
        ball = Ball()
        engine.sprite_engine.materialize_random_from_center(ball, self)

    def add_ball(self, ball: Ball) -> None:
        self.balls.append(ball)
        self.add_node(ball.node)

    def remove_ball(self, ball: Ball) -> None:
        if ball in self.balls:
            self.balls.remove(ball)
            self.remove_node(ball.node)

    def update(self, delta_time: float):
        if len(self.balls) < BALL_COUNT and not self.respawning_balls:
            self.respawning_balls = True

            def re_spawn(delta_time: float):
                self.spawn_ball()
                self.respawning_balls = False

            Scheduler().schedule_once(re_spawn, 3.0)

        super().update(delta_time)
