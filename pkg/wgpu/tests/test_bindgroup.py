from crunge import wgpu


def main():
    wgpu_context = wgpu.Context()
    device = wgpu_context.device

    bgl_desc = wgpu.BindGroupLayoutDescriptor(entries=[])
    bgl = device.create_bind_group_layout(bgl_desc)
    desc = wgpu.BindGroupDescriptor(layout=bgl, entries=[])
    bg = device.create_bind_group(desc)

    print(bg)


if __name__ == "__main__":
    main()
