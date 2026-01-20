
from typing import Generic, TypeVar

from .phase import RenderPhase, GroupPhase

T_Renderer = TypeVar("T_Renderer")


class RenderContext(Generic[T_Renderer]):
    def __init__(self, renderer: T_Renderer, root: GroupPhase[T_Renderer]) -> None:
        self.renderer = renderer
        self._stack: list[GroupPhase[T_Renderer]] = [root]

    def push_group(self, group: GroupPhase[T_Renderer]) -> None:
        self._stack.append(group)

    def pop_group(self) -> None:
        self._stack.pop()

    def current_group(self) -> GroupPhase[T_Renderer]:
        return self._stack[-1]

    def phase(self, phase_type: type[RenderPhase[T_Renderer]]) -> RenderPhase[T_Renderer]:
        return self._stack[-1].phase(phase_type)
