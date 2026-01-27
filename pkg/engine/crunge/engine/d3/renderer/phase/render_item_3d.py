from typing import TYPE_CHECKING, Callable
from dataclasses import dataclass

from ...node_3d import Node3D
from ...vu_3d import Vu3D

if TYPE_CHECKING:
    from ..renderer_3d import Renderer3D

DrawCallback3D = Callable[["Renderer3D"], None]


@dataclass(slots=True)
class Transmissive3D:
    vu: Vu3D
    callback: DrawCallback3D
    node: "Node3D" = None

    def __post_init__(self):
        self.node = self.vu.node