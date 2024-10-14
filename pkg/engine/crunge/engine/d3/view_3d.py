from loguru import logger
import glm

from crunge import wgpu

from crunge.engine.imgui import ImGuiView

from crunge.engine.d3.scene_3d import Scene3D
from crunge.engine.d3.renderer_3d import Renderer3D
from crunge.engine.d3.camera_3d import Camera3D


class View3D(ImGuiView):
    def __init__(self, scene: Scene3D, size=glm.ivec2()) -> None:
        super().__init__(size)
        self.scene = scene
        self.camera = Camera3D(size)

    def create_renderer(self):
        self.renderer = Renderer3D(self.window.viewport, self.camera)

    def on_size(self):
        super().on_size()
        self.camera.size = self.size

    def draw(self, renderer: Renderer3D):
        with self.renderer:
            self.scene.draw(self.renderer)
            super().draw(self.renderer)

    '''
    def draw(self, renderer: Renderer3D):
        if renderer.viewport.use_msaa:
            color_attachments = [
                wgpu.RenderPassColorAttachment(
                    view=renderer.viewport.msaa_texture_view,
                    resolve_target=renderer.viewport.color_texture_view,

                    load_op=wgpu.LoadOp.CLEAR,
                    store_op=wgpu.StoreOp.STORE,
                    clear_value=wgpu.Color(0, 0, 0, 1),
                )
            ]
        else:
            color_attachments = [
                wgpu.RenderPassColorAttachment(
                    view=renderer.viewport.color_texture_view,
                    load_op=wgpu.LoadOp.CLEAR,
                    store_op=wgpu.StoreOp.STORE,
                    clear_value=wgpu.Color(0, 0, 0, 1),
                    # clear_value=wgpu.Color(.5, .5, .5, 1),
                )
            ]

        depthStencilAttach = wgpu.RenderPassDepthStencilAttachment(
            view=renderer.viewport.depth_stencil_texture_view,
            depth_load_op=wgpu.LoadOp.CLEAR,
            depth_store_op=wgpu.StoreOp.STORE,
            depth_clear_value=1.0,
        )

        renderpass = wgpu.RenderPassDescriptor(
            label="Main Render Pass",
            color_attachment_count=1,
            color_attachments=color_attachments,
            depth_stencil_attachment=depthStencilAttach,
        )

        encoder: wgpu.CommandEncoder = self.device.create_command_encoder()
        pass_enc: wgpu.RenderPassEncoder = encoder.begin_render_pass(renderpass)
        renderer.pass_enc = pass_enc
        renderer.camera = self.camera
        self.scene.draw(renderer)
        pass_enc.end()
        commands = encoder.finish()

        self.device.queue.submit(1, commands)

        super().draw(renderer)
        '''