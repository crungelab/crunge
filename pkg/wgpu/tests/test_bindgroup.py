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
    #feature_name = FeatureName()
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

"""
wgpu::BindGroupLayoutDescriptor bglDesc{};
auto bgl = device.CreateBindGroupLayout(&bglDesc);
wgpu::BindGroupDescriptor desc{};
desc.layout = bgl;
desc.entryCount = 0;
desc.entries = nullptr;
device.CreateBindGroup(&desc);
"""