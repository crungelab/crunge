import glm

from crunge import wgpu

from .texture import Texture


class Texture2dArray(Texture):
    def __init__(
        self,
        texture: wgpu.Texture,
        size: glm.ivec3,
    ):
        super().__init__(texture, size)
