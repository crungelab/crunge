from typing import TYPE_CHECKING
from ....renderer.phase import RenderPhase

if TYPE_CHECKING:
    from .. import SceneRenderer3D


class RenderPhase3D(RenderPhase["SceneRenderer3D"]):
    pass
