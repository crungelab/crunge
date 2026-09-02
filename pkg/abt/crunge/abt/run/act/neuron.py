import types
from loguru import logger

from .helpers import *


class Neuron:
    def __init__(self):
        pass

    @property
    def activity(self):
        level = self.main()
        #logger.debug(f"neuron level: {level}")
        return level

    def activate(self):
        pass

    def deactivate(self):
        pass

    def main(self):
        return 1

    def use(self, fn):
        self.main = types.MethodType(fn, self)


@contextmanager
def neuron(neuron=None):
    if not neuron:
        neuron = Neuron()
    ctx = neuron_ctx_enter(neuron)
    yield neuron
    neuron_ctx_exit(ctx)
