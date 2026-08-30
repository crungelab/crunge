from typing import Any, Generic, TypeVar

import glm

from ..node_group import NodeGroup
from .node_2d import Node2D

T_Node = TypeVar("T_Node", bound=Node2D)


class NodeGroup2D(NodeGroup[T_Node], Generic[T_Node]):
    def update(self, delta_time: float) -> None:
        if not self.members:
            return
        total = glm.vec2()
        for node in self.members:
            total += node.position
        self.node.position = total / len(self.members)