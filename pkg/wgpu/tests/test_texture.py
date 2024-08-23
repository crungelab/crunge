from crunge import wgpu
from crunge.wgpu import BackendType

def main():
    instance = wgpu.create_instance()
    adapter = instance.request_adapter()
    props = adapter.get_properties()
    print(props.vendor_name)
    device = adapter.create_device()
    print(device)
    device.enable_logging()

    '''
    descriptor = wgpu.TextureDescriptor()
    descriptor.usage = wgpu.TextureUsage.RENDER_ATTACHMENT | wgpu.TextureUsage.COPY_SRC
    descriptor.size = wgpu.Extent3D(1, 1, 1)
    descriptor.format = wgpu.TextureFormat.BGRA8_UNORM
    '''
    descriptor = wgpu.TextureDescriptor(
        usage=wgpu.TextureUsage.RENDER_ATTACHMENT | wgpu.TextureUsage.COPY_SRC,
        size=wgpu.Extent3D(1, 1, 1),
        format=wgpu.TextureFormat.BGRA8_UNORM,
    )
    texture = device.create_texture(descriptor)

    print(texture)

if __name__ == "__main__":
    main()
