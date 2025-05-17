from loguru import logger

from crunge import wgpu
from crunge.wgpu.utils import divround_up

from ..base import Base


class Buffer(Base):
    def __init__(self, size: int, usage: wgpu.BufferUsage = None, label: str = None):
        """
        Base class for WebGPU buffers.

        :param device: The WebGPU device to use.
        :param size: The size of the buffer in bytes.
        :param usage: WebGPU buffer usage (e.g., uniform, vertex).
        :param label: Optional label for the buffer (string).
        """
        super().__init__()

        self.size = size
        self.usage = usage
        self.label = label

        # Create the WebGPU buffer
        #logger.debug(f"Creating buffer: {label}")
        size = divround_up(size, 4)
        #TODO: fix Dawny/CxBind's issue with c strings

        desc = wgpu.BufferDescriptor(
            label=label,
            size=size,
            usage=usage | wgpu.BufferUsage.COPY_DST,
            #mapped_at_creation=False,
        )

        #logger.debug(f"Buffer size: {size}")
        self.buffer = self.device.create_buffer(desc)
        #logger.debug(f"Buffer created: {label}")

    def upload(self):
        """
        Upload the data to the GPU buffer.
        """
        raise NotImplementedError("Must be implemented by subclasses.")

    def download_from_gpu(self):
        """
        Download data from the GPU buffer.
        """
        raise NotImplementedError("Must be implemented by subclasses.")

    def destroy(self):
        """
        Clean up the GPU buffer.
        """
        self.device.destroy_buffer(self.buffer)

    def get(self) -> wgpu.Buffer:
        return self.buffer
