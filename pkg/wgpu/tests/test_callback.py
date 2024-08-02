from crunge import wgpu
from crunge.wgpu import BackendType

#TODO: Have to implement callbacks first!

def main():
    instance = wgpu.create_instance()
    adapter = instance.request_adapter()
    props = adapter.get_properties()
    print(props.vendor_name)
    device = adapter.create_device()
    print(device)

    device.set_uncaptured_error_callback(lambda type, message, userdata: print(message))

if __name__ == "__main__":
    main()