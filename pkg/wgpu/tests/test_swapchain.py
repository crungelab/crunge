from crunge import wgpu
from crunge.wgpu import BackendType

def main():
    instance = wgpu.create_instance()
    adapter = instance.request_adapter()
    props = wgpu.AdapterProperties()
    adapter.get_properties(props)
    print(props.vendor_name)
    device = adapter.create_device()
    print(device)


    scDesc = wgpu.SwapChainDescriptor()
    scDesc.usage = wgpu.TextureUsage.RENDER_ATTACHMENT
    scDesc.format = wgpu.TextureFormat.BGRA8_UNORM
    scDesc.width = 800
    scDesc.height = 600
    scDesc.presentMode = wgpu.PresentMode.FIFO
    swapChain = device.create_swap_chain(surface, scDesc)

"""
    wgpu::SwapChainDescriptor scDesc{};
    scDesc.usage = wgpu::TextureUsage::RenderAttachment;
    scDesc.format = wgpu::TextureFormat::BGRA8Unorm;
    scDesc.width = kWidth;
    scDesc.height = kHeight;
    scDesc.presentMode = wgpu::PresentMode::Fifo;
    swapChain = device.CreateSwapChain(surface, &scDesc);
"""