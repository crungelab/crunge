import glm

from crunge import wgpu

from ..image import Image

from .texture_2d import Texture2D


class ImageTexture(Texture2D):
    def __init__(
        self,
        texture: wgpu.Texture,
        size: glm.ivec2,
        image: Image,
    ):
        super().__init__(texture, size)
        self.image = image
