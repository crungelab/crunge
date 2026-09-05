from typing import TYPE_CHECKING

import math
import random

from loguru import logger
import glm

from wyggles.game_entity import GameEntity

from .. import world
from wyggles.game_agent import GameAgent

if TYPE_CHECKING:
    from wyggles.wyggle import Wyggle


class WyggleAgent(GameAgent):
    node: "Wyggle"

    MAX_SPEED = 0.01            # meters per tick
    LOOK_AHEAD = 1.0            # meters
    AVOID_AUTHORITY = 4.0       # steering weight vs seek at point blank
    WIGGLE_STRENGTH = 0.2       # perpendicular amplitude, relative to unit heading
    WIGGLE_SPEED = 0.25

    WANDER_SAMPLES = 6
    WANDER_SPREAD = 90.0        # degrees either side of current heading
    WANDER_MIN_CLEARANCE = 0.3  # below this, treat every sample as boxed in
    PROBE_ANGLE = 45.0          # degrees either side, for avoidance probes
    GOAL_BACKOFF = 0.1          # keep the goal this far off a contact point

    def __init__(self, node: "Wyggle"):
        super().__init__(node)
        self.focus: GameEntity = None
        self.state: str = "wanderer"
        self.wiggle_phase = 0.0
        self.turn_bias = random.choice((1.0, -1.0))

    def reset(self):
        self.state = ""
        self.focus = None

    def scan(self, sensor_range: float = None) -> list[GameEntity]:
        if sensor_range is None:
            sensor_range = self.sensor_range
        return world.world_instance.query(
            self.node.position.x, self.node.position.y, sensor_range
        )

    # --- steering ---------------------------------------------------------

    def avoidance(self, direction: glm.vec2, distance: float) -> glm.vec2:
        """Steering vector away from obstacles ahead. Zero if the path is clear.
        Magnitude runs 0..AVOID_AUTHORITY, rising sharply as obstacles close in."""
        radius = self.node.radius
        origin = self.position

        ahead = self.cast_mover(origin, direction * distance, radius)
        if ahead >= 1.0:
            return glm.vec2(0, 0)

        perp = glm.vec2(-direction.y, direction.x)
        rad = glm.radians(self.PROBE_ANGLE)
        c, s = math.cos(rad), math.sin(rad)

        left = self.cast_mover(origin, (direction * c + perp * s) * distance, radius)
        right = self.cast_mover(origin, (direction * c - perp * s) * distance, radius)

        if abs(left - right) < 1e-3:
            turn = perp * self.turn_bias
        else:
            turn = perp if left > right else -perp

        urgency = (1.0 - ahead) ** 2 * self.AVOID_AUTHORITY
        return turn * urgency

    def move(self):
        to_target = self.target_position - self.node.position
        distance = glm.length(to_target)

        if distance > 1e-3:
            heading_dir = to_target / distance
        else:
            heading_dir = self.heading_vector

        steering = heading_dir + self.avoidance(heading_dir, self.LOOK_AHEAD)

        if glm.length(steering) > 1e-3:
            steering_dir = glm.normalize(steering)
        else:
            steering_dir = heading_dir

        # Steering direction is what the agent *intends*; velocity carries the
        # wiggle. Keeping them separate stops the wiggle from feeding back into
        # next tick's avoidance probes.
        self.velocity = steering_dir * self.MAX_SPEED

        self.wiggle_phase += self.WIGGLE_SPEED
        clearance = self.cast_mover(
            self.position, steering_dir * self.LOOK_AHEAD, self.node.radius
        )
        perp = glm.vec2(-steering_dir.y, steering_dir.x)
        wiggle = perp * math.sin(self.wiggle_phase) * self.WIGGLE_STRENGTH * clearance

        step = glm.normalize(steering_dir + wiggle) * self.MAX_SPEED
        self.node.move(self.node.position + step)

    # --- wander -----------------------------------------------------------

    def sample_wander(self) -> tuple[float, float]:
        """Probe WANDER_SAMPLES headings around the current one.
        Returns (heading degrees, clearance fraction) for the most open."""
        stride = self.sensor_range
        radius = self.node.radius
        current_heading = self.heading
        origin = self.position

        best_angle = current_heading
        best_fraction = 0.0

        for _ in range(self.WANDER_SAMPLES):
            angle = current_heading + random.uniform(
                -self.WANDER_SPREAD, self.WANDER_SPREAD
            )
            rad = glm.radians(angle)
            direction = glm.vec2(math.cos(rad), math.sin(rad))
            fraction = self.cast_mover(origin, direction * stride, radius)

            if fraction > best_fraction:
                best_fraction, best_angle = fraction, angle

        if best_fraction <= self.WANDER_MIN_CLEARANCE:
            logger.debug(f"Wander boxed in (best={best_fraction:.2f}); reversing")
            return current_heading + 180.0, best_fraction

        return best_angle, best_fraction

    def get_clear_wander_direction(self) -> float:
        return self.sample_wander()[0]

    def wander_goal(self) -> glm.vec2:
        """A reachable point to wander toward -- clamped short of whatever
        the chosen heading runs into, so seek can actually arrive."""
        heading, fraction = self.sample_wander()
        reach = max(0.0, fraction - self.GOAL_BACKOFF)
        return self.project(heading, self.sensor_range * reach)