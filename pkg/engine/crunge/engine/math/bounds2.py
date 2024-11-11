from loguru import logger
import glm

class Bounds2:
    #def __init__(self, min=glm.vec3(float('inf')), max=glm.vec3(float('-inf'))):
    #def __init__(self, min=glm.vec2(), max=glm.vec2()):
    def __init__(self, left: float = 0.0, bottom: float = 0.0, right: float = 0.0, top: float = 0.0):
        #self.min = min
        self.min = glm.vec2(left, bottom)
        #self.max = max
        self.max = glm.vec2(right, top)

    @property
    def left(self) -> float:
        """Returns the left edge of the bounding box."""
        return self.min.x
    
    @property
    def bottom(self) -> float:
        """Returns the bottom edge of the bounding box."""
        return self.min.y
    
    @property
    def right(self) -> float:
        """Returns the right edge of the bounding box."""
        return self.max.x
    
    @property
    def top(self) -> float:
        """Returns the top edge of the bounding box."""
        return self.max.y
    
    @property
    def size(self) -> glm.vec2:
        """Returns the size of the bounding box as a vec2 (width, height)."""
        return self.max - self.min

    @property
    def width(self) -> float:
        """Returns the width of the bounding box."""
        return self.size.x
    
    @property
    def height(self) -> float:
        """Returns the height of the bounding box."""
        return self.size.y

    @property
    def center(self) -> glm.vec2:
        """Returns the center point of the bounding box."""
        return (self.min + self.max) * 0.5

    def expand(self, point: glm.vec2) -> None:
        """Expands the bounding box to include the given point."""
        self.min = glm.vec2(min(self.min.x, point.x), min(self.min.y, point.y))
        self.max = glm.vec2(max(self.max.x, point.x), max(self.max.y, point.y))

    def merge(self, other: "Bounds2") -> None:
        """Expands the bounding box to include another bounding box."""
        self.expand(other.min)
        self.expand(other.max)

    def contains(self, point: glm.vec2) -> bool:
        """Checks if the bounding box contains a given point."""
        return (self.min.x <= point.x <= self.max.x and
                self.min.y <= point.y <= self.max.y)

    def intersects(self, other: "Bounds2") -> bool:
        """Checks if this bounding box intersects with another bounding box."""
        return (self.min.x <= other.max.x and self.max.x >= other.min.x and
                self.min.y <= other.max.y and self.max.y >= other.min.y)

    def is_valid(self) -> bool:
        """Checks if the bounding box is valid (min is less than or equal to max)."""
        return (self.min.x <= self.max.x and
                self.min.y <= self.max.y)

    def reset(self) -> None:
        """Resets the bounding box to an invalid state."""
        #self.min = glm.vec2(float('inf'))
        self.min = glm.vec2()
        #self.max = glm.vec2(float('-inf'))
        self.max = glm.vec2()

    '''
    def to_global(self, transform: glm.mat4) -> 'Bounds2':
        min = transform * glm.vec4(self.min, 0.0, 1.0)
        logger.debug(f"class: {self.__class__}, min: {min}")
        max = transform * glm.vec4(self.max, 0.0, 1.0)
        logger.debug(f"class: {self.__class__}, max: {max}")
        return Bounds2(min.x, min.y, max.x, max.y)

    '''
    def to_global(self, transform: glm.mat4) -> 'Bounds2':
        """Transforms local bounds to a global (world-space) axis-aligned bounding box."""
        # Define the corners of the bounding box in local space
        corners = [
            glm.vec2(self.min.x, self.min.y),
            glm.vec2(self.max.x, self.min.y),
            glm.vec2(self.min.x, self.max.y),
            glm.vec2(self.max.x, self.max.y)
        ]

        # Initialize transformed bounds with an invalid state to expand with transformed corners
        transformed_bounds = Bounds2()
        
        # Transform each corner and expand the bounds to include it
        for corner in corners:
            #world_corner = glm.vec2(transform * glm.vec4(corner, 0.0, 1.0))
            world_corner = transform * glm.vec4(corner, 0.0, 1.0)
            world_corner = glm.vec2(world_corner.x, world_corner.y)
            transformed_bounds.expand(world_corner)
        
        return transformed_bounds

    def __repr__(self) -> str:
        return f"Bounds2(min={self.min}, max={self.max})"
