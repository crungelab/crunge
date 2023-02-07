import ctypes

from crunge import wgpu


def create_buffer_from_data(device: wgpu.Device, data: ctypes.py_object, size:int, usage: wgpu.BufferUsage) -> wgpu.Buffer:
    descriptor = wgpu.BufferDescriptor()
    descriptor.size = size
    descriptor.usage = usage | wgpu.BufferUsage.COPY_DST
    buffer: wgpu.Buffer = device.create_buffer(descriptor)
    return buffer