from loguru import logger
import glm

from crunge import wgpu

from crunge.engine.imgui import ImGuiView

from crunge.engine.d3.scene_3d import Scene3D
from crunge.engine.d3.renderer_3d import Renderer3D
from crunge.engine.d3.camera_3d import Camera3D

from crunge.engine.gltf.constants import SAMPLE_COUNT


class View(ImGuiView):
    def __init__(self, scene: Scene3D, size=glm.ivec2()) -> None:
        super().__init__(size)
        self.scene = scene
        self.camera = Camera3D(size)

    def create_device_objects(self):
        self.create_depth_stencil_view()
        self.create_msaa_view()

    def create_depth_stencil_view(self):
        descriptor = wgpu.TextureDescriptor(
            usage=wgpu.TextureUsage.RENDER_ATTACHMENT,
            size=wgpu.Extent3D(self.width, self.height, 1),
            format=wgpu.TextureFormat.DEPTH24_PLUS,
            sample_count=SAMPLE_COUNT,
        )
        self.window.renderer.depth_stencil_view = self.device.create_texture(
            descriptor
        ).create_view()

    def create_msaa_view(self):
        descriptor = wgpu.TextureDescriptor(
            usage=wgpu.TextureUsage.RENDER_ATTACHMENT,
            size=wgpu.Extent3D(self.width, self.height, 1),
            sample_count=SAMPLE_COUNT,
            format=wgpu.TextureFormat.BGRA8_UNORM,
            mip_level_count=1,
        )
        self.window.renderer.msaa_view = self.device.create_texture(
            descriptor
        ).create_view()

    def resize(self, size: glm.ivec2):
        super().resize(size)
        self.resize_camera(size)
        self.create_depth_stencil_view()
        self.create_msaa_view()

    def resize_camera(self, size: glm.ivec2):
        self.camera.size = size

    def draw(self, renderer: Renderer3D):
        # logger.debug("View.draw()")

        color_attachments = [
            wgpu.RenderPassColorAttachment(
                view=renderer.texture_view,
                # view=renderer.msaa_view,
                # resolve_target=renderer.texture_view,
                load_op=wgpu.LoadOp.CLEAR,
                store_op=wgpu.StoreOp.STORE,
                clear_value=wgpu.Color(0, 0, 0, 1),
                # clear_value=wgpu.Color(.5, .5, .5, 1),
            )
        ]

        depthStencilAttach = wgpu.RenderPassDepthStencilAttachment(
            view=renderer.depth_stencil_view,
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
