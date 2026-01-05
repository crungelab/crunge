import crunge.wgpu._wgpu as _wgpu
cb = _wgpu.RequestAdapterCallbackInfo()
print(type(cb))
print(cb.__class__.__module__, cb.__class__.__qualname__)