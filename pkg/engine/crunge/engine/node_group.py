from typing import Any, Generic, TypeVar


from .chip import Chip
from .group import Group
from .node import Node
T_Node = TypeVar("T_Node", bound=Node)


class NodeGroup(Chip[Any], Group[T_Node], Generic[T_Node]):
    pass
