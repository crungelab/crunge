from crunge import wgpu


def main():
    wgpu_context = wgpu.Context()
    device = wgpu_context.device

    descriptor = wgpu.TextureDescriptor(
        usage=wgpu.TextureUsage.RENDER_ATTACHMENT | wgpu.TextureUsage.COPY_SRC,
        size=wgpu.Extent3D(1, 1, 1),
        format=wgpu.TextureFormat.BGRA8_UNORM,
    )
    texture = device.create_texture(descriptor)

    print(texture)

if __name__ == "__main__":
    main()
