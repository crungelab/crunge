import unittest

from crunge.abt.run import *
from crunge.abt.run.agent import Agent
from crunge.abt.run.policy import Rule

_Bob = term_("Bob")
_likes = term_("likes")
_Fish = term_("Fish")

_Joe = term_("Joe")
_likes = term_("likes")
_Turtles = term_("Turtles")

_x = var_("x")


class Test(unittest.TestCase):
    def test(self):
        c = Believe(_Bob, _likes, _Fish)
        print(c)
        m = Assert(c)
        print(m)

        agent = Agent()

        t = Trigger(Assert, Believe, _Bob, _likes, _Fish)
        print(t.match(m))

        t = Trigger(Assert, Believe, _Joe, _likes, _Fish)
        print(t.match(m))

        t = Trigger(Assert, Believe, _x, _likes, _Fish)
        print(t.match(m))

        async def action(task, msg):
            print("Match:", msg.data.obj)

        r = agent.subscribe(t, action)

        agent.post(m)
        agent.run()

if __name__ == "__main__":
    unittest.main()
