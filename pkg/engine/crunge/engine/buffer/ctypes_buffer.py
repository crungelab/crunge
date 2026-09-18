from typing import Generic, TypeVar, Type, Iterator
import ctypes

from loguru import logger

from crunge import wgpu
from .buffer import Buffer

# TODO: Generics may be a waste of time for ctypes.  It can't even handle the type hinting.

TDataType = TypeVar("TDataType", bound=ctypes.Structure)


class CtypesBuffer(Buffer, Generic[TDataType]):
    """A GPU buffer with a host-side ctypes array shadowing it.

    The host copy is what makes growth cheap to get right: the new GPU
    buffer is filled from it, so nothing has to be read back and no data is
    lost across a resize.
    """

    MIN_COUNT = 8

    def __init__(
        self,
        data_type: Type[TDataType],
        count: int,
        usage: wgpu.BufferUsage = None,
        label: str = None,
    ) -> None:
        self.data_type = data_type
        self.stride = ctypes.sizeof(data_type)
        self.count = count
        self.data: ctypes.Array[TDataType] = (data_type * count)()
        super().__init__(self.stride * count, usage, label)

    # -- growth ------------------------------------------------------------

    def ensure(self, count: int) -> bool:
        """Make room for at least `count` elements. Returns whether the
        buffer grew — and therefore whether bind groups over it are stale.

        Call before writing an index at or past `count`. A group appending
        its nth member calls ensure(n + 1) rather than checking capacity and
        raising.
        """
        if count <= self.count:
            return False

        new_count = max(count, int(self.count * self.GROWTH_FACTOR), self.MIN_COUNT)

        old_data = self.data
        old_count = self.count

        self.count = new_count
        self.data = (self.data_type * new_count)()
        ctypes.memmove(self.data, old_data, self.stride * old_count)

        # resize() reallocates the GPU buffer, calls _on_resized to refill
        # it from the array above, then fires `resized` so bind groups get
        # rebuilt. The host array has to be grown and copied first, or the
        # refill writes the old contents into the new buffer.
        self.resize(self.stride * new_count)
        return True

    def _on_resized(self) -> None:
        self.upload()

    def upload(self) -> None:
        """Write the whole host array. Used after a resize; a single element
        write goes through __setitem__ instead."""
        self.device.queue.write_buffer(self.buffer, 0, self.data)

    # -- list-like behaviour -----------------------------------------------

    def __len__(self) -> int:
        return self.count

    def __getitem__(self, index: int) -> TDataType:
        if isinstance(index, slice):
            return [self.data[i] for i in range(*index.indices(self.count))]
        if index < 0 or index >= self.count:
            raise IndexError(
                f"{self.label}: index {index} out of range for {self.count} "
                f"elements"
            )
        return self.data[index]

    def __setitem__(self, index: int, value: TDataType) -> None:
        if not isinstance(value, self.data_type):
            raise ValueError("Value must be of type {}".format(self.data_type))
        if index < 0 or index >= self.count:
            # Does not grow implicitly. A write past the end is almost
            # always a slot that was never allocated rather than a request
            # for more room, and growing here would hide it — and fire
            # `resized` from inside a flush, where a listener rebuilding a
            # bind group is the last thing anyone expects.
            raise IndexError(
                f"{self.label}: index {index} out of range for {self.count} "
                f"elements; call ensure({index + 1}) first"
            )
        self.data[index] = value
        self.device.queue.write_buffer(self.buffer, index * self.stride, value)

    def __iter__(self) -> Iterator[TDataType]:
        return iter(self.data)

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}(data_type={self.data_type}, "
            f"count={self.count}, size={self.size}, usage={self.usage}, "
            f"label={self.label})"
        )


class UniformBuffer(CtypesBuffer[TDataType], Generic[TDataType]):
    def __init__(
        self,
        data_type: Type[TDataType],
        count: int,
        usage: wgpu.BufferUsage = wgpu.BufferUsage.UNIFORM,
        label: str = None,
    ) -> None:
        super().__init__(data_type, count, usage, label)