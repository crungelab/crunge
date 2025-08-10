from crunge import wgpu

from .image_texture_array import ImageTextureArray


class SpriteTexture(ImageTextureArray):
    @property
    def view(self) -> wgpu.TextureView:
        if self._view is not None:
            return self._view
        
        texture_view_desc = wgpu.TextureViewDescriptor(
            dimension=wgpu.TextureViewDimension.E2D_ARRAY,
        )

        self._view = self.texture.create_view(texture_view_desc)
        return self._view
