from typing import TYPE_CHECKING, Protocol

from loguru import logger

import glm

from crunge.abt.run import *
from crunge.abt.run.act import *

# from crunge.abt.run.act import Action, Neuron, Message, action, neuron

from crunge.abt.run.task import Status

from ..agent import WyggleAgent
from ...fruit import Fruit
from ...ball import Ball

if TYPE_CHECKING:
    from crunge.engine.d2.node_2d import Node2D
    from ...wyggle.wyggle import Wyggle  # ASSUMPTION: module path


# ---------------------------------------------------------------------------
# Host vocabulary
# ---------------------------------------------------------------------------


class Beacon(Protocol):
    """What a spatial query hands back."""

    node: "Node2D"


# ---------------------------------------------------------------------------
# Shared slots
# ---------------------------------------------------------------------------


class Focus[T: Node2D]:
    """A one-slot blackboard shared between a scoring neuron and the actions
    that consume its pick.

    Passing this explicitly at tree-construction time -- rather than handing
    actions a reference to the neuron -- keeps the data dependency visible in
    the tree and stops actions reaching into a sibling task's internals.
    """

    __slots__ = ("target",)

    def __init__(self) -> None:
        self.target: T | None = None

    def clear(self) -> None:
        self.target = None

    def __repr__(self) -> str:
        return f"Focus({self.target!r})"


# ---------------------------------------------------------------------------
# Sensing
# ---------------------------------------------------------------------------


class SeesKind[T: Node2D](Neuron):
    """Scores 1 when something of `kind` is in sensor range, and parks it in
    `focus` for the actions downstream.

    Replaces the SeesFood / SeesBall pair, which differed only in isinstance
    target.
    """

    agent: WyggleAgent

    def __init__(self, kind: type[T], focus: Focus[T]) -> None:
        super().__init__()
        self.kind = kind
        self.focus = focus

    def main(self) -> float:
        self.focus.clear()
        for entity in self.agent.scan(self.agent.sensor_range):
            if isinstance(entity, self.kind):
                self.focus.target = entity
                return 1.0
        return 0.0


# ---------------------------------------------------------------------------
# Actions
# ---------------------------------------------------------------------------


class FocusedAction[T: Node2D](Action):
    """Base for actions driven by a Focus slot.

    Claims the slot on entry, fails cleanly if the reading went stale between
    scoring and running, and resets the agent on any exit that is not SUCCESS
    -- including cancellation, which raises GeneratorExit at the await and so
    never reaches code placed after the loop.
    """

    agent: WyggleAgent
    state_name: str = ""

    def __init__(self, focus: Focus[T]) -> None:
        super().__init__()
        self.focus = focus

    def claim(self) -> T | None:
        target = self.focus.target
        if target is None:
            return None
        self.agent.focus = target
        self.agent.state = self.state_name
        return target


class MoveTo(FocusedAction["Node2D"]):
    state_name = "seek"

    async def main(self, msg: Message) -> Status:
        target = self.claim()
        if target is None:
            return self.fail()

        agent = self.agent
        try:
            while self.ok():
                if agent.entity.intersects(target):
                    agent.state = ""
                    return self.succeed()
                agent.move_to(target.position)
                agent.move()
                await self.sleep()
            return self.fail()
        finally:
            if self.status is not Status.SUCCESS:
                agent.reset()


class Eat(FocusedAction[Fruit]):
    state_name = "eat"

    #: ticks between mouth toggles
    munch_interval = 10

    async def main(self, msg: Message) -> Status:
        target = self.claim()
        if target is None:
            return self.fail()

        agent = self.agent
        entity = agent.entity
        munch_timer = 0

        try:
            while self.ok():
                if target.is_munched:
                    entity.close_mouth()
                    entity.energy = entity.energy + target.energy
                    agent.reset()
                    return self.succeed()

                if munch_timer > 0:
                    munch_timer -= 1
                else:
                    munch_timer = self.munch_interval
                    if entity.face != "munchy":
                        entity.open_mouth()
                    else:
                        entity.close_mouth()
                        target.receive_munch()

                await self.sleep()
            return self.fail()
        finally:
            if self.status is not Status.SUCCESS:
                agent.reset()


class Kick(FocusedAction[Ball]):
    state_name = "kick"

    kick_force = 0.2

    async def main(self, msg: Message) -> Status:
        target = self.claim()
        if target is None:
            return self.fail()

        target.receive_kick(self.agent.entity.position, self.kick_force)
        self.agent.reset()
        return self.succeed()


class Wander(Action):
    """Fallback steering. Runs its own per-tick movement rather than handing
    off to a `state_wander` method on the brain."""

    agent: WyggleAgent

    async def main(self, msg: Message) -> Status:
        agent = self.agent
        agent.state = "wander"
        try:
            while self.ok():
                if agent.at_goal():
                    heading = agent.get_clear_wander_direction()
                    agent.move_to(agent.project(heading, agent.sensor_range))
                agent.move()
                await self.sleep()
            return self.fail()
        finally:
            if self.status is not Status.SUCCESS:
                agent.reset()


# ---------------------------------------------------------------------------
# Brain
# ---------------------------------------------------------------------------


class ReactiveWyggleAgent(WyggleAgent):
    def __init__(self, model) -> None:
        super().__init__(model)

        fruit: Focus[Fruit] = Focus()
        ball: Focus[Ball] = Focus()

        with root(self):
            with forever():
                with utility():
                    with neuron(SeesKind(Fruit, fruit)):
                        with sequence():
                            with action(MoveTo(fruit)):
                                pass
                            with action(Eat(fruit)):
                                pass

                    with neuron(SeesKind(Ball, ball)):
                        with sequence():
                            with action(MoveTo(ball)):
                                pass
                            with action(Kick(ball)):
                                pass

                    with action(Wander()):
                        pass
