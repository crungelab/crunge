import unittest

from crunge.mia.run import *
from crunge.mia.run.context.yaml import YamlContext
from crunge.mia.assets import asset

class Test(unittest.TestCase):
    def test(self):
        ctx = YamlContext().load(asset('cleavers.yml'))
        print(ctx)

if __name__ == '__main__':
    unittest.main()
