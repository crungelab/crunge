from loguru import logger

from . import GraphLayer2D
from ....render_group import RenderGroup

class RenderLayer2D(GraphLayer2D):
    """
    A layer that draws its vus through a RenderGroup.
    """

    def __init__(self, name: str = "RenderLayer2D", is_managed: bool = False) -> None:
        super().__init__(name)
        # Mounted on the root, so the chip walk drives create, enable,
        # update, draw and destroy. The RenderGroup is now the only chip in
        # the arrangement; VuGroups are plain objects it owns, which is what
        # keeps them from being updated and drawn twice.
        self.root_render_group = self.root.add(RenderGroup(is_managed=is_managed))
        self.register_vu_groups()

    def register_vu_groups(self) -> None:
        """Subclasses register their group factories here."""

    def find_render_group(self) -> RenderGroup:
        return self.root_render_group

    def append(self, vu) -> None:
        self.root_render_group.append(vu)

    def clear(self) -> None:
        self.root_render_group.clear()
