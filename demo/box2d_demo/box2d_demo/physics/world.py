from typing import TYPE_CHECKING, Generator
from typing import Optional

import contextlib
from contextvars import ContextVar

from loguru import logger


from crunge import box2d

#from . import globe

from .constants import GRAVITY

physics_world: ContextVar[Optional["PhysicsWorld2D"]] = ContextVar("physics_world", default=None)

class PhysicsWorld2D(box2d.World):
    def __init__(self, gravity=GRAVITY, iterations=35):
        world_def = box2d.WorldDef(gravity = box2d.Vec2(gravity[0], gravity[1]))
        super().__init__(world_def)
        logger.debug("PhysicsWorld2D.__init__")
        #globe.physics_engine = self
        self.gravity = gravity

    def make_current(self):
        logger.debug(f"PhysicsWorld2D.make_current: {self}")
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

    def update(self, delta_time=1 / 60.0):
        # logger.debug('PhysicsEngine.update')
        self.step(delta_time, 4)
