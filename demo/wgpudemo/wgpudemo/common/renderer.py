from crunge import wgpu


class Renderer:
    def __init__(self, view: wgpu.TextureView, depth_stencil_view: wgpu.TextureView = None):
        self.view = view
        self.depth_stencil_view = depth_stencil_view