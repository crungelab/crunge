
from typing import Generic

from .render_phase import RenderPhase, T_Renderer


class GroupPhase(Generic[T_Renderer], RenderPhase[T_Renderer]):
    def __init__(self, renderer: T_Renderer) -> None:
        super().__init__(renderer)
        self.renderer = renderer
        self.children: list[RenderPhase[T_Renderer]] = []

    def add_child(self, child: RenderPhase[T_Renderer]) -> None:
        self.children.append(child)

    def clear(self) -> None:
        for child in self.children:
            child.clear()

    def render(self) -> None:
        # Execution policy belongs here: fixed order, conditional, etc.
        for child in self.children:
            child.render()
