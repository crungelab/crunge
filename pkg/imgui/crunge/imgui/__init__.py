__version__ = '0.1.0'

import sys
import platform
from pathlib import Path

from . import _imgui
from ._imgui import *

from .extra import *

def add_plugin(location):
    LIB_PATH = Path(location).parent
    sys.path.insert(0, LIB_PATH)

add_plugin(__file__)

#TODO:Belongs on the c++ side?

VERTEX_BUFFER_POS_OFFSET = _imgui.get_vertex_buffer_vertex_pos_offset()
VERTEX_BUFFER_UV_OFFSET = _imgui.get_vertex_buffer_vertex_uv_offset()
VERTEX_BUFFER_COL_OFFSET = _imgui.get_vertex_buffer_vertex_col_offset()

VERTEX_SIZE = _imgui.get_vertex_buffer_vertex_size()
INDEX_SIZE = _imgui.get_index_buffer_index_size()

def rel(x, y):
    pos = _imgui.get_cursor_screen_pos()
    x1 = pos[0] + x
    y1 = pos[1] + y
    return x1, y1
