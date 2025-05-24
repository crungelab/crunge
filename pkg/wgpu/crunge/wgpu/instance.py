import asyncio

from loguru import logger

from . import _wgpu as wgpu

wgpu.Instance._pending_futures = []

def _Instance__new__(cls, *args, **kwargs):
    if not hasattr(cls, '_instance'):
        # Create the instance capabilities
        capabilities = wgpu.InstanceCapabilities(timed_wait_any_enable=True)
        instance_descriptor = wgpu.InstanceDescriptor(capabilities=capabilities)

        # Create the actual instance
        instance = wgpu.create_instance(instance_descriptor)

        # Store the instance in the class attribute
        cls._instance = instance

    return cls._instance

wgpu.Instance.__new__ = _Instance__new__

def _Instance_request_adapter_sync(
    self: wgpu.Instance, options: wgpu.RequestAdapterOptions
) -> wgpu.Adapter:
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

async def _Instance_request_adapter_async(
    self: wgpu.Instance, options: wgpu.RequestAdapterOptions
) -> wgpu.Adapter:
    loop = asyncio.get_event_loop()
    py_future = loop.create_future()

    # 3) Define the callback exactly like the C++ lambda did
    def on_adapter_request(
        status: wgpu.RequestAdapterStatus, adapter: wgpu.Adapter, message: str
    ):
        logger.debug("on_adapter_request called")
        nonlocal py_future

        if status != wgpu.RequestAdapterStatus.SUCCESS:
            logger.debug(f"Failed to get an adapter: {message}")
        else:
            logger.debug("Got an adapter")
            logger.debug(f"message: {message}")
            py_future.set_result(adapter)

    callback_info = wgpu.RequestAdapterCallbackInfo(
        # mode=wgpu.CallbackMode.ALLOW_PROCESS_EVENTS,
        mode=wgpu.CallbackMode.WAIT_ANY_ONLY,
        callback=on_adapter_request,
    )

    # 5) Kick off the async request
    wgpu_future = self._request_adapter(options, callback_info)

    self._pending_futures.append(wgpu_future)

    return await py_future

wgpu.Instance.request_adapter_async = _Instance_request_adapter_async

def _Instance_process_futures(self: wgpu.Instance):
    wait_infos = [
        wgpu.FutureWaitInfo(future=future, completed=False)
        for future in self._pending_futures
    ]

    self.wait_any(wait_infos, 0xFFFFFFFFFFFFFFFF)

    for wait_info in wait_infos:
        if wait_info.completed:
            self._pending_futures.remove(wait_info.future)
            

wgpu.Instance.process_futures = _Instance_process_futures
