import glm

class Bounds3:
    #def __init__(self, min=glm.vec3(float('inf')), max=glm.vec3(float('-inf'))):
    def __init__(self, min=glm.vec3(), max=glm.vec3()):
        self.min = min
        self.max = max

    @property
    def size(self) -> glm.vec3:
        """Returns the size of the bounding box as a vec3 (width, height, depth)."""
        return self.max - self.min

    @property
    def center(self) -> glm.vec3:
        """Returns the center point of the bounding box."""
        return (self.min + self.max) * 0.5

    @property
    def max_extent(self) -> float:
        """Returns the maximum extent of the bounding box."""
        return max(self.size.x, self.size.y, self.size.z)

    def expand(self, point: glm.vec3) -> None:
        """Expands the bounding box to include the given point."""
        self.min = glm.vec3(min(self.min.x, point.x), min(self.min.y, point.y), min(self.min.z, point.z))
        self.max = glm.vec3(max(self.max.x, point.x), max(self.max.y, point.y), max(self.max.z, point.z))

    def merge(self, other: "Bounds3") -> None:
        """Expands the bounding box to include another bounding box."""
        self.expand(other.min)
        self.expand(other.max)

    def contains(self, point: glm.vec3) -> bool:
        """Checks if the bounding box contains a given point."""
        return (self.min.x <= point.x <= self.max.x and
                self.min.y <= point.y <= self.max.y and
                self.min.z <= point.z <= self.max.z)

    def intersects(self, other: "Bounds3") -> bool:
        """Checks if this bounding box intersects with another bounding box."""
        return (self.min.x <= other.max.x and self.max.x >= other.min.x and
                self.min.y <= other.max.y and self.max.y >= other.min.y and
                self.min.z <= other.max.z and self.max.z >= other.min.z)

    def is_valid(self) -> bool:
        """Checks if the bounding box is valid (min is less than or equal to max)."""
        return (self.min.x <= self.max.x and
                self.min.y <= self.max.y and
                self.min.z <= self.max.z)

    def reset(self) -> None:
        """Resets the bounding box to an invalid state."""
        self.min = glm.vec3(float('inf'))
        self.max = glm.vec3(float('-inf'))

    def to_global(self, transform: glm.mat4) -> 'Bounds3':
        """Transforms local bounds to a global (world-space) axis-aligned bounding box."""
        corners = [
            glm.vec3(self.min.x, self.min.y, self.min.z),
            glm.vec3(self.max.x, self.min.y, self.min.z),
            glm.vec3(self.min.x, self.max.y, self.min.z),
            glm.vec3(self.max.x, self.max.y, self.min.z),
            glm.vec3(self.min.x, self.min.y, self.max.z),
            glm.vec3(self.max.x, self.min.y, self.max.z),
            glm.vec3(self.min.x, self.max.y, self.max.z),
            glm.vec3(self.max.x, self.max.y, self.max.z),
        ]

        transformed_bounds = Bounds3()
        for corner in corners:
            world_corner = glm.vec3(transform * glm.vec4(corner, 1.0))
            transformed_bounds.expand(world_corner)

        return transformed_bounds

    def __repr__(self) -> str:
        return f"Bounds3(min={self.min}, max={self.max})"
