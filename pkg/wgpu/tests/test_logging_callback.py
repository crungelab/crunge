from crunge import wgpu
from crunge.wgpu import BackendType
from crunge.wgpu import utils

class DeviceLostCallbackInfo:
    def __init__(self, callback, mode):
        self.callback = callback
        self.mode = mode

class LoggingCallbackInfo:
    def __init__(self, callback):
        self.callback = callback

def main():
    instance = utils.create_instance()
    adapter = instance.request_adapter()

    def device_cb(device, reason, message):
        print("Device lost: ", reason, message)

    device_lost_callback_info = DeviceLostCallbackInfo(device_cb, wgpu.CallbackMode.ALLOW_PROCESS_EVENTS)
    device_desc = wgpu.DeviceDescriptor(device_lost_callback_info=device_lost_callback_info)

    device = adapter.create_device(device_desc)
    cb = lambda info: print(info)
    cbinfo = LoggingCallbackInfo(cb)
    device.set_logging_callback(cbinfo)
    #device.enable_logging()
    print(device)

if __name__ == "__main__":
    main()