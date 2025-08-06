from typing import List
import glm

from crunge import wgpu

from ..image import Image

from .texture_2d_array import Texture2dArray


class ImageTextureArray(Texture2dArray):
    def __init__(
        self,
        texture: wgpu.Texture,
        size: glm.ivec2,
        images: List[Image],
    ):
        super().__init__(texture, size)
        self.images = images
