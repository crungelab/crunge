from typing import TYPE_CHECKING, ClassVar, Type, Dict, List, Any, Callable

from loguru import logger

import glm

from crunge.engine.d2.node_2d import Node2D

if TYPE_CHECKING:
    from ..physics import Physics


class Entity2D(Node2D):
    geom = None
    material = None

    physics_class: ClassVar["type[Physics] | None"] = None

    def __init__(
        self, position=glm.vec2(), rotation=0.0, scale=glm.vec2(1.0), model=None
    ):
        super().__init__(position, rotation, scale, model=model)
        # logger.debug(f"Entity2D: {self}")

    def _seat(self) -> None:
        super()._seat()
        if self.physics_class is not None:
            self.physics = self.add(
                self.physics_class(geom=self.geom, material=self.material)
            )
