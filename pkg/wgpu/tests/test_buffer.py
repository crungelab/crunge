from ctypes import Structure, c_float, c_uint32, c_uint16, sizeof, c_bool, c_int, c_void_p
import numpy as np

from loguru import logger

from crunge import wgpu
from crunge.wgpu import BackendType

from utils import as_void_ptr


indices = np.array([0, 1, 2, 3, 7, 1, 5, 0, 4, 2, 6, 7, 4, 5,], dtype=np.uint16)
data = as_void_ptr(indices)
size = len(indices) * sizeof(c_uint16)
logger.debug(size)
usage = wgpu.BufferUsage.INDEX

def main():
    instance = wgpu.create_instance()
    adapter = instance.request_adapter()
    props = wgpu.AdapterProperties()
    adapter.get_properties(props)
    logger.debug(props.vendor_name)
    device = adapter.create_device()
    logger.debug(device)
    device.enable_logging()

    queue = device.get_queue()

    descriptor = wgpu.BufferDescriptor()
    descriptor.size = size
    descriptor.usage = usage | wgpu.BufferUsage.COPY_DST
    buffer: wgpu.Buffer = device.create_buffer(descriptor)

    queue.write_buffer(buffer, 0, data, size)

if __name__ == "__main__":
    main()