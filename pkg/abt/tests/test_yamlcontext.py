import unittest

from crunge.abt.run import *
from crunge.abt.run.context.yaml import YamlContext
from crunge.abt.assets import asset

class Test(unittest.TestCase):
    def test(self):
        ctx = YamlContext().load(asset('cleavers.yml'))
        print(ctx)

if __name__ == '__main__':
    unittest.main()
