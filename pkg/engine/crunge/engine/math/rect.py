import glm

class RectI:
    def __init__(self, x: int = 0, y: int = 0, width: int = 0, height: int = 0):
        self.position = glm.ivec2(x, y)
        self.size = glm.ivec2(width, height)

    @property
    def x(self) -> int:
        return self.position.x

    @property
    def y(self) -> int:
        return self.position.y

    @property
    def width(self) -> int:
        return self.size.x

    @property
    def height(self) -> int:
        return self.size.y

    def get_center(self) -> glm.ivec2:
        return self.position + self.size // 2

    def get_area(self) -> int:
        return self.width * self.height

    def contains_point(self, point: glm.ivec2) -> bool:
        return (self.x <= point.x < self.x + self.width and
                self.y <= point.y < self.y + self.height)

    def intersects(self, other: 'RectI') -> bool:
        return not (self.x + self.width <= other.x or
                    other.x + other.width <= self.x or
                    self.y + self.height <= other.y or
                    other.y + other.height <= self.y)

    def union(self, other: 'RectI') -> 'RectI':
        x = min(self.x, other.x)
        y = min(self.y, other.y)
        width = max(self.x + self.width, other.x + other.width) - x
        height = max(self.y + self.height, other.y + other.height) - y
        return RectI(x, y, width, height)

    def __repr__(self) -> str:
        return f"RectI(x={self.x}, y={self.y}, width={self.width}, height={self.height})"

class RectF:
    def __init__(self, x: float = 0.0, y: float = 0.0, width: float = 0.0, height: float = 0.0):
        self.position = glm.vec2(x, y)
        self.size = glm.vec2(width, height)

    @property
    def x(self) -> float:
        return self.position.x

    @property
    def y(self) -> float:
        return self.position.y

    @property
    def width(self) -> float:
        return self.size.x

    @property
    def height(self) -> float:
        return self.size.y

    def get_center(self) -> glm.vec2:
        return self.position + self.size * 0.5

    def get_area(self) -> float:
        return self.width * self.height

    def contains_point(self, point: glm.vec2) -> bool:
        return (self.x <= point.x < self.x + self.width and
                self.y <= point.y < self.y + self.height)

    def contains_rect(self, other: 'RectF') -> bool:
        """Check if the rectangle completely contains another rectangle."""
        return (self.x <= other.x and
                self.x + self.width >= other.x + other.width and
                self.y <= other.y and
                self.y + self.height >= other.y + other.height)

    def intersects(self, other: 'RectF') -> bool:
        return not (self.x + self.width <= other.x or
                    other.x + other.width <= self.x or
                    self.y + self.height <= other.y or
                    other.y + other.height <= self.y)

    def union(self, other: 'RectF') -> 'RectF':
        x = min(self.x, other.x)
        y = min(self.y, other.y)
        width = max(self.x + self.width, other.x + other.width) - x
        height = max(self.y + self.height, other.y + other.height) - y
        return RectF(x, y, width, height)

    def scale(self, factor: float) -> 'RectF':
        return RectF(self.x, self.y, self.width * factor, self.height * factor)

    def __repr__(self) -> str:
        return f"RectF(x={self.x:.2f}, y={self.y:.2f}, width={self.width:.2f}, height={self.height:.2f})"