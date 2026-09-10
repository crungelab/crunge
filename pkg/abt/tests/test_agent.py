import unittest

from crunge.abt.run import *
from crunge.abt.run import _I
from crunge.abt.run.agent import Agent
from crunge.abt.run.message import *
from crunge.abt.run.rule_kit import rule, RuleKit

_jump = term_('jump')
_say = term_('say')
_x_ = var_('x')

class MyAgent(Agent):
    def __init__(self):
        super().__init__()
        #print(self.__class__.rules)
        print(self.get_cls_chip(RuleKit))
        self.post(attempt_(Achieve, _I, _jump))
        self.post(attempt_(Achieve, _I, _say, 'Howdy Folks!'))

    @rule(OnAttempt(Achieve, _I, _jump))
    async def howhigh(self, msg):
        print('How high?')
        print(msg)

    @rule(OnAttempt(Achieve, _I, _say, _x_))
    async def howdy(self, msg):
        print(msg.data.obj)
        print(msg)

class Test(unittest.TestCase):
    def test(self):
        agent = MyAgent()
        agent.run()

if __name__ == '__main__':
    unittest.main()