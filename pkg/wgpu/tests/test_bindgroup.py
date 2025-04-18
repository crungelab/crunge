from crunge import wgpu
from crunge.wgpu import BackendType


def main():
    instance = wgpu.create_instance()
    adapter = instance.request_adapter()
    device = adapter.create_device()
    print(device)
    device.enable_logging()

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
