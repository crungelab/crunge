import inspect
import crunge.wgpu._wgpu as _wgpu
from crunge.wgpu.generated import RequestAdapterOptions

inst = _wgpu.create_instance(None)

print("callable:", inst._request_adapter)
print("signature:", inspect.signature(inst._request_adapter))
print("options type:", RequestAdapterOptions)
