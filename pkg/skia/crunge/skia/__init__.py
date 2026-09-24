__version__ = "0.1.0"

from crunge import core

core.add_plugin(__file__)

from ._skia import *

# TODO?

"""
import types

from . import _skia
from ._skia import *


class hybridmethod:
    def __init__(self, static, instance):
        self.static = static
        self.instance = instance

    def __get__(self, obj, cls=None):
        if obj is None:
            return self.static
        return types.MethodType(self.instance, obj)


def install_hybrids(module):
    for cls in list(vars(module).values()):
        if not isinstance(cls, type):
            continue
        for name in list(vars(cls)):
            if not name.endswith("_static"):
                continue
            base = name[: -len("_static")]
            if base in vars(cls):
                setattr(cls, base, hybridmethod(getattr(cls, name), getattr(cls, base)))


install_hybrids(_skia)
"""
