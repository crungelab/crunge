from typing import TYPE_CHECKING, Generic
from ....renderer.phase.item_phase import ItemPhase, T_PhaseItem

if TYPE_CHECKING:
    from .. import SceneRenderer2D


class ItemPhase2D(Generic[T_PhaseItem], ItemPhase["SceneRenderer2D", T_PhaseItem]):
    pass
