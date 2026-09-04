import math

from loguru import logger
import glm


class Bounds2:
    def __init__(
        self,
        left: float = 0.0,
        bottom: float = 0.0,
        right: float = 0.0,
        top: float = 0.0,
    ):
        self.min = glm.vec2(left, bottom)
        self.max = glm.vec2(right, top)

    @classmethod
    def empty(cls) -> "Bounds2":
        """An inverted-infinite box, for accumulating with expand()/merge().

        A zeroed box is not empty — it is a valid degenerate box at the
        origin, so accumulating into one drags the result back to (0, 0).
        Start from this instead.
        """
        inf = float("inf")
        return cls(inf, inf, -inf, -inf)

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

    @property
    def corners(self) -> "list[glm.vec2]":
        """Corners in winding order, starting bottom-left."""
        return [
            glm.vec2(self.min.x, self.min.y),
            glm.vec2(self.max.x, self.min.y),
            glm.vec2(self.max.x, self.max.y),
            glm.vec2(self.min.x, self.max.y),
        ]

    def expand(self, point: glm.vec2) -> None:
        """Expands the bounding box to include the given point."""
        self.min = glm.vec2(min(self.min.x, point.x), min(self.min.y, point.y))
        self.max = glm.vec2(max(self.max.x, point.x), max(self.max.y, point.y))

    def merge(self, other: "Bounds2") -> None:
        """Expands the bounding box to include another bounding box.

        An empty `other` is skipped: its infinities would poison this box.
        """
        if not other.is_valid():
            return
        self.expand(other.min)
        self.expand(other.max)

    def contains(self, point: glm.vec2) -> bool:
        """Checks if the bounding box contains a given point."""
        return (
            self.min.x <= point.x <= self.max.x and self.min.y <= point.y <= self.max.y
        )

    def intersects(self, other: "Bounds2") -> bool:
        """Checks if this bounding box intersects with another bounding box."""
        return (
            self.min.x <= other.max.x
            and self.max.x >= other.min.x
            and self.min.y <= other.max.y
            and self.max.y >= other.min.y
        )

    def is_valid(self) -> bool:
        """Checks if the bounding box is valid (min is less than or equal to max).

        An empty box (from Bounds2.empty() or reset()) is not valid — that is
        the point of the sentinel. A zeroed box still reports valid, since a
        degenerate point box at the origin is a legitimate result.
        """
        return self.min.x <= self.max.x and self.min.y <= self.max.y

    def is_finite(self) -> bool:
        """True when every component is a real number.

        A transform containing NaN, or a to_global() on an empty box, yields
        corners that pass is_valid() by accident (comparisons against NaN are
        all False, so the <= test can fall through). Use this when the box is
        about to be handed to something that will divide by its size.
        """
        return all(
            math.isfinite(v)
            for v in (self.min.x, self.min.y, self.max.x, self.max.y)
        )

    def reset(self) -> None:
        """Resets the bounding box to an empty (accumulation-ready) state."""
        inf = float("inf")
        self.min = glm.vec2(inf, inf)
        self.max = glm.vec2(-inf, -inf)

    def to_global(self, transform: glm.mat4) -> "Bounds2":
        """Axis-aligned box enclosing this box after `transform`.

        Note this is the AABB of the transformed corners, not the transformed
        box: under rotation the result is larger than the source, by
        |cos t| + |sin t|. That is what broadphase and intersects() want. If
        you need a box that hugs a rotated node — for debug drawing, say —
        transform `corners` yourself and draw the polygon.
        """
        p1 = transform * glm.vec4(self.min.x, self.min.y, 0.0, 1.0)
        p2 = transform * glm.vec4(self.max.x, self.min.y, 0.0, 1.0)
        p3 = transform * glm.vec4(self.min.x, self.max.y, 0.0, 1.0)
        p4 = transform * glm.vec4(self.max.x, self.max.y, 0.0, 1.0)
        xs = [p.x for p in [p1, p2, p3, p4]]
        ys = [p.y for p in [p1, p2, p3, p4]]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        return Bounds2(min_x, min_y, max_x, max_y)

    def __repr__(self) -> str:
        return f"Bounds2(min={self.min}, max={self.max})"