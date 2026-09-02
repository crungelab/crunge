import unittest

from crunge.abt.run.act import *


class Test(unittest.TestCase):
    def test(self):
        with timer(0.1) as top:
            with counter(1, 1000) as cntr:
                with action() as a:

                    async def fn(task, msg):
                        print("a count: ", cntr.count)

                    a.use(fn)

        top.run()


if __name__ == "__main__":
    unittest.main()
