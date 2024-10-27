from ctypes import (
    Structure,
    c_float,
    c_uint32,
    sizeof,
    c_bool,
    c_int,
    c_void_p,
    cast,
    POINTER,
)

from loguru import logger
import numpy as np
import glm

from crunge.engine.d2.uniforms_2d import Vec2, Vec4

class Particle(Structure):
    _fields_ = [
        ("position", Vec2),
        ("velocity", Vec2),
        ("color", Vec4),
        ("age", c_float),
        ("lifespan", c_float),
        ("_pad1", c_float * 2),
    ]

assert sizeof(Particle) % 16 == 0
