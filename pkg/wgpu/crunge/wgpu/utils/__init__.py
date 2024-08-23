import ctypes
import numpy as np

from crunge import wgpu
from crunge.wgpu.constants import *
from crunge.core import as_capsule


def divround_down(value, step):
    return value // step * step


def divround_up(value, step):
    return (value + step - 1) // step * step


def create_buffer(
    device: wgpu.Device, label: str, size: int, usage: wgpu.BufferUsage
) -> wgpu.Buffer:
    # Buffer size has to be a multiple of 4
    size = divround_up(size, 4)
    desc = wgpu.BufferDescriptor()
    desc.label = label
    desc.usage = usage | wgpu.BufferUsage.COPY_DST
    desc.size = size
    return device.create_buffer(desc)


def write_buffer(
    device: wgpu.Device, buffer: wgpu.Buffer, offset: int, data: object, size: int
) -> None:
    # Buffer size has to be a multiple of 4
    size = divround_up(size, 4)
    device.queue.write_buffer(buffer, offset, as_capsule(data), size)


def create_buffer_from_ndarray(
    device: wgpu.Device, label: str, data: np.ndarray, usage: wgpu.BufferUsage
) -> wgpu.Buffer:
    size = data.nbytes
    # Buffer size has to be a multiple of 4
    size = divround_up(size, 4)
    buffer = create_buffer(device, label, size, usage)
    device.queue.write_buffer(buffer, 0, as_capsule(data), size)
    return buffer


def write_buffer_from_ndarray(
    device: wgpu.Device, buffer: wgpu.Buffer, data: np.ndarray
) -> None:
    size = data.nbytes
    # Buffer size has to be a multiple of 4
    size = divround_up(size, 4)
    device.queue.write_buffer(buffer, 0, as_capsule(data), size)


def create_buffer_from_ctypes_array(
    device: wgpu.Device, label: str, data: ctypes.Array, usage: wgpu.BufferUsage
) -> wgpu.Buffer:
    # Calculate the size of the ctypes array
    item_size = ctypes.sizeof(data._type_)
    total_size = len(data) * item_size
    # Buffer size has to be a multiple of 4
    size = divround_up(total_size, 4)

    # Create the buffer
    buffer = create_buffer(device, label, size, usage)

    # Get a pointer to the array data
    ptr = as_capsule(data)

    # Write the data to the buffer
    device.queue.write_buffer(buffer, 0, ptr, size)

    return buffer


def write_buffer_from_ctypes_array(
    device: wgpu.Device, buffer: wgpu.Buffer, data: ctypes.Array
) -> None:
    # Calculate the size of the ctypes array
    item_size = ctypes.sizeof(data._type_)
    total_size = len(data) * item_size
    # Buffer size has to be a multiple of 4
    size = divround_up(total_size, 4)

    # Get a pointer to the array data
    ptr = as_capsule(data)

    # Write the data to the buffer
    device.queue.write_buffer(buffer, 0, ptr, size)


def create_image_copy_buffer(
    buffer: wgpu.Buffer,
    offset: int,
    bytes_per_row: int = WGPU_COPY_STRIDE_UNDEFINED,
    rows_per_image: int = WGPU_COPY_STRIDE_UNDEFINED,
) -> wgpu.ImageCopyBuffer:
    image_copy_buffer = wgpu.ImageCopyBuffer()
    image_copy_buffer.buffer = buffer
    image_copy_buffer.layout = create_texture_data_layout(
        offset, bytes_per_row, rows_per_image
    )

    return image_copy_buffer


def create_image_copy_texture(
    texture: wgpu.Texture,
    mip_level: int = 0,
    origin: wgpu.Origin3D = wgpu.Origin3D(0, 0, 0),
    aspect: wgpu.TextureAspect = wgpu.TextureAspect.ALL,
) -> wgpu.ImageCopyTexture:
    image_copy_texture = wgpu.ImageCopyTexture()
    image_copy_texture.texture = texture
    image_copy_texture.mip_level = mip_level
    image_copy_texture.origin = origin
    image_copy_texture.aspect = aspect

    return image_copy_texture


def create_shader_module(device: wgpu.Device, source: str) -> wgpu.ShaderModule:
    wgsl_desc = wgpu.ShaderModuleWGSLDescriptor()
    wgsl_desc.code = source
    descriptor = wgpu.ShaderModuleDescriptor()
    descriptor.next_in_chain = wgsl_desc
    return device.create_shader_module(descriptor)


def create_texture_data_layout(
    offset: int, bytes_per_row: int, rows_per_image: int
) -> wgpu.TextureDataLayout:
    texture_data_layout = wgpu.TextureDataLayout()
    texture_data_layout.offset = offset
    texture_data_layout.bytes_per_row = bytes_per_row
    texture_data_layout.rows_per_image = rows_per_image

    return texture_data_layout


def create_texture(
    device: wgpu.Device,
    label: str,
    extent: wgpu.Extent3D,
    format: wgpu.TextureFormat,
    usage: wgpu.TextureUsage,
):
    descriptor = wgpu.TextureDescriptor()
    descriptor.label = label
    descriptor.size = extent
    descriptor.format = format
    descriptor.usage = usage
    texture = device.create_texture(descriptor)
    return texture
