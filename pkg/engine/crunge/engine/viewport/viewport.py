from typing import TYPE_CHECKING, TypeVar, Generic, Dict, List, Callable, Any

import glm

from crunge import wgpu
from crunge import skia

from ..base import Base

class ViewportListener():
    def on_viewport_size(self, viewport: "Viewport") -> None:
        pass


class Viewport(Base):
    def __init__(
        self,
        size: glm.ivec2,
        use_depth_stencil: bool = False,
        use_msaa: bool = False,
        use_snapshot: bool = False,
    ):
        self._size = size
        self.listeners: List[ViewportListener] = []

        self.use_depth_stencil = use_depth_stencil
        self.use_msaa = use_msaa
        self.sample_count = 4 if use_msaa else 1
        self.use_snapshot = use_snapshot

        self.color_texture: wgpu.Texture = None
        self.color_texture_view: wgpu.TextureView = None

        self.depth_stencil_texture: wgpu.Texture = None
        self.depth_stencil_texture_view: wgpu.TextureView = None

        self.msaa_texture: wgpu.Texture = None
        self.msaa_texture_view: wgpu.TextureView = None

        self.snapshot_texture: wgpu.Texture = None
        self.snapshot_texture_view: wgpu.TextureView = None

        # Skia
        self.skia_context = skia.create_context(self.gfx.instance, self.gfx.device)
        recorder_options = skia.create_standard_recorder_options()
        self.recorder = self.skia_context.make_recorder(recorder_options)
        self.skia_surface: skia.Surface = None # segfaults if we don't hang on to a reference
        self.canvas: skia.Canvas = None

        self.create_device_objects()

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
        if self.use_depth_stencil:
            self.create_depth_stencil()
        if self.use_msaa:
            self.create_msaa()
        if self.use_snapshot:
            self.create_snapshot()

    def create_depth_stencil(self) -> None:
        descriptor = wgpu.TextureDescriptor(
            usage=wgpu.TextureUsage.RENDER_ATTACHMENT,
            size=wgpu.Extent3D(self.width, self.height, 1),
            format=wgpu.TextureFormat.DEPTH24_PLUS,
            sample_count=self.sample_count,
        )
        self.depth_stencil_texture = self.device.create_texture(descriptor)
        self.depth_stencil_texture_view = self.depth_stencil_texture.create_view()

    def create_msaa(self) -> None:
        descriptor = wgpu.TextureDescriptor(
            usage=wgpu.TextureUsage.RENDER_ATTACHMENT | wgpu.TextureUsage.COPY_SRC,
            size=wgpu.Extent3D(self.width, self.height, 1),
            format=wgpu.TextureFormat.BGRA8_UNORM,
            sample_count=self.sample_count,
            mip_level_count=1,
        )
        self.msaa_texture = self.device.create_texture(descriptor)
        self.msaa_texture_view = self.msaa_texture.create_view()

    def create_snapshot(self) -> None:
        descriptor = wgpu.TextureDescriptor(
            usage=wgpu.TextureUsage.RENDER_ATTACHMENT | wgpu.TextureUsage.COPY_DST,
            size=wgpu.Extent3D(self.width, self.height, 1),
            format=wgpu.TextureFormat.BGRA8_UNORM,
            sample_count=self.sample_count,
            mip_level_count=1,
        )
        self.snapshot_texture = self.device.create_texture(descriptor)
        self.snapshot_texture_view = self.msaa_texture.create_view()

    def snap(self):
        if not self.use_snapshot:
            raise RuntimeError("Snapshot is not enabled for this viewport.")
        
        if self.snapshot_texture is None:
            self.create_snapshot()
        
        # Create a command encoder to copy the MSAA texture to the snapshot texture
        encoder = self.device.create_command_encoder()
        source=wgpu.TexelCopyTextureInfo(texture=self.msaa_texture)
        destination=wgpu.TexelCopyTextureInfo(texture=self.snapshot_texture)
        encoder.copy_texture_to_texture(
            source=source,
            destination=destination,
            copy_size=wgpu.Extent3D(self.width, self.height, 1),
        )
        
        # Submit the commands
        self.device.queue.submit([encoder.finish()])
