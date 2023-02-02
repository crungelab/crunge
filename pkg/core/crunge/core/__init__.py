__version__ = '0.1.0'

import sys
from pathlib import Path

def add_plugin(location):
    LIB_PATH = Path(location).parent
    sys.path.insert(0, LIB_PATH)
