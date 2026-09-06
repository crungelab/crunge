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

from ..uniforms import Vec2, Vec3, Vec4, Mat4, ViewportUniform, CameraUniform


class NodeUniform(Structure):
    _fields_ = [
        ("transform", Mat4),
        ("color", Vec4),
        ("model_index", c_uint32),
        ("_pad1", c_float * 3),
    ]


assert sizeof(NodeUniform) % 16 == 0


class ModelUniform(Structure):
    _fields_ = [
        ("color", Vec4),
        ("rect", Vec4),
        ("texture_size", Vec2),
        ("flip_flags", c_uint32),
        ("texture_layer", c_int),
    ]


# assert sizeof(ModelUniform) % 16 == 0


class ParticleUniform(Structure):
    _fields_ = [
        ("position", Vec2),
        ("velocity", Vec2),
        ("color", Vec4),
        ("age", c_float),
        ("lifespan", c_float),
        ("_pad1", c_float * 2),
    ]


assert sizeof(ParticleUniform) % 16 == 0
