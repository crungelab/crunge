class BindGroupIndex:
    SCENE = 0
    MATERIAL = 1
    MODEL = 2
    NODE = 3


from .material import (
    MaterialBindGroup,
    MaterialBindGroupLayout,
    MaterialBindIndex,
)
from .model import ModelBindGroup, ModelBindGroupLayout, DynamicModelBindGroupLayout, ModelBindIndex
from .node import NodeBindGroup, NodeBindGroupLayout, DynamicNodeBindGroupLayout, NodeBindIndex
from .emitter import EmitterBindGroup, EmitterBindGroupLayout, EmitterBindIndex
