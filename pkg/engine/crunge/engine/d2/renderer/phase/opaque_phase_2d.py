from .render_phase_2d import RenderPhase2D


class OpaquePhase2D(RenderPhase2D):
    def render(self) -> None:
        with self.renderer.frame():
            with self.renderer.render_pass():
                self.renderer.scene.draw()

    '''
    def render(self) -> None:
        with self.renderer.render_pass():
            self.renderer.scene.draw()
    '''