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

    descriptor = wgpu.TextureDescriptor()
    descriptor.usage = wgpu.TextureUsage.RENDER_ATTACHMENT | wgpu.TextureUsage.COPY_SRC
    descriptor.size = wgpu.Extent3D(1, 1, 1)
    descriptor.format = wgpu.TextureFormat.BGRA8_UNORM
    texture = device.create_texture(descriptor)
    print(texture)

"""
wgpu::TextureDescriptor descriptor{};
descriptor.usage = wgpu::TextureUsage::RenderAttachment | wgpu::TextureUsage::CopySrc;
descriptor.size = {1, 1, 1};
descriptor.format = wgpu::TextureFormat::BGRA8Unorm;
readbackTexture = device.CreateTexture(&descriptor);
"""

if __name__ == "__main__":
    main()
