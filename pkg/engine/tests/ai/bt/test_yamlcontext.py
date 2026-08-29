import unittest

from crunge.engine.ai.bt.run import *
from crunge.engine.ai.bt.run.context.yaml import YamlContext
from crunge.engine.ai.bt.assets import asset

class Test(unittest.TestCase):
    def test(self):
        ctx = YamlContext().load(asset('cleavers.yml'))
        print(ctx)

if __name__ == '__main__':
    unittest.main()
