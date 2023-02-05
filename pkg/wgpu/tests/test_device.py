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
    queue = device.get_queue()

if __name__ == "__main__":
    main()