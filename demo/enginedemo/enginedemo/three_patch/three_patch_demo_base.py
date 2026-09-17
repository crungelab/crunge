import time

import glm

from crunge import wgpu
from crunge.engine import Viewport

from ..demo import Demo


class ThreePatchDemoBase(Demo):
    """
    Draws every renderer in `self.patches` in one render pass.

    Subclasses build their renderers in `create_patches` and position them
    each frame in `arrange_patches`.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.patches = []
        self.start_time = time.perf_counter()

    def create_device_objects(self):
        self.patches = self.create_patches()

    def create_patches(self) -> list:
        raise NotImplementedError

    def layout_patches(
        self, view_projection: glm.mat4, width: float, height: float, elapsed: float
    ):
        raise NotImplementedError

    def skin_paths(self, *names: str):
        return [self.resource_root / "skins" / name for name in names]

    def _draw(self):
        viewport = Viewport.get_current()
        easel = viewport.easel

        color_attachments = [
            wgpu.RenderPassColorAttachment(
                view=easel.color_texture_view,
                load_op=wgpu.LoadOp.CLEAR,
                store_op=wgpu.StoreOp.STORE,
                clear_value=wgpu.Color(0.2, 0.3, 0.4, 1),
            )
        ]

        renderpass = wgpu.RenderPassDescriptor(
            label="Main Render Pass",
            color_attachments=color_attachments,
        )

        encoder: wgpu.CommandEncoder = self.device.create_command_encoder()
        pass_enc: wgpu.RenderPassEncoder = encoder.begin_render_pass(renderpass)
        for patch in self.patches:
            patch.draw(pass_enc)
        pass_enc.end()

        self.queue.submit([encoder.finish()])

        super()._draw()

    def frame(self):
        width = self.viewport.width
        height = self.viewport.height

        # View is identity, so the projection is the whole view-projection
        view_projection = glm.ortho(0, width, 0, height, -1, 1)

        elapsed = time.perf_counter() - self.start_time
        self.layout_patches(view_projection, width, height, elapsed)

        super().frame()
