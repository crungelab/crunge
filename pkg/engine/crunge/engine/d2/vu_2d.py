from loguru import logger
import glm

from ..math import Rect2, Bounds2

from ..vu import Vu

from .node_2d import Node2D

class Vu2D(Vu[Node2D]):
    def __init__(self) -> None:
        super().__init__()
        self._transform = glm.mat4(1.0)
        self.bounds = Bounds2()

    @property
    def transform(self) -> glm.mat4:
        return self._transform
    
    @transform.setter
    def transform(self, value: glm.mat4):
        self._transform = value
        self.on_transform()

    def on_transform(self):
        pass

    @property
    def size(self) -> glm.vec2:
        raise NotImplementedError

    def on_node_transform_change(self, node: Node2D) -> None:
        matrix = glm.mat4(1.0)  # Identity matrix
        #matrix = glm.translate(matrix, glm.vec3(x, y, z))
        #matrix = glm.rotate(matrix, self._rotation, glm.vec3(0, 0, 1))
        matrix = glm.scale(
            matrix,
            glm.vec3(self.size.x , self.size.y, 1),
        )

        self.transform = node.transform * matrix
        #logger.debug(f"Vu2D: {self.transform}")
        self.bounds = node.bounds
