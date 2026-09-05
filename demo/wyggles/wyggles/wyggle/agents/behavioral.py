#
# A purely behavioral brain
#
import math
import random

from crunge.abt.run import *
from crunge.abt.run import _I
from crunge.abt.run.act import *

from wyggles import world
from wyggles.wyggle.agent import WyggleAgent
from wyggles.fruit import Fruit
from wyggles.ball import Ball

_see = term_('see')

class SeesFood(Sequence):
    def __init__(self):
        super().__init__()
        self.focus = None

    async def main(self, msg: Message):
        entities = self.agent.scan()
        self.focus = None
        for entity in entities:
            if isinstance(entity, Fruit):
                self.focus = entity
                break
        else:
            return self.fail()

        self.post(Assert(Believe(_I, _see, self.focus)))
        await super().main(msg)

class Seek(Action):
    def __init__(self, sees):
        super().__init__()
        self.sees = sees

    async def main(self, msg: Message):
        self.agent.focus = focus = self.sees.focus
        self.agent.state = 'seek'
        while self.ok():
            if self.agent.entity.intersects(focus):
                self.agent.state = ''
                return self.succeed()
            self.agent.move_to(focus.position)
            await self.sleep()

class Eat(Action):
    def __init__(self, sees):
        super().__init__()
        self.sees = sees

    async def main(self, msg: Message):
        self.agent.focus = focus = self.sees.focus
        self.agent.state = 'eat'
        
        while self.ok():
            if focus.is_munched:
                sprite = self.agent.entity
                sprite.close_mouth()
                sprite.energy = sprite.energy + focus.energy
                self.agent.reset()
                return self.succeed()
            await self.sleep()

class SeesBall(Sequence):
    def __init__(self):
        super().__init__()
        self.focus = None

    async def main(self, msg: Message):
        entities = self.agent.scan()
        self.focus = None
        for entity in entities:
            if isinstance(entity, Ball):
                self.focus = entity
                break
        else:
            return self.fail()
        self.post(Assert(Believe(_I, _see, self.focus)))
        await super().main(msg)

class Kick(Action):
    def __init__(self, sees):
        super().__init__()
        self.sees = sees

    async def main(self, msg: Message):
        self.agent.focus = focus = self.sees.focus
        self.agent.state = 'kick'
        focus.receive_kick(self.agent.heading, .2)
        self.agent.reset()

class Wander(Action):
    async def main(self, msg: Message):
        self.agent.state = 'wander'
        while self.ok():
            await self.sleep()
            return self.fail()

class BehavioralWyggleAgent(WyggleAgent):
    def __init__(self, model):
        super().__init__(model)
        self.munch_timer = 10

        with root(self):
            with forever():
                with selector():
                    with sequence(SeesFood()) as sees_food:
                        with action(Seek(sees_food)):
                            pass
                        with action(Eat(sees_food)):
                            pass
                    
                    with sequence(SeesBall()) as sees_ball:
                        with action(Seek(sees_ball)):
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
            pt = math.floor(random.random() * 3)
            pd = math.floor(random.random() * 45)
            if pt == 0:
                self.left(pd)
            elif pt == 2:
                self.right(pd)
            else:
                pass
            self.project(self.sensor_range)
        self.move()

    def state_seek(self):
        self.move()

    def state_eat(self):
        if self.munch_timer > 0:
            self.munch_timer -= 1
            return
        else:
            self.munch_timer = 10

        if self.entity.face != "munchy":
            self.entity.open_mouth()
        else:
            self.entity.close_mouth()
            self.focus.receive_munch()

    def state_kick(self):
        self.move()
