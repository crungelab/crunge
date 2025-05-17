from loguru import logger
import glm
import numpy as np

from crunge import wgpu
from crunge.wgpu import utils

from .constants import *
from .base import Base
from .scene import Scene
from .camera import Camera


class View(Base):
    scene: Scene = None
    surface: wgpu.Surface = None

    def __init__(self, scene: Scene, size: glm.ivec2) -> None:
        self.scene = scene
        self.size = size
        self.camera = Camera(size)
        self.depthTexture = utils.create_texture(
            self.device,
            "Depth texture",
            wgpu.Extent3D(size.x, size.y),
            wgpu.TextureFormat.DEPTH24_PLUS,
            wgpu.TextureUsage.RENDER_ATTACHMENT,
        )

    def create_from_wsd(self, wsd):
        sd = wgpu.SurfaceDescriptor(next_in_chain=wsd)
        self.surface = self.instance.create_surface(sd)
        logger.debug(self.surface)
        self.configure_surface(self.size)

    def configure_surface(self, size: glm.ivec2):
        logger.debug("Configuring surface")

        if not size.x or not size.y:
            return

        logger.debug("Creating surface configuration")
        config = wgpu.SurfaceConfiguration(
            device=self.device,
            width=size.x,
            height=size.y,
            format=wgpu.TextureFormat.BGRA8_UNORM,
            usage=wgpu.TextureUsage.RENDER_ATTACHMENT,
            present_mode=wgpu.PresentMode.FIFO,
            alpha_mode=wgpu.CompositeAlphaMode.OPAQUE,
        )
        logger.debug(config)
        self.surface.configure(config)
        logger.debug(f"Surface configured to size: {size}")

    def frame(self):
        surface_texture = wgpu.SurfaceTexture()
        self.surface.get_current_texture(surface_texture)
        backbufferView: wgpu.TextureView = surface_texture.texture.create_view()

        self.draw(backbufferView)
        self.surface.present()

    def draw(self, view: wgpu.TextureView):
        # self.camera.update()

        color_attachments = [
            wgpu.RenderPassColorAttachment(
                view=view,
                load_op=wgpu.LoadOp.CLEAR,
                store_op=wgpu.StoreOp.STORE,
                clear_value=wgpu.Color(0, 0, 0, 1),
                # clear_value=wgpu.Color(.5, .5, .5, 1),
            )
        ]

        depthStencilAttach = wgpu.RenderPassDepthStencilAttachment(
            view=self.depthTexture.create_view(),
            depth_load_op=wgpu.LoadOp.CLEAR,
            depth_store_op=wgpu.StoreOp.STORE,
            depth_clear_value=1.0,
        )

        renderpass = wgpu.RenderPassDescriptor(
            label="Main Render Pass",
            color_attachments=color_attachments,
            depth_stencil_attachment=depthStencilAttach,
        )

        encoder: wgpu.CommandEncoder = self.device.create_command_encoder()
        pass_enc: wgpu.RenderPassEncoder = encoder.begin_render_pass(renderpass)
        self.scene.draw(self.camera, pass_enc)
        pass_enc.end()
        commands = encoder.finish()

        self.device.queue.submit(1, commands)
        # exit()
