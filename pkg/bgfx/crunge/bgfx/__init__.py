__version__ = '0.1.0'

from crunge import core

core.add_plugin(__file__)

from ._bgfx import *
from .constants import *

def set_platform_data(platform_data):
    platform_data.set()