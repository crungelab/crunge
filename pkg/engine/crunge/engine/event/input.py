from dataclasses import dataclass, field

import glm


@dataclass(slots=True)
class Input:
    """Engine-side wrapper around an SDL event. `native` keeps everything SDL
    gave us, so nothing has to be modelled before it's needed."""

    event: object


@dataclass(slots=True)
class PointerInput(Input):
    """`point` is in the space of whoever is dispatching: world units at the
    layer, logical widget pixels inside a WidgetControl2D. Each level that
    changes space makes a new wrapper around the same native event.

    native.x / native.y are always window pixels and stay that way.
    """

    point: glm.vec2 = field(default_factory=glm.vec2)

    def moved_to(self, point: glm.vec2) -> "PointerInput":
        return PointerInput(self.event, glm.vec2(point))