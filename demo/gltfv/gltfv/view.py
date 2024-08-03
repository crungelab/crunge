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
    swap_chain: wgpu.SwapChain = None
    width: int = 0
    height: int = 0

    def __init__(self, scene: Scene, width: int, height: int) -> None:
        self.scene = scene
        self.width = width
        self.height = height
        self.camera = Camera(width, height)
        self.depthTexture = utils.create_texture(
            self.device,
            "Depth texture",
            wgpu.Extent3D(width, height),
            wgpu.TextureFormat.DEPTH24_PLUS,
            wgpu.TextureUsage.RENDER_ATTACHMENT,
        )

    def create_from_wsd(self, wsd):
        sd = wgpu.SurfaceDescriptor(next_in_chain=wsd)
        self.surface = self.instance.create_surface(sd)
        logger.debug(self.surface)

        scDesc = wgpu.SwapChainDescriptor(
            usage=wgpu.TextureUsage.RENDER_ATTACHMENT,
            format=wgpu.TextureFormat.BGRA8_UNORM,
            width=self.width,
            height=self.height,
            present_mode=wgpu.PresentMode.MAILBOX,
        )

        self.swap_chain = self.device.create_swap_chain(self.surface, scDesc)
        logger.debug(self.swap_chain)

    def frame(self):
        backbufferView: wgpu.TextureView = self.swap_chain.get_current_texture_view()
        backbufferView.set_label("Back Buffer Texture View")
        self.draw(backbufferView)
        self.swap_chain.present()

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
            color_attachment_count=1,
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
