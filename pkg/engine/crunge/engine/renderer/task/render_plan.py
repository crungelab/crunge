from typing import Generic

from .render_task import RenderTask, T_Renderer
from .render_phase import RenderPhase


class RenderPlan(Generic[T_Renderer], RenderTask[T_Renderer]):
    def __init__(
        self, renderer: T_Renderer, children: list[RenderTask[T_Renderer]] = None
    ) -> None:
        super().__init__(renderer)
        self.renderer = renderer
        self.children: list[RenderTask[T_Renderer]] = []
        self.phases: dict[type[RenderPhase[T_Renderer]], RenderPhase[T_Renderer]] = {}

        for child in children:
            self.add_child(child)

    def add_child(self, child: RenderTask[T_Renderer]) -> None:
        self.children.append(child)
        if isinstance(child, RenderPhase):
            self.phases[type(child)] = child

    def get_phase(
        self, child_type: type[RenderPhase[T_Renderer]]
    ) -> RenderPhase[T_Renderer]:
        return self.phases.get(child_type)

    def clear(self) -> None:
        for child in self.children:
            child.clear()

    def render(self) -> None:
        # Execution policy belongs here: fixed order, conditional, etc.
        for child in self.children:
            child.render()
