from ...viewport import Viewport
from ...renderer import SceneRenderer

from ..camera_3d import Camera3D
from ..lighting_3d import Lighting3D

from ..scene_3d import Scene3D

from .render_pass_3d import RenderPass3D
from .phase import RenderPlan3D, OpaquePhase3D, TransmissivePhase3D


class SceneRenderer3D(SceneRenderer["SceneRenderer3D", Scene3D]):
    def __init__(
        self,
        scene: Scene3D,
        viewport: Viewport,
        camera: Camera3D = None,
        lighting: Lighting3D = None,
    ) -> None:
        super().__init__(scene, viewport, camera_3d=camera, lighting_3d=lighting)

    def create_render_pass(self):
        return RenderPass3D(self.viewport, first=True)

    def create_phases(self) -> None:
        phases = [
            OpaquePhase3D(self),
            TransmissivePhase3D(self)
        ]
        self.root_phase = RenderPlan3D(self, phases)

    """
    def create_phases(self) -> None:
        self.phases = [
            OpaquePhase3D(self),
            TransmissivePhase3D(self)
        ]
    """

    """
    def render(self):
        with self.render_pass():
            self.scene.draw()
    """
