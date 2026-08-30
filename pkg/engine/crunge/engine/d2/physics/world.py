from typing import Optional

import contextlib
from contextvars import ContextVar
from dataclasses import dataclass

from loguru import logger

from crunge import box2d

from crunge.engine.signal import Signal

from . import globe
from .constants import GRAVITY

physics_world: ContextVar[Optional["PhysicsWorld2D"]] = ContextVar(
    "physics_world", default=None
)

SUB_STEPS = 4


@dataclass
class Contact:
    """A begin/end touch between two shapes, for the frame it happened."""

    shape_a: box2d.Shape
    shape_b: box2d.Shape

    def other(self, shape: box2d.Shape) -> Optional[box2d.Shape]:
        if self.shape_a is shape:
            return self.shape_b
        if self.shape_b is shape:
            return self.shape_a
        return None


@dataclass
class SensorContact:
    """A sensor overlap. The sensor is the trigger; the visitor entered it."""

    sensor: box2d.Shape
    visitor: box2d.Shape


class PhysicsWorld2D(box2d.World):
    def __init__(self, gravity=GRAVITY, sub_steps: int = SUB_STEPS):
        world_def = box2d.WorldDef(gravity=box2d.Vec2(gravity[0], gravity[1]))
        super().__init__(world_def)
        logger.debug("PhysicsWorld2D.__init__")

        globe.world = self
        self.gravity = gravity
        self.sub_steps = sub_steps

        # Box2D v3 reports contacts as per-frame edge events. Polled once
        # here and pushed out, so consumers don't each walk the whole list.
        self.contact_began = Signal[Contact]()
        self.contact_ended = Signal[Contact]()
        self.sensor_began = Signal[SensorContact]()
        self.sensor_ended = Signal[SensorContact]()

    # -- current-world plumbing -------------------------------------------

    def make_current(self):
        logger.debug(f"PhysicsWorld2D.make_current: {self}")
        physics_world.set(self)

    @classmethod
    def get_current(cls) -> Optional["PhysicsWorld2D"]:
        return physics_world.get()

    @contextlib.contextmanager
    def use(self):
        token = physics_world.set(self)
        try:
            yield self
        finally:
            physics_world.reset(token)

    # -- stepping ----------------------------------------------------------

    def update(self, delta_time=1 / 60.0):
        self.step(delta_time, self.sub_steps)
        self.dispatch_contacts()

    def dispatch_contacts(self):
        events = self.get_contact_events()

        for evt in events.get_begin_events():
            a, b = evt.shape_id_a, evt.shape_id_b
            # A shape destroyed by an earlier handler in this same batch is
            # a dead handle; touching it trips the generation assertion.
            if a.is_valid() and b.is_valid():
                self.contact_began.emit(Contact(a, b))

        for evt in events.get_end_events():
            a, b = evt.shape_id_a, evt.shape_id_b
            if a.is_valid() and b.is_valid():
                self.contact_ended.emit(Contact(a, b))

    def dispatch_sensors(self):
        # ASSUMPTION: bindings emit get_sensor_events with
        # get_begin_events/get_end_events and sensor/visitor shape fields.
        # Not called from update() — wire it in once the names are confirmed.
        events = self.get_sensor_events()

        for evt in events.get_begin_events():
            sensor, visitor = evt.sensor_shape_id, evt.visitor_shape_id
            if sensor.is_valid() and visitor.is_valid():
                self.sensor_began.emit(SensorContact(sensor, visitor))

        for evt in events.get_end_events():
            sensor, visitor = evt.sensor_shape_id, evt.visitor_shape_id
            if sensor.is_valid() and visitor.is_valid():
                self.sensor_ended.emit(SensorContact(sensor, visitor))

    def draw(self, debug_draw):
        box2d.world_draw(self, debug_draw)