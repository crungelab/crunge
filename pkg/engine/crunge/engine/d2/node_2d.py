from typing import TYPE_CHECKING, Type, Dict, List, Any, Callable

if TYPE_CHECKING:
    from .scene_2d import Scene2D

from loguru import logger
import glm

from .renderer_2d import Renderer2D
from .vu_2d import Vu2D

from ..math import Vector2, Point2, Size2, Rect2
from ..scene_node import SceneNode

class Node2D(SceneNode["Node2D", Vu2D, "Scene2D", Renderer2D]):
    def __init__(
        self,
        position=Point2(),
        size=Size2(1.0),
        scale=Vector2(1.0),
        vu: Vu2D = None,
    ) -> None:
        super().__init__(vu)
        self._position = position
        self._depth = 0.0
        self._rotation = 0.0  # radians
        self._size = size
        self._scale = scale
        self._matrix = glm.mat4(1.0)
        self.aabb = Rect2(0, 0, 0, 0)

        if vu is not None:
            self._size = vu.size

        self.update_matrix()

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

    @property
    def transform(self) -> glm.mat4:
        transform = self.matrix
        if self.parent:
            transform = self.parent.transform * transform
        return transform

    def on_transform(self):
        self.aabb = self.get_world_aabb()

        if self.vu is not None:
            self.vu.transform = self.transform

    def update_matrix(self):
        x = self._position.x
        y = self._position.y
        z = self._depth

        matrix = glm.mat4(1.0)  # Identity matrix
        matrix = glm.translate(matrix, glm.vec3(x, y, z))
        matrix = glm.rotate(matrix, self._rotation, glm.vec3(0, 0, 1))
        matrix = glm.scale(
            matrix,
            glm.vec3(self._size.x * self._scale.x, self._size.y * self._scale.y, 1),
        )
        self.matrix = matrix

    def get_local_aabb(self) -> Rect2:
        half_width = self.size.x / 2
        half_height = self.size.y / 2
        return Rect2(-half_width, -half_height, self.size.x, self.size.y)

    def get_world_aabb(self) -> Rect2:
        """Create the transformed Rect2 for the sprite."""
        # Get the local bounding box
        local_rect = self.get_local_aabb()

        # Get the sprite's transformation matrix (position, scale, rotation)
        transform = self.transform  # This should be a 3x3 or 4x4 matrix that applies position, scale, and rotation

        # Get the four corners of the local rectangle
        corners = [
            glm.vec2(local_rect.x, local_rect.y),
            glm.vec2(local_rect.x + local_rect.width, local_rect.y),
            glm.vec2(local_rect.x, local_rect.y + local_rect.height),
            glm.vec2(local_rect.x + local_rect.width, local_rect.y + local_rect.height),
        ]

        # Transform each corner by the sprite's transform matrix
        transformed_corners = [glm.vec2(transform * glm.vec4(corner, 0, 1)) for corner in corners]

        # Calculate the AABB (axis-aligned bounding box) from the transformed corners
        min_x = min(corner.x for corner in transformed_corners)
        max_x = max(corner.x for corner in transformed_corners)
        min_y = min(corner.y for corner in transformed_corners)
        max_y = max(corner.y for corner in transformed_corners)

        # Return the new AABB in world space
        return Rect2(min_x, min_y, max_x - min_x, max_y - min_y)
