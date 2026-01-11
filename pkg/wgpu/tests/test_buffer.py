import numpy as np

from loguru import logger

from crunge import wgpu


indices = np.array([0, 1, 2, 3, 7, 1, 5, 0, 4, 2, 6, 7, 4, 5,], dtype=np.uint16)
size = indices.nbytes
logger.debug(size)
usage = wgpu.BufferUsage.INDEX

def main():
    wgpu_context = wgpu.Context()
    device = wgpu_context.device

    descriptor = wgpu.BufferDescriptor(size=size, usage=usage | wgpu.BufferUsage.COPY_DST)
    #descriptor.size = size
    #descriptor.usage = usage | wgpu.BufferUsage.COPY_DST
    buffer: wgpu.Buffer = device.create_buffer(descriptor)
    logger.debug(buffer)

    device.queue.write_buffer(buffer, 0, indices)

if __name__ == "__main__":
    main()