from typing import TYPE_CHECKING

from crunge import wgpu

from .image_texture_array import ImageTextureArray

if TYPE_CHECKING:
    from ..resource_group import ResourceGroup


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

    def add_to_group(self, group: "ResourceGroup"):
        group.texture_array_kit.add(self)
        return self
