from crunge import wgpu
from crunge.wgpu import BackendType

def main():
    instance = wgpu.create_instance()
    adapter = instance.request_adapter()
    props = adapter.get_properties()
    print(f'vendor_id: {props.vendor_id}')
    print(f'vendor_name: {props.vendor_name}')
    print(f'architecture: {props.architecture}')
    print(f'device_id: {props.device_id}')
    print(f'name: {props.name}')
    print(f'driver_description: {props.driver_description}')
    print(f'backend_type: {props.backend_type}')

if __name__ == "__main__":
    main()