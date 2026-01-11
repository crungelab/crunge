import inspect
from crunge import wgpu
from crunge.wgpu import RequestAdapterOptions

inst = wgpu.create_instance(None)

print("callable:", inst.request_adapter_sync)
print("signature:", inspect.signature(inst.request_adapter_sync))
print("options type:", RequestAdapterOptions)
