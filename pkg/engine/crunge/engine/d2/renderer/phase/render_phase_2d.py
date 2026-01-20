from typing import TYPE_CHECKING
from ....renderer.phase import RenderPhase

if TYPE_CHECKING:
    from .. import SceneRenderer2D


class RenderPhase2D(RenderPhase["SceneRenderer2D"]):
    pass
