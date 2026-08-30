from typing import TYPE_CHECKING

from loguru import logger
import glm

from crunge import box2d
from crunge.engine.math import Rect2

if TYPE_CHECKING:
    from ..physics import Physics

from .poly_geom import PolyGeom


class ChainGeom(PolyGeom):
    """A chain (edge loop) from the model's outline. Static geometry only —
    chains have no interior, so a dynamic body won't collide correctly."""

    def __init__(self, is_loop: bool = True, clip: Rect2 = None):
        super().__init__(clip)
        self.is_loop = is_loop

    def create_shapes(self, chip: "Physics") -> list:
        points = self.get_points(chip)
        points = _dedupe_closing_point(points, self.is_loop)

        if len(points) < (3 if self.is_loop else 2):
            logger.warning(f"{chip.node}: too few points for a chain; none built")
            return []

        chain_def = box2d.ChainDef(is_loop=self.is_loop)
        chain_def.enable_sensor_events = False

        material = self.material if self.material is not None else chip.material
        materials = [material.make_surface_material()] if material else [
            box2d.SurfaceMaterial()
        ]

        chain = chip.body.create_chain_from_points(
            chain_def,
            [box2d.Vec2(x, y) for (x, y) in points],
            materials,
        )
        return [chain]

    """
    def create_shapes(
        self,
        chip: "Physics",
        transform: box2d.Transform = None,
        clip: Rect2 = None,
    ) -> list:
        node = chip.node

        if node.model is None or node.model.points is None:
            raise ValueError(f"model: {node.model}: no points")

        sx, sy = node.scale.x, node.scale.y
        raw = node.model.points

        points = [(float(p[0]) * sx, float(p[1]) * sy) for p in raw]
        points = _dedupe_closing_point(points, self.is_loop)

        if len(points) < (3 if self.is_loop else 2):
            logger.warning(f"{node}: too few points for a chain; none built")
            return []

        chain_points = [box2d.Vec2(x, y) for (x, y) in points]
        logger.debug(f"ChainGeom {node} points={len(chain_points)} loop={self.is_loop}")

        chain_def = box2d.ChainDef(is_loop=self.is_loop)
        if chip.material is not None:
            chip.material.apply(chain_def)
        #chip.material.apply_chain(chain_def)
        chain_def.enable_sensor_events = False

        chain = chip.body.create_chain_from_points(chain_def, chain_points)
        return [chain]
    """

def _dedupe_closing_point(points, is_loop):
    """Box2D closes loops itself; a repeated final point makes a zero-length
    segment and a degenerate normal."""
    if is_loop and len(points) >= 2:
        first, last = points[0], points[-1]
        if abs(first[0] - last[0]) < 1e-6 and abs(first[1] - last[1]) < 1e-6:
            return points[:-1]
    return points