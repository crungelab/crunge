from loguru import logger
import glm

from ..math import Rect2, Bounds2

from ..vu import Vu

from .node_2d import Node2D

class Vu2D(Vu[Node2D]):
    def __init__(self) -> None:
        super().__init__()
        self._transform = glm.mat4(1.0)
        #self.aabb = Rect2(0, 0, 0, 0)
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
        #self.aabb = self.get_world_aabb()
        #logger.debug(f"Vu2D: {self.aabb}")

    @property
    def size(self) -> glm.vec2:
        raise NotImplementedError

    def on_node_transform(self, node: Node2D) -> None:
        self.transform = node.transform
        #logger.debug(f"Vu2D: {self.transform}")
        self.bounds = node.bounds

    '''
    def get_local_aabb(self) -> Rect2:
        half_width = self.size.x / 2
        half_height = self.size.y / 2
        return Rect2(-half_width, -half_height, self.size.x, self.size.y)

    def get_world_aabb(self) -> Rect2:
        """Create the transformed Rect2 for the sprite."""
        # Get the local bounding box
        local_rect = self.get_local_aabb()
        logger.debug(f"local_rect: {local_rect}")

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
    '''