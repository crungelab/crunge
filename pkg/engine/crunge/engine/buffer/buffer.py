from loguru import logger

from crunge import wgpu
from crunge.wgpu.utils import divround_up

from crunge.core.base import Base
from crunge.core.signal import Signal

from ..gfx_access import GfxAccess


class Buffer(GfxAccess, Base):
    """A WebGPU buffer that can grow.

    Growing means creating a new wgpu.Buffer — there is no realloc — so
    every bind group built over the old handle stops being valid. That is
    the whole difficulty: the resize itself is three lines, and telling
    everyone who referenced the old buffer is the rest.

    `resized` is how they find out. A holder connects once and rebuilds its
    bind group when it fires; a holder that doesn't connect will bind a
    buffer the pipeline no longer sees the data in, and nothing will say so.
    """

    # Doubling. The alternative to over-allocating is rebuilding every bind
    # group over the buffer, which is far more expensive than the memory.
    GROWTH_FACTOR = 2.0

    def __init__(self, size: int, usage: wgpu.BufferUsage = None, label: str = None):
        """
        :param size: The size of the buffer in bytes.
        :param usage: WebGPU buffer usage (e.g., uniform, vertex).
        :param label: Optional label for the buffer (string).
        """
        super().__init__()

        self.usage = usage
        self.label = label
        self.size = 0
        self.buffer: wgpu.Buffer = None

        # Emits self. Connect before anything builds a bind group over this.
        self.resized: Signal["Buffer"] = Signal()

        self._allocate(size)

    def _allocate(self, size: int) -> None:
        self.size = size

        # ASSUMPTION: divround_up rounds size UP to a multiple of 4. If it
        # is ceil(size / 4) — which the name also reads as — every buffer in
        # the engine is a quarter of its intended size, and this is the line
        # to check first.
        allocated = divround_up(size, 4)

        desc = wgpu.BufferDescriptor(
            label=self.label,
            size=allocated,
            usage=self.usage | wgpu.BufferUsage.COPY_DST,
        )
        self.buffer = self.device.create_buffer(desc)

    def resize(self, size: int) -> bool:
        """Grow to at least `size` bytes. Returns whether anything changed.

        Never shrinks. A smaller request is satisfied by the buffer already
        allocated, and shrinking would invalidate every bind group to
        reclaim memory nothing is short of.
        """
        if size <= self.size:
            return False

        old_size = self.size
        old_buffer = self.buffer

        self._allocate(size)

        # Deliberately not destroyed. A command buffer submitted this frame
        # may still reference it, and destroying a buffer in use is a
        # validation error. Dropping the reference lets Dawn's refcount
        # release it once nothing is reading.
        del old_buffer

        logger.debug(f"{self.label}: grew {old_size} -> {self.size} bytes")

        # Subclass restores contents first, so a listener rebuilding a bind
        # group sees a buffer with data in it rather than an empty one.
        self._on_resized()
        self.resized.emit(self)
        return True

    def grow_to_fit(self, size: int) -> bool:
        """Resize with the growth factor applied, so repeated appends do not
        reallocate every time."""
        if size <= self.size:
            return False
        return self.resize(max(size, int(self.size * self.GROWTH_FACTOR)))

    def _on_resized(self) -> None:
        """Restore the new buffer's contents. Subclasses that hold a host
        copy re-upload it here."""

    def upload(self):
        raise NotImplementedError("Must be implemented by subclasses.")

    def download_from_gpu(self):
        raise NotImplementedError("Must be implemented by subclasses.")

    def _destroy(self):
        self.device.destroy_buffer(self.buffer)

    def get(self) -> wgpu.Buffer:
        return self.buffer