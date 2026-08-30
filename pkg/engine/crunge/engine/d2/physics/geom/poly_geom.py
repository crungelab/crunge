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

    def get_points(
        self,
        chip: "Physics",
        clip: Rect2 = None,
        dedupe_eps: float = 1e-5,
    ) -> List[Tuple[float, float]]:
        """Model points, scaled to node space, optionally clipped, sanitized."""
        node = chip.node

        if node.model is None or node.model.points is None:
            raise ValueError(f"model: {node.model}: no points")

        sx, sy = node.scale.x, node.scale.y
        rect = self.resolve_clip(chip, clip)

        points = []
        for p in node.model.points:
            x = float(p[0]) * sx
            y = float(p[1]) * sy
            if not (math.isfinite(x) and math.isfinite(y)):
                continue
            if rect is not None and not rect.contains_point(glm.vec2(x, y)):
                continue
            points.append((x, y))

        return dedupe(points, dedupe_eps) if dedupe_eps else points


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