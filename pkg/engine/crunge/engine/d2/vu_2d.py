import glm
from loguru import logger

from crunge.engine import Vu
from crunge.engine.math.rect import RectF

class Vu2D(Vu):
    def __init__(self) -> None:
        super().__init__()
        self._transform = glm.mat4(1.0)
        self.aabb = RectF(0, 0, 0, 0)

    @property
    def transform(self):
        return self._transform
    
    @transform.setter
    def transform(self, value):
        self._transform = value
        self.on_transform()

    def on_transform(self):
        pass
        #self.aabb = self.get_world_aabb()
        #logger.debug(f"Vu2D: {self.aabb}")

    @property
    def size(self):
        raise NotImplementedError

    def get_local_aabb(self) -> RectF:
        half_width = self.size.x / 2
        half_height = self.size.y / 2
        return RectF(-half_width, -half_height, self.size.x, self.size.y)

    def get_world_aabb(self) -> RectF:
        """Create the transformed RectF for the sprite."""
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
        return RectF(min_x, min_y, max_x - min_x, max_y - min_y)
