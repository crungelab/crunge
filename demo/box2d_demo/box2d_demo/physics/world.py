from typing import TYPE_CHECKING, Generator
from typing import Optional

import contextlib
from contextvars import ContextVar

from loguru import logger


from crunge import box2d

from . import globe

from .constants import GRAVITY

#from .draw_options import DrawOptions

physics_world: ContextVar[Optional["PhysicsWorld2D"]] = ContextVar("physics_world", default=None)

class PhysicsWorld2D(box2d.World):
    def __init__(self, gravity=GRAVITY, iterations=35):
        world_def = box2d.WorldDef(gravity = box2d.Vec2(0.0, -10.0))
        super().__init__(world_def)
        logger.debug("PhysicsWorld2D.__init__")
        globe.physics_engine = self
        self.gravity = gravity
        #world_def = box2d.WorldDef(gravity = box2d.Vec2(0.0, -10.0))
        #self.world = box2d.World(world_def)
        #self.world.gravity = gravity
        #self.world.iterations = iterations

        # Enable sleeping
        #self.world.sleep_time_threshold = 0.5     # default is disabled
        #self.world.idle_speed_threshold = 0.1     # m/s-ish
        # Optional global damping helps bodies settle
        #self.world.damping = 0.99

    def make_current(self):
        physics_world.set(self)

    @classmethod
    def get_current(cls) -> Optional["PhysicsWorld2D"]:
        return physics_world.get()

    @contextlib.contextmanager
    def use(self):
        prev_engine = self.get_current()
        self.make_current()
        yield self
        if prev_engine is not None:
            prev_engine.make_current()

    @contextlib.contextmanager
    def update(self, delta_time=1 / 60.0):
        with self.use():
            self.world.step(delta_time)
            yield self
    """
    def update(self, delta_time=1 / 60.0):
        # logger.debug('PhysicsEngine.update')
        self.world.step(delta_time)
    """

    """
    def debug_draw(self, draw_options: DrawOptions):
        self.space.debug_draw(draw_options)
    """