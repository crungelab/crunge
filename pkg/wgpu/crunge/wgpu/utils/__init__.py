import ctypes
import numpy as np

from crunge import wgpu
from crunge.wgpu.constants import *
from crunge.core import as_capsule

# def create_buffer_from_ndarray(device: wgpu.Device, data: np.ndarray, size:int, usage: wgpu.BufferUsage) -> wgpu.Buffer:
def create_buffer_from_ndarray(
    device: wgpu.Device, data: np.ndarray, usage: wgpu.BufferUsage
) -> wgpu.Buffer:
    size = data.nbytes
    descriptor = wgpu.BufferDescriptor()
    descriptor.size = size
    descriptor.usage = usage | wgpu.BufferUsage.COPY_DST
    buffer: wgpu.Buffer = device.create_buffer(descriptor)
    device.queue.write_buffer(buffer, 0, as_capsule(data), size)
    return buffer


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
    wgsl_desc.source = source
    descriptor = wgpu.ShaderModuleDescriptor()
    descriptor.next_in_chain = wgsl_desc
    return device.create_shader_module(descriptor)

def make_bind_group_layout(device: wgpu.Device, initializers: list[tuple[3]]):
    entries = wgpu.BindGroupLayoutEntries()
    for inizer in initializers:
        entry = wgpu.BindGroupLayoutEntry()
        entry.
        entries.append(entry)

"""
struct BindGroupLayoutEntry {
    ChainedStruct const * nextInChain = nullptr;
    uint32_t binding;
    ShaderStage visibility;
    BufferBindingLayout buffer;
    SamplerBindingLayout sampler;
    TextureBindingLayout texture;
    StorageTextureBindingLayout storageTexture;
};
"""

"""
wgpu::BindGroupLayout MakeBindGroupLayout(
    const wgpu::Device& device,
    std::initializer_list<BindingLayoutEntryInitializationHelper> entriesInitializer) {
    std::vector<wgpu::BindGroupLayoutEntry> entries;
    for (const BindingLayoutEntryInitializationHelper& entry : entriesInitializer) {
        entries.push_back(entry);
    }

    wgpu::BindGroupLayoutDescriptor descriptor;
    descriptor.entryCount = static_cast<uint32_t>(entries.size());
    descriptor.entries = entries.data();
    return device.CreateBindGroupLayout(&descriptor);
}
"""
"""
wgpu::ShaderModule CreateShaderModule(const wgpu::Device& device, const char* source) {
    wgpu::ShaderModuleWGSLDescriptor wgslDesc;
    wgslDesc.source = source;
    wgpu::ShaderModuleDescriptor descriptor;
    descriptor.nextInChain = &wgslDesc;
    return device.CreateShaderModule(&descriptor);
}

"""
"""
wgpu::ImageCopyTexture CreateImageCopyTexture(wgpu::Texture texture,
                                              uint32_t mipLevel,
                                              wgpu::Origin3D origin,
                                              wgpu::TextureAspect aspect) {
    wgpu::ImageCopyTexture imageCopyTexture;
    imageCopyTexture.texture = texture;
    imageCopyTexture.mipLevel = mipLevel;
    imageCopyTexture.origin = origin;
    imageCopyTexture.aspect = aspect;

    return imageCopyTexture;
}
"""

"""
wgpu::ImageCopyBuffer CreateImageCopyBuffer(wgpu::Buffer buffer,
                                            uint64_t offset,
                                            uint32_t bytesPerRow,
                                            uint32_t rowsPerImage) {
    wgpu::ImageCopyBuffer imageCopyBuffer = {};
    imageCopyBuffer.buffer = buffer;
    imageCopyBuffer.layout = CreateTextureDataLayout(offset, bytesPerRow, rowsPerImage);

    return imageCopyBuffer;
}
"""


def create_texture_data_layout(
    offset: int, bytes_per_row: int, rows_per_image: int
) -> wgpu.TextureDataLayout:
    texture_data_layout = wgpu.TextureDataLayout()
    texture_data_layout.offset = offset
    texture_data_layout.bytes_per_row = bytes_per_row
    texture_data_layout.rows_per_image = rows_per_image

    return texture_data_layout


"""
wgpu::TextureDataLayout CreateTextureDataLayout(uint64_t offset,
                                                uint32_t bytesPerRow,
                                                uint32_t rowsPerImage) {
    wgpu::TextureDataLayout textureDataLayout;
    textureDataLayout.offset = offset;
    textureDataLayout.bytesPerRow = bytesPerRow;
    textureDataLayout.rowsPerImage = rowsPerImage;

    return textureDataLayout;
}
"""
