class BindGroupIndex:
    #VIEWPORT = 0
    CAMERA = 0

#from .viewport import ViewportBindGroup, ViewportBindGroupLayout, ViewportBindIndex
from .camera import (
    CameraBindGroup,
    CameraBindGroupLayout,
    CameraBindIndex,
)