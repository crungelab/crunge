import glm

from crunge import wgpu
from crunge.wgpu import utils

from ..base import Base


class Viewport(Base):
    def __init__(
        self,
        width: int,
        height: int,
        use_depth_stencil: bool = False,
        use_msaa: bool = False,
    ):
        self._size = glm.ivec2(width, height)
        self.use_depth_stencil = use_depth_stencil
        self.use_msaa = use_msaa
        self.sample_count = 4 if use_msaa else 1

        self.color_texture: wgpu.Texture = None
        self.color_texture_view: wgpu.TextureView = None
        self.depth_stencil_texture: wgpu.Texture = None
        self.depth_stencil_texture_view: wgpu.TextureView = None
        self.msaa_texture: wgpu.Texture = None
        self.msaa_texture_view: wgpu.TextureView = None

        if use_depth_stencil:
            self.create_depth_stencil()

        if use_msaa:
            self.create_msaa()

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
        if self.use_depth_stencil:
            self.create_depth_stencil()
        if self.use_msaa:
            self.create_msaa()

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

    def create_depth_stencil(self):
        descriptor = wgpu.TextureDescriptor(
            usage=wgpu.TextureUsage.RENDER_ATTACHMENT,
            size=wgpu.Extent3D(self.width, self.height, 1),
            format=wgpu.TextureFormat.DEPTH24_PLUS,
            sample_count=self.sample_count,
        )
        '''
        self.window.renderer.depth_stencil_view = self.device.create_texture(
            descriptor
        ).create_view()
        '''
        self.depth_stencil_texture = self.device.create_texture(descriptor)
        self.depth_stencil_texture_view = self.depth_stencil_texture.create_view()

    '''
    def create_depth_stencil(self):
        self.depth_stencil_texture = utils.create_texture(
            self.device,
            "Depth texture",
            wgpu.Extent3D(self.size.x, self.size.y),
            wgpu.TextureFormat.DEPTH24_PLUS,
            wgpu.TextureUsage.RENDER_ATTACHMENT,
        )
        self.depth_stencil_texture_view = self.depth_stencil_texture.create_view()
    '''

    def create_msaa(self):
        descriptor = wgpu.TextureDescriptor(
            usage=wgpu.TextureUsage.RENDER_ATTACHMENT,
            size=wgpu.Extent3D(self.width, self.height, 1),
            sample_count=self.sample_count,
            format=wgpu.TextureFormat.BGRA8_UNORM,
            mip_level_count=1,
        )
        '''
        self.window.renderer.msaa_view = self.device.create_texture(
            descriptor
        ).create_view()
        '''
        self.msaa_texture = self.device.create_texture(descriptor)
        self.msaa_texture_view = self.msaa_texture.create_view()