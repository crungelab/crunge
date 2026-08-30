from typing import TYPE_CHECKING, List, Tuple

from loguru import logger

from crunge import box2d
from crunge.engine.math import Rect2

if TYPE_CHECKING:
    from ..physics import Physics

from .poly_geom import PolyGeom, cross

SLOP = 0.01

MAX_POLY_VERTS = 8  # Box2D default: B2_MAX_POLYGON_VERTICES


def _convex_hull_monotonic_chain(
    points: List[Tuple[float, float]]
) -> List[Tuple[float, float]]:
    """CCW hull, without repeating the first point at the end."""
    pts = sorted(points)
    if len(pts) <= 1:
        return pts

    def build_half(pts_iter):
        half = []
        for x, y in pts_iter:
            while len(half) >= 2:
                x1, y1 = half[-2]
                x2, y2 = half[-1]
                if cross(x2 - x1, y2 - y1, x - x2, y - y2) <= 0.0:
                    half.pop()
                else:
                    break
            half.append((x, y))
        return half

    lower = build_half(pts)
    upper = build_half(reversed(pts))

    return lower[:-1] + upper[:-1]


def _tri_area2(a, b, c) -> float:
    """Twice the signed area magnitude of triangle abc."""
    return abs(cross(b[0] - a[0], b[1] - a[1], c[0] - a[0], c[1] - a[1]))


def _simplify_convex_polygon(
    points_ccw: List[Tuple[float, float]], max_verts: int
) -> List[Tuple[float, float]]:
    """Drop the lowest-area vertices until the polygon fits max_verts.

    Assumes CCW, convex input. Removing by local triangle area tends to
    preserve the corners that matter.
    """
    pts = points_ccw[:]
    if len(pts) <= max_verts:
        return pts

    while len(pts) > max_verts:
        n = len(pts)
        best_i = 0
        best_cost = float("inf")
        for i in range(n):
            prev = pts[(i - 1) % n]
            cur = pts[i]
            nxt = pts[(i + 1) % n]
            cost = _tri_area2(prev, cur, nxt)
            if cost < best_cost:
                best_cost = cost
                best_i = i
        pts.pop(best_i)

        if len(pts) < 3:
            break

    return pts


class HullGeom(PolyGeom):
    """Single convex hull enclosing the model's outline."""

    def create_shapes(
        self,
        chip: "Physics",
        transform: box2d.Transform = None,
        clip: Rect2 = None,
    ) -> list:
        node = chip.node
        points = self.get_points(chip, clip)

        if len(points) < 3:
            logger.warning(f"{node}: fewer than 3 usable points; no shape built")
            return []

        # Hull computed here rather than leaning on Box2D, so the vertex
        # count is capped before b2ComputeHull sees it.
        hull2d = _convex_hull_monotonic_chain(points)
        if len(hull2d) < 3:
            logger.warning(f"{node}: degenerate hull; no shape built")
            return []

        if len(hull2d) > MAX_POLY_VERTS:
            hull2d = _simplify_convex_polygon(hull2d, MAX_POLY_VERTS)

        if len(hull2d) < 3:
            logger.warning(f"{node}: hull collapsed during simplify; no shape built")
            return []

        hull_points = [box2d.Vec2(x, y) for (x, y) in hull2d]
        shape_hull = box2d.compute_hull(hull_points)

        count = getattr(shape_hull, "count", 0)
        if count > MAX_POLY_VERTS:
            raise ValueError(f"Box2D hull has {count} verts; max is {MAX_POLY_VERTS}")

        polygon = box2d.make_polygon(shape_hull, SLOP)

        shape_def = self.make_shape_def(chip)
        shape = chip.body.create_polygon_shape(shape_def, polygon)
        shape.user_data = node

        return [shape]