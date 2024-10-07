import glm

from crunge import wgpu


class Viewport:
    def __init__(self, width: int, height: int, surface: wgpu.Surface):
        self._size = glm.ivec2(width, height)
        self.surface = surface

    @property
    def size(self) -> glm.ivec2:
        return self._size
    
    @size.setter
    def size(self, value: glm.ivec2):
        changed = self._size != value
        self._size = value
        if changed:
            self.on_size(value)

    def on_size(self):
        pass

    @property
    def width(self) -> int:
        return self._size.x

    @property
    def height(self) -> int:
        return self._size.y
