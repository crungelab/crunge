import unittest

from crunge.abt.run import *
from crunge.abt.run.act import *
from crunge.abt.run.agent import Agent

class MyAgent(Agent):
    def __init__(self):
        super().__init__()
        with root(self):
            with counter(1, 11):
                with action() as a:
                    async def fn(task, msg):
                        print('agent: ',task.agent)
                        print('count: ',task.parent.count)
                    a.use(fn)

class Test(unittest.TestCase):
    def test(self):
        agent = MyAgent()
        agent.run()

if __name__ == '__main__':
    unittest.main()