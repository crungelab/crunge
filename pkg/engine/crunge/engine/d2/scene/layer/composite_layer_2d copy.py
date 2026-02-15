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

    def _render(self):
        current_viewport = Viewport.get_current()
        viewport = OffscreenViewport(ivec2(current_viewport.width, current_viewport.height), current_viewport.render_options)
        current_renderer = Renderer2D.get_current()
        camera = Camera2D()
        renderer = Renderer2D(viewport, camera=camera)
        #renderer = Renderer2D(viewport, current_renderer.camera_2d)

        with viewport.use():
            with renderer.frame():
                renderer.render(self)

        def do_composite():
            self.compositor.composite(current_renderer.encoder, src_view=viewport.color_texture_view, dst_view=current_viewport.color_texture_view)
        phase: CompositePhase = current_renderer.plan.get_phase(CompositePhase)
        phase.add(CompositeItem(do_composite))


    def root_render(self):
        for child in self.children:
            child.render()
