__version__ = '0.1.0'

import sys
from pathlib import Path

from kcore import DispatchResult, EVENT_HANDLED, EVENT_UNHANDLED, Base, BaseNode, Chip, Signal, Pulse
from kcore import klass

from .utils import as_capsule, from_capsule, pointer_to_memoryview

def add_plugin(location):
    LIB_PATH = Path(location).parent
    sys.path.insert(0, LIB_PATH)
