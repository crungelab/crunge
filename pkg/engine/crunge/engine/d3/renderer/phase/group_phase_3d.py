from typing import TYPE_CHECKING
from ....renderer.phase.group_phase import GroupPhase

if TYPE_CHECKING:
    from ..scene_renderer_3d import SceneRenderer3D


class GroupPhase3D(GroupPhase["SceneRenderer3D"]):
    pass
