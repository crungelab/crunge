from crunge import wgpu
from crunge.wgpu import BackendType

def main():
    instance = wgpu.create_instance()
    adapter = instance.request_adapter()
    props = adapter.get_properties()
    print(props.vendor_name)
    device = adapter.create_device()
    device.enable_logging()
    print(device)

if __name__ == "__main__":
    main()