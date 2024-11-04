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

from ..uniforms import Vec3, Vec4, Mat4

class CameraUniform(Structure):
    _fields_ = [
        ("projection", Mat4),
        ("view", Mat4),
        ("position", Vec3),
    ]


assert sizeof(CameraUniform) % 16 == 0

class ModelUniform(Structure):
    _fields_ = [
        ("transform", Mat4),
    ]

assert sizeof(ModelUniform) % 16 == 0


class MaterialUniform(Structure):
    _fields_ = [
        ("color", Vec4),
        ("uvs", Vec4 * 4),
    ]

assert sizeof(ModelUniform) % 16 == 0

class LightUniform(Structure):
    _fields_ = [
        ("position", Vec3),
        ("color", Vec3),
        ("range", c_float),
        ("intensity", c_float),
        ("_pad1", c_float * 2),
    ]


assert sizeof(LightUniform) % 16 == 0
