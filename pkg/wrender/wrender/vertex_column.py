from ctypes import Structure, c_float, c_uint32, sizeof, c_bool, c_int, c_void_p

import numpy as np

from crunge import wgpu

class VertexColumn:
    struct: Structure
    name: str
    data: np.ndarray
    location: int = None

    def __init__(self, name: str, data: np.ndarray) -> None:
        self.name = name
        self.data = data

    @property
    def struct_size(self):
        return sizeof(self.struct)
    
    @property
    def type(self):
        if self.name == 'pos':
            return "vec4<f32>"
        elif self.format == wgpu.VertexFormat.FLOAT32X2:
            return "vec2<f32>"
        elif self.format == wgpu.VertexFormat.FLOAT32X3:
            return "vec3<f32>"
        elif self.format == wgpu.VertexFormat.FLOAT32X4:
            return "vec4<f32>"
        
    @property
    def input_type(self):
        return self.type

    @property
    def output_type(self):
        return self.type

class Vec3(Structure):
    _fields_ = [
        ("x", c_float),
        ("y", c_float),
        ("z", c_float),
    ]

class Vec4(Structure):
    _fields_ = [
        ("x", c_float),
        ("y", c_float),
        ("z", c_float),
        ("w", c_float),
    ]

class Position(Vec3):
    pass

class PosColumn(VertexColumn):
    struct = Position
    format = wgpu.VertexFormat.FLOAT32X3

class Normal(Vec3):
    pass

class NormalColumn(VertexColumn):
    struct = Normal
    format = wgpu.VertexFormat.FLOAT32X3

class Tangent(Vec4):
    pass

class TangentColumn(VertexColumn):
    struct = Tangent
    format = wgpu.VertexFormat.FLOAT32X4

    @property
    def output_type(self):
        return "vec3<f32>"

'''
class BiTangent(Vec3):
    pass

class BiTangentColumn(VertexColumn):
    struct = BiTangent
    format = wgpu.VertexFormat.FLOAT32X3
'''

class UvCoord(Structure):
    _fields_ = [
        ("u", c_float),
        ("v", c_float),
    ]

class UvColumn(VertexColumn):
    struct = UvCoord
    format = wgpu.VertexFormat.FLOAT32X2

class RgbaColor(Structure):
    _fields_ = [
        ("r", c_float),
        ("g", c_float),
        ("b", c_float),
        ("a", c_float),
    ]

class RgbaColumn(VertexColumn):
    struct = RgbaColor
    format = wgpu.VertexFormat.FLOAT32X4
