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


class Vec3(Structure):
    _fields_ = [
        ("x", c_float),
        ("y", c_float),
        ("z", c_float),
        ("_pad", c_float),
    ]  # Padding to ensure 16-byte alignment


assert sizeof(Vec3) % 16 == 0
assert sizeof(Vec3) == 16


class Mat4(Structure):
    _fields_ = [("data", c_float * 16)]  # GLM uses column-major order


assert sizeof(Mat4) % 16 == 0
assert sizeof(Mat4) == 64


class Mat3(Structure):
    _fields_ = [
        ("data", c_float * 9),
        ("_pad1", c_float * 3),
    ]  # GLM uses column-major order
    # _fields_ = [("data", c_float * 9), ("_pad1", c_float * 3)]  # Padding after each vec3


assert sizeof(Mat3) % 16 == 0
assert sizeof(Mat3) == 48


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


def cast_matrix4(matrix: glm.mat4):
    ptr = glm.value_ptr(matrix)
    return cast(ptr, POINTER(c_float * 16)).contents


def cast_matrix3(matrix: glm.mat3):
    ptr = glm.value_ptr(matrix)
    return cast(ptr, POINTER(c_float * 9)).contents


def cast_vec3(vec: glm.vec3):
    return Vec3(vec.x, vec.y, vec.z, 0.0)
