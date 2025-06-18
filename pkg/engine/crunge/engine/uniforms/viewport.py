from ctypes import Structure, c_float
from . import Vec2

class ViewportUniform(Structure):
    _fields_ = [
        ("size", Vec2),
        #("_pad1", c_float * 4),
    ]
