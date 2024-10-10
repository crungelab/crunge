'''
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..d2.camera_2d import Camera2D
    from ..d3.camera_3d import Camera3D
'''

import glm

from crunge.core.event_source import EventSource
from crunge import wgpu

from ..base import Base
#from ..camera import CameraAdapter


class Viewport(Base):
    def __init__(
        self,
        width: int,
        height: int,
        use_depth_stencil: bool = False,
        use_msaa: bool = False,
    ):
        self._size = glm.ivec2(width, height)
        self.size_events = EventSource[glm.ivec2]()

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

        #self.camera_2d: "Camera2D" = None
        #self.camera_3d: "Camera3D" = None
        #self.camera_adapter: CameraAdapter = None

    @property
    def size(self) -> glm.ivec2:
        return self._size

    @size.setter
    def size(self, value: glm.ivec2):
        changed = self._size != value
        self._size = value
        if changed:
            self.on_size()

    def on_size(self):
        self.create_device_objects()
        self.size_events.publish(self._size)

    @property
    def width(self) -> int:
        return self._size.x

    @property
    def height(self) -> int:
        return self._size.y

    def frame(self):
        pass

    def present(self):
        pass

    def create_device_objects(self):
        if self.use_depth_stencil:
            self.create_depth_stencil()
        if self.use_msaa:
            self.create_msaa()

    def create_depth_stencil(self):
        descriptor = wgpu.TextureDescriptor(
            usage=wgpu.TextureUsage.RENDER_ATTACHMENT,
            size=wgpu.Extent3D(self.width, self.height, 1),
            format=wgpu.TextureFormat.DEPTH24_PLUS,
            sample_count=self.sample_count,
        )
        self.depth_stencil_texture = self.device.create_texture(descriptor)
        self.depth_stencil_texture_view = self.depth_stencil_texture.create_view()

    def create_msaa(self):
        descriptor = wgpu.TextureDescriptor(
            usage=wgpu.TextureUsage.RENDER_ATTACHMENT,
            size=wgpu.Extent3D(self.width, self.height, 1),
            format=wgpu.TextureFormat.BGRA8_UNORM,
            sample_count=self.sample_count,
            mip_level_count=1,
        )
        self.msaa_texture = self.device.create_texture(descriptor)
        self.msaa_texture_view = self.msaa_texture.create_view()