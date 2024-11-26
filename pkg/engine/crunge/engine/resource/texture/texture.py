from typing import TYPE_CHECKING

from loguru import logger
import glm

from crunge import wgpu

from ..resource import Resource

if TYPE_CHECKING:
    from ..resource_group import ResourceGroup


class Texture(Resource):
    def __init__(
        self,
        texture: wgpu.Texture,
        size: glm.ivec3,
    ):
        super().__init__()
        self.texture = texture
        self._size = size

        self._view: wgpu.TextureView = None
        self.sampler: wgpu.Sampler = None

    def __str__(self):
        #return f"Texture(id={self.id}, name={self.name}, path={self.path}, texture={self.texture}, size={self.size})"
        return f"{self.__class__.__name__}(id={self.id}, name={self.name}, path={self.path}, texture={self.texture}, size={self.size})"

    def __repr__(self):
        return str(self)

    """
    def __repr__(self):
        return f"{self.__class__.__name__}({self.texture}, {self.x}, {self.y}, {self.width}, {self.height}, {self.coords})"
    """

    @property
    def size(self) -> glm.ivec3:
        return self._size

    @size.setter
    def size(self, value: glm.ivec3):
        changed = self._size != value
        self._size = value
        if changed:
            self.on_size()

    def on_size(self) -> None:
        pass

    @property
    def width(self) -> int:
        return self._size.x

    @property
    def height(self) -> int:
        return self._size.y

    @property
    def view(self) -> wgpu.TextureView:
        if self._view is None:
            self._view = self.texture.create_view()
        return self._view

    @view.setter
    def view(self, view: wgpu.TextureView):
        self._view = view

    def add_to_group(self, group: "ResourceGroup"):
        group.texture_kit.add(self)
        return self
