from typing import TYPE_CHECKING, Generic

from ....renderer.phase.item_phase import ItemPhase, T_PhaseItem

if TYPE_CHECKING:
    from ..scene_renderer_3d import SceneRenderer3D


class ItemPhase3D(Generic[T_PhaseItem], ItemPhase["SceneRenderer3D", T_PhaseItem]):
    pass
