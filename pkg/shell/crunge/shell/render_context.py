from crunge import wgpu

class RenderContext:
    def __init__(self, device: wgpu.Device, texture_view: wgpu.TextureView, depth_stencil_view: wgpu.TextureView = None):
        self.device = device
        self.texture_view = texture_view
        self.depth_stencil_view = depth_stencil_view