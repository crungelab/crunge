from crunge import wgpu


def main():
    wgpu_context = wgpu.Context()
    device = wgpu_context.device

    bgl_desc = wgpu.BindGroupLayoutDescriptor()
    bgl = device.create_bind_group_layout(bgl_desc)
    desc = wgpu.BindGroupDescriptor()
    desc.layout = bgl
    desc.entry_count = 0
    desc.entries = None
    bg = device.create_bind_group(desc)
    print(bg)


if __name__ == "__main__":
    main()
