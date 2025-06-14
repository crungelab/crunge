from enum import auto, IntEnum

class GroupIndex(IntEnum):
    #VIEWPORT = auto()
    CAMERA = auto()
    #LIGHT = auto()
    MATERIAL = auto()
    MODEL = auto()


class ViewportIndex(IntEnum):
    VIEWPORT = auto()

class CameraIndex(IntEnum):
    CAMERA = auto()

class LightIndex(IntEnum):
    LIGHT = auto()
    LIGHT_COUNT = auto()
    LIGHTS = auto()
    SHADOW_MAP = auto()
    SHADOW_MAP_SAMPLER = auto()

class MaterialIndex(IntEnum):
    TEXTURE = auto()
    SAMPLER = auto()
    MATERIAL = auto()

class ModelIndex(IntEnum):
    MODEL = auto()
