from typing import TYPE_CHECKING
from ....renderer.phase.render_plan import RenderPlan

if TYPE_CHECKING:
    from ..scene_renderer_2d import SceneRenderer2D

    
class RenderPlan2D(RenderPlan["SceneRenderer2D"]):
    pass
