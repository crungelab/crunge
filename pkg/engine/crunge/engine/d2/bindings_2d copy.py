from enum import auto, IntEnum

class BindGroupIndex(IntEnum):
    #VIEWPORT = auto()
    CAMERA = auto()
    #LIGHT = auto()
    MATERIAL = auto()
    MODEL = auto()


class ViewportBinding(IntEnum):
    VIEWPORT = auto()

class CameraBinding(IntEnum):
    CAMERA_UNIFORM = auto()

class LightBinding(IntEnum):
    LIGHT = auto()
    LIGHT_COUNT = auto()
    LIGHTS = auto()
    SHADOW_MAP = auto()
    SHADOW_MAP_SAMPLER = auto()

class MaterialBinding(IntEnum):
    TEXTURE = auto()
    SAMPLER = auto()
    MATERIAL = auto()

class ModelBinding(IntEnum):
    MODEL = auto()

class BindingIndex:
    class Camera(IntEnum):
        CAMERA_UNIFORM = 0

    class Light(IntEnum):
        LIGHT_UNIFORM = 0
        LIGHT_COUNT = 1
        SHADOW_MAP = 2
        SHADOW_MAP_SAMPLER = 3

'''
class Binding:
    def __init__(self, binding: IntEnum, group: BindGroupIndex):
        self.binding = binding
        self.group = group

    def __repr__(self):
        return f"Binding(binding={self.binding}, group={self.group})"
'''