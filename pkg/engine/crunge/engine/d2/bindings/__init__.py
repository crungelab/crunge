class BindGroupIndex:
    # VIEWPORT = 0
    CAMERA = 0
    # LIGHT = 2
    MATERIAL = 1
    MODEL = 2

from .camera import CameraBindGroup, CameraBGL, CameraBindIndex
from .material import MaterialBindGroup, MaterialBGL, MaterialBindIndex
from .model import ModelBindGroup, ModelBGL, ModelBindIndex
