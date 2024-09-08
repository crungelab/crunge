from typing import TYPE_CHECKING, Type, Dict, List, Any, Callable

if TYPE_CHECKING:
    from .scene_2d import Scene2D

from loguru import logger
import glm

from .renderer_2d import Renderer2D
from .vu_2d import Vu2D

from ..node import Node

class Node2D(Node["Node2D", "Scene2D", Renderer2D]):
    def __init__(
        self,
        position=glm.vec2(),
        size=glm.vec2(1.0),
        scale=glm.vec2(1.0),
        vu: Vu2D = None,
    ) -> None:
        super().__init__(vu)
        self._position = position
        self._depth = 0.0
        self._rotation = 0.0  # radians
        self._size = size
        self._scale = scale
        self.transform = glm.mat4(1.0)

        if vu is not None:
            self._size = vu.size

        self.update_transform()

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value: glm.vec2):
        self._position = value
        self.update_transform()

    @property
    def x(self):
        return self._position.x
    
    @x.setter
    def x(self, value: float):
        self._position.x = value
        self.update_transform()

    @property
    def y(self):
        return self._position.y
    
    @y.setter
    def y(self, value: float):
        self._position.y = value
        self.update_transform()

    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self, value: float):
        self._depth = value
        self.update_transform()

    @property
    def angle(self):
        return glm.degrees(self._rotation)

    @angle.setter
    def angle(self, value: float):
        self._rotation = glm.radians(value)
        # logger.debug(f"class: {self.__class__}, angle: {value}, rotation: {self._rotation}")
        self.update_transform()

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value: glm.vec2):
        self._size = value
        self.update_transform()

    @property
    def width(self):
        return self._size.x

    @width.setter
    def width(self, value: float):
        self._size.x = value
        self.update_transform()

    @property
    def height(self):
        return self._size.y

    @height.setter
    def height(self, value: float):
        self._size.y = value
        self.update_transform()

    @property
    def radius(self):
        return self._size.x / 2

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value: float):
        self._scale = value
        self.update_transform()

    def update_transform(self):
        x = self._position.x
        y = self._position.y
        z = self._depth

        model = glm.mat4(1.0)  # Identity matrix
        model = glm.translate(model, glm.vec3(x, y, z))
        model = glm.rotate(model, self._rotation, glm.vec3(0, 0, 1))
        model = glm.scale(
            model,
            glm.vec3(self._size.x * self._scale.x, self._size.y * self._scale.y, 1),
        )
        self.transform = model

        if self.vu is not None:
            self.vu.transform = self.transform
