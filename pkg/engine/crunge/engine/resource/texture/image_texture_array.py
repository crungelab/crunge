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
        images: List[Image] = [],
    ):
        super().__init__(texture, size)
        self.images = images

    @property
    def view(self) -> wgpu.TextureView:
        if self._view is not None:
            return self._view
        
        texture_view_desc = wgpu.TextureViewDescriptor(
            dimension=wgpu.TextureViewDimension.E2D_ARRAY,
        )

        self._view = self.texture.create_view(texture_view_desc)
        return self._view
