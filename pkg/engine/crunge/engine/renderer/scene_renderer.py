from typing import TYPE_CHECKING, Generic, TypeVar

from .renderer import Renderer
from .phase import RenderPhase
from ..viewport import Viewport

if TYPE_CHECKING:
    from ..d2.camera_2d import Camera2D
    from ..d3.camera_3d import Camera3D
    from ..d3.lighting_3d import Lighting3D

T_Renderer = TypeVar("T_Renderer", bound="Renderer")
T_Scene = TypeVar("T_Scene")


class SceneRenderer(Generic[T_Renderer, T_Scene], Renderer):
    def __init__(
        self,
        scene: T_Scene,
        viewport: Viewport,
        camera_2d: "Camera2D" = None,
        camera_3d: "Camera3D" = None,
        lighting_3d: "Lighting3D" = None,
    ) -> None:
        super().__init__(viewport, camera_2d=camera_2d, camera_3d=camera_3d, lighting_3d=lighting_3d)
        self.scene = scene
        self.root_phase: RenderPhase[T_Renderer] = None

    def create_phases(self) -> None:
        pass

    def render(self) -> None:
        self.create_phases()
        self.root_phase.render()
