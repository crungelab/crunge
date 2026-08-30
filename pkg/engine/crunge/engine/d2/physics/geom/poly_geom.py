from typing import TYPE_CHECKING, List, Tuple

import math

from loguru import logger
import glm

from crunge import box2d
from crunge.engine.math import Rect2

if TYPE_CHECKING:
    from ..physics import Physics

from .geom import Geom


class PolyGeom(Geom):
    """Base for geoms built from the model's outline points."""

    def get_points(self, chip, dedupe_eps: float = 1e-5):
        node = chip.node

        if node.model is None or node.model.points is None:
            raise ValueError(f"model: {node.model}: no points")

        sx, sy = node.scale.x, node.scale.y
        points = []
        for p in node.model.points:
            x = float(p[0]) * sx
            y = float(p[1]) * sy
            if math.isfinite(x) and math.isfinite(y):
                points.append((x, y))

        if self.clip is not None:
            rect = self.resolve_clip(points)
            points = [
                (x, y) for (x, y) in points
                if rect.contains_point(glm.vec2(x, y))
            ]

        if self.offset != glm.vec2():
            ox, oy = self.offset.x, self.offset.y
            points = [(x + ox, y + oy) for (x, y) in points]

        return dedupe(points, dedupe_eps) if dedupe_eps else points

    def resolve_clip(self, points) -> Rect2:
        """Normalized clip -> a rect in the points' own space."""
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        x0, x1 = min(xs), max(xs)
        y0, y1 = min(ys), max(ys)
        w, h = x1 - x0, y1 - y0
        clip = self.clip
        return Rect2(
            x0 + clip.x * w, y0 + clip.y * h, clip.width * w, clip.height * h
        )

def dedupe(
    points: List[Tuple[float, float]], eps: float = 1e-5
) -> List[Tuple[float, float]]:
    """Quantize to an epsilon grid so noisy clipped points collapse."""
    seen = set()
    out = []
    inv = 1.0 / eps
    for x, y in points:
        key = (int(round(x * inv)), int(round(y * inv)))
        if key not in seen:
            seen.add(key)
            out.append((x, y))
    return out


def cross(ax: float, ay: float, bx: float, by: float) -> float:
    return ax * by - ay * bx