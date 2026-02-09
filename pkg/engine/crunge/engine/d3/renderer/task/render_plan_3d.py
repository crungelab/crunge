from typing import TYPE_CHECKING
from ....renderer.task.render_plan import RenderPlan

if TYPE_CHECKING:
    from ..scene_renderer_3d import SceneRenderer3D


class RenderPlan3D(RenderPlan["SceneRenderer3D"]):
    pass
