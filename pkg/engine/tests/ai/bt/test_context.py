import unittest

from crunge.engine.ai.bt.run import *
from crunge.engine.ai.bt.run.context import Context

_Bob = term_('Bob')
_likes = term_('likes')
_Toast = term_('Toast')

class Test(unittest.TestCase):
    def test(self):
        ctx = Context()
        ctx.add(believe_(_Bob, _likes, _Toast))
        print(ctx)

    def test_reactive(self):
        ctx = Context()
        ctx.add(believe_(_Bob, _likes, _Toast))
        print(ctx)

if __name__ == '__main__':
    unittest.main()