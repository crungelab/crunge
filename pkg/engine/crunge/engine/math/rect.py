from . import Point2, Size2, Point2i, Size2i


class Rect2i:
    def __init__(self, x: int = 0, y: int = 0, width: int = 0, height: int = 0):
        self.position = Point2i(x, y)
        self.size = Size2i(width, height)

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

    def get_center(self) -> Point2i:
        return self.position + self.size // 2

    def get_area(self) -> int:
        return self.width * self.height

    def contains_point(self, point: Point2i) -> bool:
        return (self.x <= point.x < self.x + self.width and
                self.y <= point.y < self.y + self.height)

    def intersects(self, other: 'Rect2i') -> bool:
        return not (self.x + self.width <= other.x or
                    other.x + other.width <= self.x or
                    self.y + self.height <= other.y or
                    other.y + other.height <= self.y)

    def union(self, other: 'Rect2i') -> 'Rect2i':
        x = min(self.x, other.x)
        y = min(self.y, other.y)
        width = max(self.x + self.width, other.x + other.width) - x
        height = max(self.y + self.height, other.y + other.height) - y
        return Rect2i(x, y, width, height)

    def __repr__(self) -> str:
        return f"Rect2i(x={self.x}, y={self.y}, width={self.width}, height={self.height})"

class Rect2:
    def __init__(self, x: float = 0.0, y: float = 0.0, width: float = 0.0, height: float = 0.0):
        self.position = Point2(x, y)
        self.size = Size2(width, height)

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

    def get_center(self) -> Point2:
        return self.position + self.size * 0.5

    def get_area(self) -> float:
        return self.width * self.height

    def contains_point(self, point: Point2) -> bool:
        return (self.x <= point.x < self.x + self.width and
                self.y <= point.y < self.y + self.height)

    def contains_rect(self, other: 'Rect2') -> bool:
        """Check if the rectangle completely contains another rectangle."""
        return (self.x <= other.x and
                self.x + self.width >= other.x + other.width and
                self.y <= other.y and
                self.y + self.height >= other.y + other.height)

    def intersects(self, other: 'Rect2') -> bool:
        return not (self.x + self.width <= other.x or
                    other.x + other.width <= self.x or
                    self.y + self.height <= other.y or
                    other.y + other.height <= self.y)

    def union(self, other: 'Rect2') -> 'Rect2':
        x = min(self.x, other.x)
        y = min(self.y, other.y)
        width = max(self.x + self.width, other.x + other.width) - x
        height = max(self.y + self.height, other.y + other.height) - y
        return Rect2(x, y, width, height)

    def scale(self, factor: float) -> 'Rect2':
        return Rect2(self.x, self.y, self.width * factor, self.height * factor)

    def __repr__(self) -> str:
        return f"Rect2(x={self.x:.2f}, y={self.y:.2f}, width={self.width:.2f}, height={self.height:.2f})"