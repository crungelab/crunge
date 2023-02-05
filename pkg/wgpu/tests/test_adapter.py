from crunge import wgpu
from crunge.wgpu import BackendType

def main():
    #adapter = wgpu.request_adapter(BackendType.D3_D12)
    instance = wgpu.create_instance()
    adapter = instance.request_adapter()
    props = wgpu.AdapterProperties()
    adapter.get_properties(props)
    print(props.vendor_name)

if __name__ == "__main__":
    main()