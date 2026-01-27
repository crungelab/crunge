
from typing import Generic

from .render_phase import RenderPhase, T_Renderer


class RenderPlan(Generic[T_Renderer], RenderPhase[T_Renderer]):
    def __init__(self, renderer: T_Renderer, children: list[RenderPhase[T_Renderer]] = None) -> None:
        super().__init__(renderer)
        self.renderer = renderer
        self.children: list[RenderPhase[T_Renderer]] = children if children is not None else []
        self._by_type: dict[type[RenderPhase[T_Renderer]], RenderPhase[T_Renderer]] = {}

    def add_child(self, child: RenderPhase[T_Renderer]) -> None:
        self.children.append(child)
        self._by_type[type(child)] = child

    
    def phase(self, child_type: type[RenderPhase[T_Renderer]]) -> RenderPhase[T_Renderer]:
        return self._by_type.get(child_type)

    def clear(self) -> None:
        for child in self.children:
            child.clear()

    def render(self) -> None:
        # Execution policy belongs here: fixed order, conditional, etc.
        for child in self.children:
            child.render()
