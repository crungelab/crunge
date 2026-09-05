from typing import Any, Optional

import math
import random

import glm

from wyggles import world
from wyggles.wyggle.agent import WyggleAgent
from wyggles.game_entity import GameEntity
from wyggles.fruit import Fruit
from wyggles.ball import Ball

class DefaultWyggleAgent(WyggleAgent):
    def __init__(self, sprite):
        super().__init__(sprite)
        self.consider_timer = 0
        self.consider_max = 10
        self.munch_timer = 0

    def update(self, delta_time: float = 1 / 60):
        super().update(delta_time)
        state = self.state
        if state == "wanderer":
            self.wander()
        elif state == "hunter":
            self.hunt()
        elif state == "eater":
            self.eat()
        elif state == "kicker":
            self.kick()
        self.consider()

    def wander(self):
        if self.at_goal():
            self.move_to(self.wander_goal())
        self.move()

    '''
    def wander(self):
        if self.at_goal():
            pt = math.floor(random.random() * 3)
            pd = math.floor(random.random() * 45)
            if pt == 0:
                self.left(pd)
            elif pt == 2:
                self.right(pd)
            else:
                pass
            self.project(self.heading, self.sensor_range)
        self.move()
    '''

    def hunt(self):
        if self.entity.intersects(self.focus):
            self.state = "eater"
        self.move()

    def eat(self):
        if self.focus.is_munched:
            self.entity.close_mouth()
            self.entity.energy = self.entity.energy + self.focus.energy
            self.state = "wanderer"
            self.focus = None
            # self.node.grow()
            return
        # else
        self.munch()

    def munch(self):
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

    def kick(self):
        self.state = "kicker"
        self.move_to(self.focus.position)  # fixme: add--> follow(sprite)
        if glm.distance(self.entity.position, self.focus.position) < 1.0:
            self.focus.receive_kick(self.heading, .2)

        elif(glm.distance(self.entity.position, self.focus.position) > self.sensor_range):
            self.focus = None
            self.state = 'wanderer'

        self.move()

    def consider(self):
        if self.consider_timer > 0:
            self.consider_timer -= 1
            return
        else:
            self.consider_timer = self.consider_max

        entities = self.scan()
        #
        state = self.state
        if state == "wanderer":
            if not self.consider_eating(entities):
                self.consider_kicking(entities)
        elif state == "hunter":
            pass
        elif state == "eater":
            pass
        elif state == "kicker":
            pass
        # cleanup
        if entities != None:
            del entities

    def consider_eating(self, entities: list[GameEntity]):
        target_fruit = None
        for entity in entities:
            if isinstance(entity, Fruit):
                target_fruit = entity
                break
        #
        if target_fruit == None:
            return False
        # else
        self.focus = target_fruit
        self.move_to(target_fruit.position)
        self.state = "hunter"
        return True

    def consider_kicking(self, entities: list[GameEntity]):
        ball = None
        for entity in entities:
            if isinstance(entity, Ball):
                ball = entity
                break
        #
        if ball == None:
            return False
        # else
        self.focus = ball
        self.move_to(ball.position)
        self.state = "kicker"
        return True
