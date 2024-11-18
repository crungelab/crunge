import glm

from crunge import wgpu

from .texture import Texture


class Texture2D(Texture):
    def __init__(
        self,
        texture: wgpu.Texture,
        size: glm.ivec2,
    ):
        super().__init__(texture, glm.ivec3(size, 1))
