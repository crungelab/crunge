from typing import TYPE_CHECKING

from crunge import box2d
from crunge.engine.math import Rect2

if TYPE_CHECKING:
    from ..physics import Physics


class Geom:
    """Builds Box2D shapes for a Physics chip's body."""

    def __init__(self, clip: Rect2 = None):
        # Normalized: fractions of node size, origin at node origin.
        self.clip = clip

    def create_shapes(
        self,
        chip: "Physics",
        transform: box2d.Transform = None,
        clip: Rect2 = None,
    ) -> list:
        raise NotImplementedError


    def make_shape_def(self, chip: "Physics") -> box2d.ShapeDef:
        shape_def = box2d.ShapeDef()
        shape_def.enable_contact_events = True
        if chip.material is not None:
            chip.material.apply(shape_def)
        #chip.material.apply(shape_def)
        self.configure_shape_def(chip, shape_def)
        return shape_def

    def configure_shape_def(self, chip: "Physics", shape_def: box2d.ShapeDef) -> None:
        pass

    def resolve_clip(self, chip: "Physics", clip: Rect2 = None) -> Rect2 | None:
        """Normalized clip -> node-space rect."""
        clip = self.clip if clip is None else clip
        if clip is None:
            return None
        node = chip.node
        w, h = node.width, node.height
        return Rect2(clip.x * w, clip.y * h, clip.width * w, clip.height * h)