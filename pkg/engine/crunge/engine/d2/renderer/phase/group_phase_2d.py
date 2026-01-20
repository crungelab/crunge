from typing import TYPE_CHECKING
from ....renderer.phase.group_phase import GroupPhase

if TYPE_CHECKING:
    from ..scene_renderer_2d import SceneRenderer2D

    
class GroupPhase2D(GroupPhase["SceneRenderer2D"]):
    pass
