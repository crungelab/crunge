from crunge import wgpu

class RenderContext:
    def __init__(self):
        self.texture_view: wgpu.TextureView = None
        self.depth_stencil_view: wgpu.TextureView = None