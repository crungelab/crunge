import ctypes

from crunge import wgpu


def create_buffer_from_memory(device: wgpu.Device, data: memoryview, size:int, usage: wgpu.BufferUsage) -> wgpu.Buffer:
    descriptor = wgpu.BufferDescriptor()
    descriptor.size = size
    descriptor.usage = usage | wgpu.BufferUsage.COPY_DST
    buffer: wgpu.Buffer = device.create_buffer(descriptor)
    device.queue.write_buffer(buffer, 0, data, size)
    return buffer