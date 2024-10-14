from crunge.core.event_source import EventSource
from crunge import wgpu

from ..math import Size2i
from ..base import Base


class Viewport(Base):
    def __init__(
        self,
        size: Size2i,
        use_depth_stencil: bool = False,
        use_msaa: bool = False,
    ):
        self._size = size
        self.size_events = EventSource[Size2i]()

        self.use_depth_stencil = use_depth_stencil
        self.use_msaa = use_msaa
        self.sample_count = 4 if use_msaa else 1

        self.color_texture: wgpu.Texture = None
        self.color_texture_view: wgpu.TextureView = None
        self.depth_stencil_texture: wgpu.Texture = None
        self.depth_stencil_texture_view: wgpu.TextureView = None
        self.msaa_texture: wgpu.Texture = None
        self.msaa_texture_view: wgpu.TextureView = None

        self.create_device_objects()

    @property
    def size(self) -> Size2i:
        return self._size

    @size.setter
    def size(self, value: Size2i):
        changed = self._size != value
        self._size = value
        if changed:
            self.on_size()

    def on_size(self) -> None:
        self.create_device_objects()
        self.size_events.publish(self._size)

    @property
    def width(self) -> int:
        return self._size.x

    @property
    def height(self) -> int:
        return self._size.y

    def frame(self) -> None:
        pass

    def present(self) -> None:
        pass

    def create_device_objects(self) -> None:
        if self.use_depth_stencil:
            self.create_depth_stencil()
        if self.use_msaa:
            self.create_msaa()

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
            usage=wgpu.TextureUsage.RENDER_ATTACHMENT,
            size=wgpu.Extent3D(self.width, self.height, 1),
            format=wgpu.TextureFormat.BGRA8_UNORM,
            sample_count=self.sample_count,
            mip_level_count=1,
        )
        self.msaa_texture = self.device.create_texture(descriptor)
        self.msaa_texture_view = self.msaa_texture.create_view()
