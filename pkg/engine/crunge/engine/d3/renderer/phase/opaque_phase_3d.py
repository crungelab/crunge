from .render_phase_3d import RenderPhase3D


class OpaquePhase3D(RenderPhase3D):
    def render(self) -> None:
        with self.renderer.render_pass():
            self.renderer.scene.draw()

