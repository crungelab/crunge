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

# MAT4_SIZE = 4 * 4 * 4


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
        ("model_matrix", Mat4),
        ("transform_matrix", Mat4),
        ("normal_matrix", Mat3),
        ("position", Vec3),
    ]


assert sizeof(CameraUniform) % 16 == 0


class LightUniform(Structure):
    _fields_ = [
        ("position", Vec3),
        ("color", Vec3),
        ("range", c_float),
        ("intensity", c_float),
        ("_pad1", c_float * 2),
    ]


assert sizeof(LightUniform) % 16 == 0


def cast_matrix4(matrix):
    ptr = glm.value_ptr(matrix)
    return cast(ptr, POINTER(c_float * 16)).contents


def cast_matrix3(matrix):
    ptr = glm.value_ptr(matrix)
    return cast(ptr, POINTER(c_float * 9)).contents


def cast_vec3(vec):
    return Vec3(vec.x, vec.y, vec.z, 0.0)
