from typing import Generic

from .render_task import RenderTask
from .render_phase import RenderPhase


class RenderPlan(RenderTask):
    def __init__(
        self, children: list[RenderTask] = None
    ) -> None:
        super().__init__()
        self.children: list[RenderTask] = []
        self.phases: dict[type[RenderPhase], RenderPhase] = {}

        for child in children:
            self.add_child(child)

    def add_child(self, child: RenderTask) -> None:
        self.children.append(child)
        if isinstance(child, RenderPhase):
            self.phases[type(child)] = child

    def get_phase(
        self, child_type: type[RenderPhase]
    ) -> RenderPhase:
        return self.phases.get(child_type)

    def clear(self) -> None:
        for child in self.children:
            child.clear()

    def render(self) -> None:
        for child in self.children:
            child.render()
