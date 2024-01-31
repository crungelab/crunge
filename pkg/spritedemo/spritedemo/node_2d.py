import glm

from .node import Node

class Node2D(Node):
    def __init__(self) -> None:
        super().__init__()
        self._position = glm.vec2(0.0)
        self._depth = 0.0
        self._rotation = 0.0
        self._size = glm.vec2(1.0)
        self._scale = glm.vec2(1.0)
        self.update_transform()

    @property
    def position(self):
        return self._position
    
    @position.setter
    def position(self, value: glm.vec2):
        self._position = value
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
        #return self._angle
        return glm.degrees(self._rotation)
    
    @angle.setter
    def angle(self, value: float):
        #self._angle = value
        self._rotation = glm.radians(value)
        self.update_transform()

    @property
    def size(self):
        return self._size
    
    @size.setter
    def size(self, value: glm.vec2):
        self._size = value
        self.update_transform()

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

        model = glm.mat4(1.0)  # Identity matrix
        model = glm.translate(model, glm.vec3(x, y, 0))
        model = glm.rotate(model, self._rotation, glm.vec3(0, 0, 1))
        model = glm.scale(model, glm.vec3(self._size.x * self._scale.x, self._size.y * self._scale.y, 1))
        self.transform = model
