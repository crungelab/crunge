from typing import TYPE_CHECKING, Type, Dict, List, Any, Callable

if TYPE_CHECKING:
    from .scene_2d import Scene2D
    from .vu_2d import Vu2D

from loguru import logger
import glm

from ..math import Bounds2
from ..scene_node import SceneNode

class Node2D(SceneNode["Node2D", "Scene2D"]):
    def __init__(
        self,
        position=glm.vec2(),
        size=glm.vec2(1.0),
        scale=glm.vec2(1.0),
        vu: "Vu2D" = None,
        model=None,
    ) -> None:
        super().__init__(vu, model)
        self._position = position
        self._depth = 0.0
        self._rotation = 0.0  # radians
        self._size = size
        self._scale = scale
        self._matrix = glm.mat4(1.0)
        self.bounds = Bounds2()
        self.velocity = glm.vec2(0.0)
        self.angular_velocity = 0.0 # radians per second

        if vu is not None:
            self._size = vu.size

        '''
        if model is not None:
            self._size = model.size
        '''

        self.update_matrix()

    '''
    def _create(self):
        super()._create()
        if self.vu is not None:
            self.size = self.vu.size
    '''

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value: glm.vec2):
        self._position = value
        self.update_matrix()

    @property
    def x(self):
        return self._position.x
    
    @x.setter
    def x(self, value: float):
        self._position.x = value
        self.update_matrix()

    @property
    def y(self):
        return self._position.y
    
    @y.setter
    def y(self, value: float):
        self._position.y = value
        self.update_matrix()

    @property
    def depth(self):
        return self._depth

    @depth.setter
    def depth(self, value: float):
        self._depth = value
        self.update_matrix()

    @property
    def rotation(self):
        return self._rotation
    
    @rotation.setter
    def rotation(self, value: float):
        self._rotation = value
        self.update_matrix()

    @property
    def angle(self):
        return glm.degrees(self._rotation)

    @angle.setter
    def angle(self, value: float):
        self._rotation = glm.radians(value)
        # logger.debug(f"class: {self.__class__}, angle: {value}, rotation: {self._rotation}")
        self.update_matrix()

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value: glm.vec2):
        self._size = value
        self.update_matrix()

    @property
    def width(self):
        return self._size.x

    @width.setter
    def width(self, value: float):
        self._size.x = value
        self.update_matrix()

    @property
    def height(self):
        return self._size.y

    @height.setter
    def height(self, value: float):
        self._size.y = value
        self.update_matrix()

    @property
    def radius(self):
        return self._size.x / 2

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value: float):
        self._scale = value
        self.update_matrix()

    @property
    def matrix(self):
        return self._matrix
    
    @matrix.setter
    def matrix(self, value):
        self._matrix = value
        self.on_transform()
        '''
        if self.enabled:
            self.on_transform()
        '''
    @property
    def transform(self) -> glm.mat4:
        transform = self.matrix
        if self.parent is not None:
            transform = self.parent.transform * transform
        return transform

    def on_transform(self):
        #self.aabb = self.get_world_aabb()
        local_bounds = self.get_local_bounds()
        #logger.debug(f"class: {self.__class__}, local_bounds: {local_bounds}")
        self.bounds = local_bounds.to_global(self.transform)
        #logger.debug(f"class: {self.__class__}, bounds: {self.bounds}")

        '''
        if self.vu is not None:
            self.vu.transform = self.transform
        '''
        for listener in self.listeners:
            listener.on_node_transform_change(self)

    def update_matrix(self):
        x = self._position.x
        y = self._position.y
        #logger.debug(f"class: {self.__class__}, x: {x}, y: {y}")
        z = self._depth

        matrix = glm.mat4(1.0)  # Identity matrix
        matrix = glm.translate(matrix, glm.vec3(x, y, z))
        matrix = glm.rotate(matrix, self._rotation, glm.vec3(0, 0, 1))
        matrix = glm.scale(
            matrix,
            glm.vec3(self._scale.x, self._scale.y, 1),
        )
        self.matrix = matrix

    def get_local_bounds(self) -> Bounds2:
        half_width = self.size.x / 2
        half_height = self.size.y / 2
        return Bounds2(-half_width, -half_height, half_width, half_height)
