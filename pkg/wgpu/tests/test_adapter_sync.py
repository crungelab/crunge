from crunge import wgpu


def main():
    capabilities = wgpu.InstanceCapabilities(timed_wait_any_enable=True)
    instance_descriptor = wgpu.InstanceDescriptor(capabilities=capabilities)
    instance = wgpu.create_instance(instance_descriptor)

    options = wgpu.RequestAdapterOptions()
    adapter = instance.request_adapter_sync(options)

    if adapter is None:
        print("Failed to get an adapter")
        return

    print("Got an adapter")

    info = wgpu.AdapterInfo()
    status = adapter.get_info(info)
    print(f"status: {status}")

    print(f"vendor: {info.vendor}")
    # print(f'vendor_id: {info.vendor_id}')
    print(f"vendor_id: {info.vendor_ID}")

    print(f"architecture: {info.architecture}")

    print(f"device: {info.device}")
    # print(f'device_id: {info.device_id}')
    print(f"device_id: {info.device_ID}")

    print(f"description: {info.description}")
    print(f"backend_type: {info.backend_type}")
    print(f"adapter_type: {info.adapter_type}")

    print(f"subgroup_min_size: {info.subgroup_min_size}")
    print(f"subgroup_max_size: {info.subgroup_max_size}")


if __name__ == "__main__":
    main()
