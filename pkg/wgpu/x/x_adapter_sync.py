from crunge import wgpu

'''
struct AdapterInfo {
    operator const WGPUAdapterInfo&() const noexcept;
    ChainedStructOut * nextInChain = nullptr;
    StringView vendor = {};
    StringView architecture = {};
    StringView device = {};
    StringView description = {};
    BackendType backendType;
    AdapterType adapterType;
    uint32_t vendorID;
    uint32_t deviceID;
    uint32_t subgroupMinSize;
    uint32_t subgroupMaxSize;
};
'''


def request_adapter_sync(instance: wgpu.Instance) -> wgpu.Adapter:
    # 1) Set up options (no surface in this example)
    options = wgpu.RequestAdapterOptions()

    # 2) Holder for the adapter we'll receive in the callback
    adapter_holder = None

    # 3) Define the callback exactly like the C++ lambda did
    def on_adapter_request(status, adapter, message):
        print("on_adapter_request called")
        nonlocal adapter_holder

        if status != wgpu.RequestAdapterStatus.SUCCESS:
            print(f"Failed to get an adapter: {message}")
        else:
            print("Got an adapter")
            print(f"message: {message}")
            adapter_holder = adapter

    callback_info = wgpu.RequestAdapterCallbackInfo(
        #mode=wgpu.CallbackMode.ALLOW_PROCESS_EVENTS,
        mode=wgpu.CallbackMode.WAIT_ANY_ONLY,
        callback=on_adapter_request
    )

    # 5) Kick off the async request
    future = instance._request_adapter(options, callback_info)

    print("Called request_adapter")
    print(f"future: {future}")
    print(f"future.id: {future.id}")


    # 6) Block until the callback fires (or timeout)
    wait_info = wgpu.FutureWaitInfo(future=future, completed=False)
    #_last_wait_info = wait_info
    print("Created wgpu.FutureWaitInfo")
    # UINT64_MAX for no real timeout:
    instance.wait_any([wait_info], 0xFFFFFFFFFFFFFFFF)
    #instance.wait_any(1, wait_info, 0xFFFFFFFFFFFFFFFF)
    print("wait_any returned")
    # 7) Pull the adapter out and return it (or None on failure)
    return adapter_holder

def main():
    capabilities = wgpu.InstanceCapabilities(timed_wait_any_enable = True)
    instance_descriptor = wgpu.InstanceDescriptor(capabilities=capabilities)
    instance = wgpu.create_instance(instance_descriptor)

    #adapter = instance.request_adapter()
    adapter = request_adapter_sync(instance)
    if adapter is None:
        print("Failed to get an adapter")
        return
    
    print("Got an adapter")

    info = wgpu.AdapterInfo()
    status = adapter.get_info(info)
    print(f'status: {status}')

    print(f'vendor: {info.vendor}')
    #print(f'vendor_id: {info.vendor_id}')
    print(f'vendor_id: {info.vendor_ID}')

    print(f'architecture: {info.architecture}')

    print(f'device: {info.device}')
    #print(f'device_id: {info.device_id}')
    print(f'device_id: {info.device_ID}')

    print(f'description: {info.description}')
    print(f'backend_type: {info.backend_type}')
    print(f'adapter_type: {info.adapter_type}')

    print(f'subgroup_min_size: {info.subgroup_min_size}')
    print(f'subgroup_max_size: {info.subgroup_max_size}')

if __name__ == "__main__":
    main()