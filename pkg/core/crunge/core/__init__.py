__version__ = '0.1.0'

import sys
from pathlib import Path

from .base_node import BaseNode
from .signal import Signal, Pulse

from .utils import as_capsule, from_capsule, pointer_to_memoryview

def add_plugin(location):
    LIB_PATH = Path(location).parent
    sys.path.insert(0, LIB_PATH)
