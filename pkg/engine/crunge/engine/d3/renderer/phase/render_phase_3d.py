from typing import TYPE_CHECKING
from ....renderer.phase.render_phase import RenderPhase

if TYPE_CHECKING:
    from ..scene_renderer_3d import SceneRenderer3D


class RenderPhase3D(RenderPhase["SceneRenderer3D"]):
    pass
