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
        ("size", Vec2),  # node size in local units, before node scale
        ("model_index", c_uint32),
        ("_pad1", c_float),
    ]


class ModelUniform(Structure):
    _fields_ = [
        ("color", Vec4),
        ("rect", Vec4),
        ("texture_size", Vec2),
        ("flip_flags", c_uint32),
        ("texture_layer", c_int),
    ]


class NinePatchUniform(ModelUniform):
    # ctypes appends subclass fields after the base's, which is exactly the
    # prefix the WGSL struct relies on
    _fields_ = [
        ("insets", Vec4),  # normalized left, top, right, bottom
        ("border_scale", c_float),  # texels -> local units (border_zoom / ppu)
        ("fill_flags", c_uint32),  # NinePatchFill
        ("_pad", c_float * 2),  # WGSL rounds the struct up to 80
    ]

'''
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
'''

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
