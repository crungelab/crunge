class BindGroupIndex:
    SCENE = 0
    MATERIAL = 1
    MODEL = 2
    NODE = 3


from .material import (
    SpriteBindGroup,
    SpriteBindGroupLayout,
    SpriteBindIndex,
    ShapeBindGroup,
    ShapeBindGroupLayout,
    ShapeBindIndex,
)
from .model import ModelBindGroup, ModelBindGroupLayout, ModelBindIndex
from .node import NodeBindGroup, NodeBindGroupLayout, NodeBindIndex
from .emitter import EmitterBindGroup, EmitterBindGroupLayout, EmitterBindIndex
