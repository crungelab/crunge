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

import glm


class Vec2(Structure):
    _fields_ = [
        ("x", c_float),
        ("y", c_float),
    ]


# assert sizeof(Vec2) % 16 == 0
# assert sizeof(Vec2) == 16


class Vec3(Structure):
    _fields_ = [
        ("x", c_float),
        ("y", c_float),
        ("z", c_float),
        ("_pad", c_float),
    ]  # Padding to ensure 16-byte alignment


assert sizeof(Vec3) % 16 == 0
assert sizeof(Vec3) == 16


class Vec4(Structure):
    _fields_ = [
        ("x", c_float),
        ("y", c_float),
        ("z", c_float),
        ("w", c_float),
    ]  # Padding to ensure 16-byte alignment


assert sizeof(Vec4) % 16 == 0
assert sizeof(Vec4) == 16


class Mat3(Structure):
    _fields_ = [
        ("data", c_float * 9),
        ("_pad1", c_float * 3),
    ]  # GLM uses column-major order
    # _fields_ = [("data", c_float * 9), ("_pad1", c_float * 3)]  # Padding after each vec3


assert sizeof(Mat3) % 16 == 0
assert sizeof(Mat3) == 48


class Mat4(Structure):
    _fields_ = [("data", c_float * 16)]  # GLM uses column-major order


assert sizeof(Mat4) % 16 == 0
assert sizeof(Mat4) == 64


def cast_vec2(vec: glm.vec2):
    return Vec2(vec.x, vec.y)

def cast_vec3(vec: glm.vec3):
    return Vec3(vec.x, vec.y, vec.z, 0.0)


def cast_vec4(vec: glm.vec4):
    return Vec4(vec.x, vec.y, vec.z, vec.w)


def cast_matrix4(matrix: glm.mat4):
    ptr = glm.value_ptr(matrix)
    return cast(ptr, POINTER(c_float * 16)).contents


def cast_matrix3(matrix: glm.mat3):
    ptr = glm.value_ptr(matrix)
    return cast(ptr, POINTER(c_float * 9)).contents
