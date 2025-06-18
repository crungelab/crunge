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

from ..uniforms import Vec2, Vec3, Vec4, Mat4

class ViewportUniform(Structure):
    _fields_ = [
        ("size", Vec2),
        #("_pad1", c_float * 4),
    ]

class CameraUniform(Structure):
    _fields_ = [
        ("projection", Mat4),
        ("view", Mat4),
        #("viewport", Vec2),
        ("position", Vec3),
        ("_pad1", c_float * 4),
    ]


#assert sizeof(CameraUniform) % 16 == 0

class ModelUniform(Structure):
    _fields_ = [
        ("transform", Mat4),
    ]

assert sizeof(ModelUniform) % 16 == 0


class SpriteUniform(Structure):
    _fields_ = [
        ("color", Vec4),
        ("rect", Vec4),
        ("texture_size", Vec2),
        ("flip_h", c_uint32),
        ("flip_v", c_uint32),
        ("_pad1", c_float * 4),
    ]

assert sizeof(SpriteUniform) % 16 == 0


class ShapeUniform(Structure):
    _fields_ = [
        ("color", Vec4),
    ]

assert sizeof(SpriteUniform) % 16 == 0


class LightUniform(Structure):
    _fields_ = [
        ("position", Vec3),
        ("color", Vec3),
        ("range", c_float),
        ("intensity", c_float),
        ("_pad1", c_float * 2),
    ]


#assert sizeof(LightUniform) % 16 == 0
