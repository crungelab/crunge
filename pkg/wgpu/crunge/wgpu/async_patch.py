from loguru import logger

#from . import wgpu
from . import _wgpu as wgpu

def _Instance_request_adapter_sync(self: wgpu.Instance, options: wgpu.RequestAdapterOptions) -> wgpu.Adapter:
    # 2) Holder for the adapter we'll receive in the callback
    adapter_holder = None

    # 3) Define the callback exactly like the C++ lambda did
    def on_adapter_request(
        status: wgpu.RequestAdapterStatus, adapter: wgpu.Adapter, message: str
    ):
        logger.debug("on_adapter_request called")
        nonlocal adapter_holder

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

    # 5) Kick off the async request
    future = self._request_adapter(options, callback_info)

    # 6) Block until the callback fires (or timeout)
    wait_info = wgpu.FutureWaitInfo(future=future, completed=False)
    # UINT64_MAX for no real timeout:
    self.wait_any([wait_info], 0xFFFFFFFFFFFFFFFF)
    # 7) Pull the adapter out and return it (or None on failure)
    return adapter_holder

wgpu.Instance.request_adapter_sync = _Instance_request_adapter_sync