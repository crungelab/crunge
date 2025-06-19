class BindGroupIndex:
    VIEWPORT = 0
    CAMERA = 1
    # LIGHT = 2
    MATERIAL = 2
    MODEL = 3


from .camera import CameraBindGroup, CameraBindGroupLayout, CameraBindIndex
from .material import (
    SpriteBindGroup,
    SpriteBindGroupLayout,
    SpriteBindIndex,
    ShapeBindGroup,
    ShapeBindGroupLayout,
    ShapeBindIndex,
)
from .model import ModelBindGroup, ModelBindGroupLayout, ModelBindIndex
from .emitter import EmitterBindGroup, EmitterBindGroupLayout, EmitterBindIndex
