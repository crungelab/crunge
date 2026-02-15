from glm import ivec2

from crunge.engine.scene.layer.composite_layer import CompositeLayer
from crunge.engine.viewport import Viewport, OffscreenViewport
from crunge.engine.d2.renderer import Renderer2D
from crunge.engine.d2.camera_2d import Camera2D
from crunge.engine.compositor import Compositor
from crunge.engine.renderer.task.composite_phase import CompositeItem, CompositePhase


class CompositeLayer2D(CompositeLayer):
    def __init__(self, name: str):
        super().__init__(name)
        self.compositor = Compositor()
        current_viewport = Viewport.get_current()
        self.viewport = OffscreenViewport(
            ivec2(current_viewport.width, current_viewport.height),
            current_viewport.render_options,
        )
        self.camera = Camera2D()
        self.renderer = Renderer2D(self.viewport, camera=self.camera)

    def _render(self):
        current_viewport = Viewport.get_current()
        current_renderer = Renderer2D.get_current()

        self.camera.position = current_renderer.camera_2d.position
        self.camera.zoom = current_renderer.camera_2d.zoom

        with self.viewport.frame():
            with self.renderer.frame():
                self.renderer.render(self)

        def do_composite():
            self.compositor.composite(
                current_renderer.encoder,
                src_view=self.viewport.color_texture_view,
                dst_view=current_viewport.color_texture_view,
            )

        phase: CompositePhase = current_renderer.plan.get_phase(CompositePhase)
        phase.add(CompositeItem(do_composite))

    def root_render(self):
        for child in self.children:
            child.render()
