class BindGroupIndex:
    # VIEWPORT = 0
    CAMERA = 0
    # LIGHT = 2
    MATERIAL = 1
    MODEL = 2


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
