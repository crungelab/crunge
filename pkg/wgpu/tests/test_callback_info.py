from loguru import logger
from crunge import wgpu

adapter_holder = None

def on_adapter_request(
    status: wgpu.RequestAdapterStatus, adapter: wgpu.Adapter, message: str
):
    logger.debug("on_adapter_request called")
    global adapter_holder

    if status != wgpu.RequestAdapterStatus.SUCCESS:
        logger.debug(f"Failed to get an adapter: {message}")
    else:
        logger.debug("Got an adapter")
        logger.debug(f"message: {message}")
        adapter_holder = adapter

callback_info = wgpu.RequestAdapterCallbackInfo(
    # mode=wgpu.CallbackMode.ALLOW_PROCESS_EVENTS,
    mode=wgpu.CallbackMode.WAIT_ANY_ONLY,
    callback=on_adapter_request,
)

print(type(callback_info))
print(callback_info.__class__.__module__, callback_info.__class__.__qualname__)