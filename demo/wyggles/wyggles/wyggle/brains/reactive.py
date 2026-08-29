import math
import random

from loguru import logger

from crunge.engine.ai.bt.run import *
from crunge.engine.ai.bt.run import _I
from crunge.engine.ai.bt.run.act import *
from crunge.engine.ai.bt.run.task import Status

from ... import engine
from ...wyggle.brain import WyggleBrain
from ...fruit import Fruit
from ...ball import Ball

_see = term_('see')
_x = var_("x")


class Sees(Action):
    def __init__(self):
        super().__init__()

    async def main(self, msg: Message):
        # was `while self.ok:` -- a bound method, always truthy
        while self.ok():
            beacons = engine.sprite_engine.query(
                self.bot.x, self.bot.y, self.bot.sensor_range
            )
            for beacon in beacons:
                self.post(Assert(Believe(_I, _see, beacon.node)))
            await self.sleep()


class SeesFood(Neuron):
    def __init__(self):
        super().__init__()
        self.focus = None
        self.rule = None

    def activate(self):
        t = Trigger(Assert, Believe, _I, _see, _x)

        async def action(task: Task, msg: Message):
            logger.debug("Match: {}", msg.data.obj)

        self.rule = self.bot.subscribe(t, action)

    def main(self):
        beacons = engine.sprite_engine.query(
            self.bot.x, self.bot.y, self.bot.sensor_range
        )
        self.focus = None
        for beacon in beacons:
            if isinstance(beacon.node, Fruit):
                self.focus = beacon.node
                return 1
        return 0


class MoveTo(Action):
    def __init__(self, sees):
        super().__init__()
        self.sees = sees

    async def main(self, msg: Message):
        focus = self.sees.focus
        if focus is None:
            # Scored on a stale reading, or the neuron was re-evaluated
            # between scoring and running.
            return self.fail()

        self.bot.focus = focus
        self.bot.state = 'seek'

        try:
            while self.ok():
                if self.bot.node.intersects(focus):
                    self.bot.state = ''
                    return self.succeed()
                self.bot.move_to(focus.position)
                await self.sleep()
        finally:
            # Runs on cancellation too. Code placed after the loop never
            # executed, because closing the coroutine raises GeneratorExit
            # at the await.
            if self.status is not Status.SUCCESS:
                self.bot.reset()


class Eat(Action):
    def __init__(self, sees):
        super().__init__()
        self.sees = sees

    async def main(self, msg: Message):
        focus = self.sees.focus
        if focus is None:
            return self.fail()

        self.bot.focus = focus
        self.bot.state = 'eat'

        try:
            while self.ok():
                if focus.is_munched():
                    node = self.bot.node
                    node.close_mouth()
                    node.energy = node.energy + focus.energy
                    self.bot.reset()
                    return self.succeed()
                await self.sleep()
        finally:
            if self.status is not Status.SUCCESS:
                self.bot.reset()


class SeesBall(Neuron):
    def __init__(self):
        super().__init__()
        self.focus = None

    def main(self):
        beacons = engine.sprite_engine.query(
            self.bot.x, self.bot.y, self.bot.sensor_range
        )
        self.focus = None
        for beacon in beacons:
            if isinstance(beacon.node, Ball):
                self.focus = beacon.node
                return 1
        return 0


class Kick(Action):
    def __init__(self, sees):
        super().__init__()
        self.sees = sees

    async def main(self, msg: Message):
        focus = self.sees.focus
        if focus is None:
            return self.fail()

        self.bot.focus = focus
        self.bot.state = 'kick'
        focus.receive_kick(self.bot.node.position, 200)
        self.bot.reset()
        return self.succeed()


class Wander(Action):
    async def main(self, msg: Message):
        # The movement itself happens in ReactiveBrain.state_wander via
        # update(). This just claims the state and yields one tick so the
        # utility node re-evaluates.
        self.bot.state = 'wander'
        await self.sleep()
        return self.fail()


class ReactiveBrain(WyggleBrain):
    def __init__(self, model):
        super().__init__(model)
        with root(self):
            with forever():
                with utility():
                    with neuron(SeesFood()) as sees_food:
                        with sequence():
                            with action(MoveTo(sees_food)):
                                pass
                            with action(Eat(sees_food)):
                                pass

                    with neuron(SeesBall()) as sees_ball:
                        with sequence():
                            with action(MoveTo(sees_ball)):
                                pass
                            with action(Kick(sees_ball)):
                                pass

                    with action(Wander()):
                        pass

    def update(self, delta_time: float = 1 / 60):
        super().update(delta_time)
        state = self.state
        if state == "wander":
            self.state_wander()
        elif state == "seek":
            self.state_seek()
        elif state == "eat":
            self.state_eat()
        elif state == "kick":
            self.state_kick()

    def state_wander(self):
        if self.at_goal():
            heading = self.get_clear_wander_direction()
            self.move_to(self.project(heading, self.sensor_range))
        self.move()

    def state_seek(self):
        self.move()

    def state_eat(self):
        if not self.focus:
            self.reset()
            return

        if self.munch_timer > 0:
            self.munch_timer -= 1
            return
        else:
            self.munch_timer = 10

        if self.node.face != "munchy":
            self.node.open_mouth()
        else:
            self.node.close_mouth()
            self.focus.receive_munch()

    def state_kick(self):
        self.move()