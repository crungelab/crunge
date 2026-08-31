import math

import glm

from crunge.engine.d2 import Node2D

from crunge.engine.ai.bt.run.agent import Agent


class Brain(Agent):
    def __init__(self, node: Node2D):
        super().__init__()
        self.node = node
        self.velocity = glm.vec2(0, 0)
        self.target_position = glm.vec2(0, 0)
        #self.sensor_range = 10
        self.sensor_range = 3

    @property
    def position(self) -> glm.vec2:
        return self.node.position

    @position.setter
    def position(self, val: glm.vec2):
        self.node.position = val

    @property
    def x(self) -> float:
        return self.node.position.x

    @property
    def y(self) -> float:
        return self.node.position.y

    @property
    def heading(self) -> float:
        angle_rad = math.atan2(self.velocity.y, self.velocity.x)
        angle_deg = math.degrees(angle_rad)
        return angle_deg

    def at_goal(self) -> bool:
        agent_radius = 1
        target_radius = 1
        distance = glm.distance(self.position, self.target_position)
        return distance <= (agent_radius + target_radius)

    def move_to(self, target_position: glm.vec2) -> None:
        self.target_position = target_position

    def seek(self) -> glm.vec2:
        return glm.normalize(self.position - self.target_position)

    def project(self, heading: float, distance: float) -> glm.vec2:
        px = self.x + (distance * (glm.cos(glm.radians(heading))))
        py = self.y + (distance * (glm.sin(glm.radians(heading))))
        return glm.vec2(px, py)

    def update(self, delta_time: float) -> None:
        pass
