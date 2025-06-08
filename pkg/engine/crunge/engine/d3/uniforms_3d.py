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

from ..uniforms import Vec3, Mat4

class CameraUniform(Structure):
    _fields_ = [
        ("projection", Mat4),
        ("view", Mat4),
        ("position", Vec3),
    ]


assert sizeof(CameraUniform) % 16 == 0


class ModelUniform(Structure):
    _fields_ = [
        ("model_matrix", Mat4),
        # ("normal_matrix", Mat3),
        ("normal_matrix", Mat4),
    ]


assert sizeof(ModelUniform) % 16 == 0


class AmbientLightUniform(Structure):
    _fields_ = [
        ("color", Vec3),
        ("energy", c_float),
        ("_pad2", c_float * 7),
    ]
    # 48 bytes


assert sizeof(AmbientLightUniform) % 16 == 0
logger.debug(f"sizeof(AmbientLightUniform): {sizeof(AmbientLightUniform)}")
assert sizeof(AmbientLightUniform) == 48

'''
class LightUniform(Structure):
    _fields_ = [
        ("position", Vec3),
        ("color", Vec3),
        ("range", c_float),
        ("_pad1", c_float * 3), # pad to 16 bytes (range + 3*pad = 16)
        ("energy", c_float),
        ("_pad2", c_float * 3),
        # ("_pad1", c_float * 2),
    ]

# Total size: 16 (position) + 16 (color) + 16 (rest) = 48 bytes, which is 3 * 16 bytes

#assert sizeof(LightUniform) == 48
assert sizeof(LightUniform) % 16 == 0
'''

class LightUniform(Structure):
    _fields_ = [
        ("position", Vec3),   # 16 bytes
        ("color", Vec3),      # 16 bytes
        ("range", c_float),   # 4 bytes
        ("energy", c_float),  # 4 bytes
        ("_pad1", c_float * 2),  # pad to 16 bytes (range + energy + 2*pad = 16)
    ]

# Total size: 16 (position) + 16 (color) + 16 (rest) = 48 bytes, which is 3 * 16 bytes

assert sizeof(LightUniform) == 48
assert sizeof(LightUniform) % 16 == 0

'''
class LightUniform(Structure):
    _fields_ = [
        ("position", Vec3),
        ("color", Vec3),
        ("range", c_float),
        ("_pad1", c_float),
        ("energy", c_float),
        ("_pad2", c_float),
        # ("_pad1", c_float * 2),
    ]


assert sizeof(LightUniform) % 16 == 0
'''