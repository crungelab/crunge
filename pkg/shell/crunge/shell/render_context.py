from crunge import wgpu

class RenderContext:
    def __init__(self, device: wgpu.Device, view: wgpu.TextureView, depthStencilView: wgpu.TextureView = None):
        self.device = device
        self.view = view
        self.depthStencilView = depthStencilView