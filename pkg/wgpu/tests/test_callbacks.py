from crunge import wgpu
from crunge.wgpu import utils


class DeviceLostCallbackInfo:
    def __init__(self, callback, mode):
        self.callback = callback
        self.mode = mode


class UncapturedErrorCallbackInfo:
    def __init__(self, callback):
        self.callback = callback


class LoggingCallbackInfo:
    def __init__(self, callback):
        self.callback = callback


def main():
    instance = utils.create_instance()
    adapter = instance.request_adapter()

    def device_cb(device, reason, message):
        print("Device lost: ", reason, message)

    device_lost_callback_info = DeviceLostCallbackInfo(
        device_cb, wgpu.CallbackMode.ALLOW_PROCESS_EVENTS
    )

    def uncaptured_error_cb(device, type, message):
        print("Uncaptured error: ", type, message)

    uncaptured_error_callback_info = UncapturedErrorCallbackInfo(uncaptured_error_cb)

    device_desc = wgpu.DeviceDescriptor(
        device_lost_callback_info=device_lost_callback_info,
        uncaptured_error_callback_info=uncaptured_error_callback_info,
    )

    device = adapter.create_device(device_desc)
    cb = lambda info: print(info)
    cbinfo = LoggingCallbackInfo(cb)
    device.set_logging_callback(cbinfo)

    print(device)


if __name__ == "__main__":
    main()
