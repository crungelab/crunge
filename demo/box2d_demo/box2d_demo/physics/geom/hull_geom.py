from typing import TYPE_CHECKING

from loguru import logger

import glm

from crunge import box2d
from crunge.engine.math import Rect2

if TYPE_CHECKING:
    from box2d_demo.entity import PhysicsEntity2D

from .poly_geom import PolyGeom

SLOP = 0.01

import math
from typing import List, Tuple

MAX_POLY_VERTS = 8  # Box2D default: B2_MAX_POLYGON_VERTICES


def _is_finite_xy(x: float, y: float) -> bool:
    return math.isfinite(x) and math.isfinite(y)


def _dedupe(points: List[Tuple[float, float]], eps: float = 1e-5) -> List[Tuple[float, float]]:
    # Quantize to an epsilon grid so we can dedupe noisy clipped points
    q = set()
    out = []
    inv = 1.0 / eps
    for x, y in points:
        k = (int(round(x * inv)), int(round(y * inv)))
        if k not in q:
            q.add(k)
            out.append((x, y))
    return out


def _cross(ax: float, ay: float, bx: float, by: float) -> float:
    return ax * by - ay * bx


def _convex_hull_monotonic_chain(points: List[Tuple[float, float]]) -> List[Tuple[float, float]]:
    # Returns CCW hull without repeating the first point at the end.
    pts = sorted(points)
    if len(pts) <= 1:
        return pts

    def build_half(pts_iter):
        half = []
        for x, y in pts_iter:
            while len(half) >= 2:
                x1, y1 = half[-2]
                x2, y2 = half[-1]
                if _cross(x2 - x1, y2 - y1, x - x2, y - y2) <= 0.0:
                    half.pop()
                else:
                    break
            half.append((x, y))
        return half

    lower = build_half(pts)
    upper = build_half(reversed(pts))

    hull = lower[:-1] + upper[:-1]
    return hull


def _tri_area2(a, b, c) -> float:
    # twice signed area magnitude of triangle abc
    return abs(_cross(b[0] - a[0], b[1] - a[1], c[0] - a[0], c[1] - a[1]))


def _simplify_convex_polygon(points_ccw: List[Tuple[float, float]], max_verts: int) -> List[Tuple[float, float]]:
    # Assumes points are in CCW order and form a convex polygon.
    pts = points_ccw[:]
    if len(pts) <= max_verts:
        return pts

    # Iteratively remove the vertex with the smallest local triangle area (prev, cur, next).
    # This tends to preserve "important" corners.
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

        # If we collapsed into something degenerate, bail early.
        if len(pts) < 3:
            break

    return pts


class HullGeom(PolyGeom):
    def __init__(self):
        super().__init__()

    def create_shapes(self, node: "PhysicsEntity2D", transform=None, clip: "Rect2" = None):
        body = node.body
        shapes = []

        if node.model.points is None:
            raise ValueError(f"model: {node.model}: no points")

        raw = node.model.points.tolist()

        # 1) Clip
        clipped = []
        if clip:
            for p in raw:
                x = float(p[0])
                y = float(p[1])
                if clip.contains_point(glm.vec2(x, y)):
                    clipped.append((x, y))
        else:
            clipped = [(float(p[0]), float(p[1])) for p in raw]

        # 2) Sanitize
        clipped = [(x, y) for (x, y) in clipped if _is_finite_xy(x, y)]
        clipped = _dedupe(clipped, eps=1e-5)

        if len(clipped) < 3:
            # Nothing meaningful to build.
            return shapes

        # 3) Compute convex hull in Python (prevents Box2D from returning hull > 8)
        hull2d = _convex_hull_monotonic_chain(clipped)
        if len(hull2d) < 3:
            return shapes

        # 4) Simplify to Box2D max vertices if needed
        if len(hull2d) > MAX_POLY_VERTS:
            hull2d = _simplify_convex_polygon(hull2d, MAX_POLY_VERTS)

        if len(hull2d) < 3:
            return shapes

        # 5) Hand to Box2D
        hull_points = [box2d.Vec2(x, y) for (x, y) in hull2d]

        shape_hull = box2d.compute_hull(hull_points)

        # Defensive: if binding exposes count and it’s still > 8, hard-fail early.
        if getattr(shape_hull, "count", 0) > MAX_POLY_VERTS:
            raise ValueError(f"Box2D hull has {shape_hull.count} verts; max is {MAX_POLY_VERTS}")

        polygon = box2d.make_polygon(shape_hull, SLOP)

        shape_def = box2d.ShapeDef()
        shape = body.create_polygon_shape(shape_def, polygon)

        shapes.append(shape)
        return shapes