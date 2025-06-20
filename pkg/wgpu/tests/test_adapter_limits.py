from crunge import wgpu


def main():
    capabilities = wgpu.InstanceCapabilities(timed_wait_any_enable = True)
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

    limits = wgpu.Limits()
    adapter.get_limits(limits)

    print(f'limits: {limits}')
    print(f'limits.max_texture_dimension_1d: {limits.max_texture_dimension_1D}')
    print(f'limits.max_texture_dimension_2d: {limits.max_texture_dimension_2D}')
    print(f'limits.max_texture_dimension_3d: {limits.max_texture_dimension_3D}')
    print(f'limits.max_texture_array_layers: {limits.max_texture_array_layers}')
    print(f'limits.max_bind_groups: {limits.max_bind_groups}')
    print(f'limits.max_bindings_per_bind_group: {limits.max_bindings_per_bind_group}')
    print(f'limits.max_dynamic_uniform_buffers_per_pipeline_layout: {limits.max_dynamic_uniform_buffers_per_pipeline_layout}')
    print(f'limits.max_dynamic_storage_buffers_per_pipeline_layout: {limits.max_dynamic_storage_buffers_per_pipeline_layout}')
    print(f'limits.max_sampled_textures_per_shader_stage: {limits.max_sampled_textures_per_shader_stage}')
    print(f'limits.max_samplers_per_shader_stage: {limits.max_samplers_per_shader_stage}')
    print(f'limits.max_storage_buffers_per_shader_stage: {limits.max_storage_buffers_per_shader_stage}')
    print(f'limits.max_storage_textures_per_shader_stage: {limits.max_storage_textures_per_shader_stage}')
    print(f'limits.max_uniform_buffers_per_shader_stage: {limits.max_uniform_buffers_per_shader_stage}')

if __name__ == "__main__":
    main()