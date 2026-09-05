import math

from loguru import logger
import glm

from crunge import box2d
from crunge.engine.d2.entity import Entity2D
from crunge.abt.run.agent import Agent

from . import world


class GameAgent(Agent):
    #: how close counts as arrived, in meters
    GOAL_TOLERANCE = 0.3

    def __init__(self, entity: Entity2D):
        super().__init__()
        self.entity = entity
        self.velocity = glm.vec2(0, 0)
        self.target_position = glm.vec2(0, 0)
        self.sensor_range = 3
        self.world = world.world_instance

    @property
    def position(self) -> glm.vec2:
        return self.entity.position

    @position.setter
    def position(self, val: glm.vec2):
        self.entity.position = val

    @property
    def heading(self) -> float:
        """Degrees, derived from current velocity. Zero when stationary."""
        return math.degrees(math.atan2(self.velocity.y, self.velocity.x))

    @property
    def heading_vector(self) -> glm.vec2:
        rad = glm.radians(self.heading)
        return glm.vec2(math.cos(rad), math.sin(rad))

    def at_goal(self) -> bool:
        return glm.distance(self.position, self.target_position) <= self.GOAL_TOLERANCE

    def move_to(self, target_position: glm.vec2) -> None:
        self.target_position = target_position

    def project(self, heading: float, distance: float) -> glm.vec2:
        """Point `distance` meters along `heading` degrees. Ignores geometry."""
        rad = glm.radians(heading)
        return self.position + glm.vec2(math.cos(rad), math.sin(rad)) * distance

    def update(self, delta_time: float) -> None:
        pass

    # --- physics queries --------------------------------------------------

    def cast_mover(
        self,
        origin: glm.vec2,
        translation: glm.vec2,
        radius: float,
        filter=None,
    ) -> float:
        """Sweep a circle of `radius` from `origin` along `translation` (meters).
        Returns the fraction of the translation travelled before contact;
        1.0 means nothing was hit.

        The capsule points are LOCAL to `origin` -- the world call takes the
        origin separately."""
        zero = box2d.Vec2(0.0, 0.0)
        mover = box2d.Capsule(center1=zero, center2=zero, radius=radius)
        return self.world.cast_mover(
            box2d.Vec2(origin.x, origin.y),
            mover,
            box2d.Vec2(translation.x, translation.y),
            filter if filter is not None else box2d.default_query_filter(),
        )

    def path_is_clear(
        self,
        origin: glm.vec2,
        translation: glm.vec2,
        radius: float,
        filter=None,
    ) -> bool:
        return self.cast_mover(origin, translation, radius, filter) >= 1.0