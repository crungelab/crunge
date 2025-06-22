from typing import TYPE_CHECKING, TypeVar, Generic, Dict, List, Callable, Any
from ctypes import sizeof

from loguru import logger
import glm

from crunge import wgpu
from crunge import skia

from ..base import Base
from ..uniforms import ViewportUniform, cast_vec2

# from ..bindings import ViewportBindGroup
from ..render_options import RenderOptions
from ..blitter import Blitter


class ViewportListener:
    def on_viewport_size(self, viewport: "Viewport") -> None:
        pass


class Viewport(Base):
    def __init__(
        self,
        size: glm.ivec2,
        render_options: RenderOptions = RenderOptions(),
    ):
        self._size = size
        self.render_options = render_options
        self.listeners: List[ViewportListener] = []

        """
        self.use_depth_stencil = use_depth_stencil
        self.use_msaa = use_msaa
        self.sample_count = 4 if use_msaa else 1
        self.use_snapshot = use_snapshot
        """
        self.color_texture: wgpu.Texture = None
        self.color_texture_view: wgpu.TextureView = None

        self.depth_stencil_texture: wgpu.Texture = None
        self.depth_stencil_texture_view: wgpu.TextureView = None

        self.msaa_texture: wgpu.Texture = None
        self.msaa_texture_view: wgpu.TextureView = None

        self.snapshot_texture: wgpu.Texture = None
        self.snapshot_texture_view: wgpu.TextureView = None
        self.snapshot_sampler: wgpu.Sampler = None
        self.blitter: Blitter = None

        # Skia
        self.skia_context = skia.create_context(self.gfx.instance, self.gfx.device)
        recorder_options = skia.create_standard_recorder_options()
        self.recorder = self.skia_context.make_recorder(recorder_options)
        self.skia_surface: skia.Surface = (
            None  # segfaults if we don't hang on to a reference
        )
        self.canvas: skia.Canvas = None

        self.create_device_objects()
        self.create_buffers()
        # self.create_bind_group()
        self.update_gpu()

    def add_listener(self, listener: ViewportListener) -> None:
        if listener not in self.listeners:
            self.listeners.append(listener)

    @property
    def size(self) -> glm.ivec2:
        return self._size

    @size.setter
    def size(self, value: glm.ivec2):
        changed = self._size != value
        self._size = value
        if changed:
            self.on_size()

    def on_size(self) -> None:
        self.create_device_objects()
        self.update_gpu()
        for listener in self.listeners:
            listener.on_viewport_size(self._size)

    @property
    def width(self) -> int:
        return self._size.x

    @property
    def height(self) -> int:
        return self._size.y

    def __enter__(self):
        self.frame()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.present()

    def frame(self) -> None:
        pass

    def present(self) -> None:
        pass

    def create_device_objects(self) -> None:
        if self.render_options.use_depth_stencil:
            self.create_depth_stencil()
        if self.render_options.use_msaa:
            self.create_msaa()
        if self.render_options.use_snapshot:
            self.create_snapshot()

    def create_depth_stencil(self) -> None:
        descriptor = wgpu.TextureDescriptor(
            usage=wgpu.TextureUsage.RENDER_ATTACHMENT,
            size=wgpu.Extent3D(self.width, self.height, 1),
            format=wgpu.TextureFormat.DEPTH24_PLUS,
            sample_count=self.render_options.sample_count,
        )
        self.depth_stencil_texture = self.device.create_texture(descriptor)
        self.depth_stencil_texture_view = self.depth_stencil_texture.create_view()

    def create_msaa(self) -> None:
        descriptor = wgpu.TextureDescriptor(
            usage=wgpu.TextureUsage.RENDER_ATTACHMENT
            | wgpu.TextureUsage.COPY_SRC
            | wgpu.TextureUsage.TEXTURE_BINDING,
            size=wgpu.Extent3D(self.width, self.height, 1),
            format=wgpu.TextureFormat.BGRA8_UNORM,
            sample_count=self.render_options.sample_count,
            mip_level_count=1,
            label="MSAA Texture",
        )
        self.msaa_texture = self.device.create_texture(descriptor)
        self.msaa_texture_view = self.msaa_texture.create_view()

    def create_snapshot(self) -> None:
        descriptor = wgpu.TextureDescriptor(
            usage=wgpu.TextureUsage.RENDER_ATTACHMENT
            | wgpu.TextureUsage.COPY_DST
            | wgpu.TextureUsage.TEXTURE_BINDING,
            size=wgpu.Extent3D(self.width, self.height, 1),
            format=wgpu.TextureFormat.BGRA8_UNORM,
            mip_level_count=1,
            label="Snapshot Texture",
        )
        self.snapshot_texture = self.device.create_texture(descriptor)
        self.snapshot_texture_view = self.snapshot_texture.create_view()

        sampler_desc = wgpu.SamplerDescriptor(
            min_filter=wgpu.FilterMode.LINEAR,
            #min_filter=wgpu.FilterMode.NEAREST,
            mag_filter=wgpu.FilterMode.LINEAR,
            #mag_filter=wgpu.FilterMode.NEAREST,
            mipmap_filter=wgpu.MipmapFilterMode.LINEAR,
            address_mode_u=wgpu.AddressMode.CLAMP_TO_EDGE,
            address_mode_v=wgpu.AddressMode.CLAMP_TO_EDGE,
            address_mode_w=wgpu.AddressMode.CLAMP_TO_EDGE,
            max_anisotropy=1,
        )

        self.snapshot_sampler = self.device.create_sampler(sampler_desc)

        # This is commented out because it causes a segfault when resizing the viewport.
        # It seems to be related to the Blitter holding a reference to the textures.
        '''
        if self.color_texture is not None:
            self.blitter = Blitter(self.color_texture, self.snapshot_texture)
        '''

    '''
    def snap(self):
        if not self.render_options.use_snapshot:
            # raise RuntimeError("Snapshot is not enabled for this viewport.")
            return

        if self.snapshot_texture is None:
            self.create_snapshot()

        #blitter = Blitter(self.color_texture, self.snapshot_texture)
        #blitter.blit()
        if self.blitter is not None:
            self.blitter.blit()
    '''

    def snap(self, encoder: wgpu.CommandEncoder):
        if not self.render_options.use_snapshot:
            #raise RuntimeError("Snapshot is not enabled for this viewport.")
            return
        
        if self.snapshot_texture is None:
            self.create_snapshot()

        # Create a command encoder to copy the color texture to the snapshot texture
        #encoder = self.device.create_command_encoder()
        source=wgpu.TexelCopyTextureInfo(texture=self.color_texture)
        destination=wgpu.TexelCopyTextureInfo(texture=self.snapshot_texture)
        encoder.copy_texture_to_texture(
            source=source,
            destination=destination,
            copy_size=wgpu.Extent3D(self.width, self.height, 1),
        )
        
        # Submit the commands
        #self.device.queue.submit([encoder.finish()])

    def create_buffers(self):
        # Uniform Buffers
        self.uniform_buffer_size = sizeof(ViewportUniform)
        self.uniform_buffer = self.gfx.create_buffer(
            "Viewport Uniform Buffer",
            self.uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )

    """
    def create_bind_group(self):
        self.bind_group = ViewportBindGroup(
            self.uniform_buffer,
            self.uniform_buffer_size,
            self.snapshot_texture_view,
            self.snapshot_sampler,
        )
    """

    """
    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        self.bind_group.bind(pass_enc)
    """

    def update_gpu(self):
        uniform = ViewportUniform()
        uniform.size = cast_vec2(self.size)

        self.device.queue.write_buffer(self.uniform_buffer, 0, uniform)
