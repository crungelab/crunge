from typing import Annotated, Generic, TypeVar, Type, Iterator, List
import ctypes

from loguru import logger

from crunge import wgpu
from crunge.core import as_capsule
from .buffer import Buffer

# TODO: Generics may be a waste of time for ctypes.  It can't even handle the type hinting.

# Define a TypeVar that must be a subclass of ctypes.Structure
TDataType = TypeVar("TDataType", bound=ctypes.Structure)


class CtypesBuffer(Buffer, Generic[TDataType]):
    def __init__(
        self,
        # data_type: ctypes.Structure,
        data_type: Type[TDataType],
        count: int,
        usage: wgpu.BufferUsage = None,
        label: str = None,
    ) -> None:
        self.data_type = data_type
        self.count = count
        # self.data = (data_type * count)()
        self.data: ctypes.Array[TDataType] = (data_type * count)()
        # logger.debug(f"Creating ctypes buffer for {data_type} x {count}")
        # logger.debug(f"Size of data type: {ctypes.sizeof(data_type)}")
        size = ctypes.sizeof(data_type) * count
        # logger.debug(f"size: {size}")
        # logger.debug(f"data: {self.data}")
        self.dirty = False
        super().__init__(size, usage, label)

    # List-like behavior
    def __len__(self) -> int:
        return self.count

    def __getitem__(self, index: int) -> TDataType:
        if isinstance(index, slice):
            return [self.data[i] for i in range(*index.indices(self.count))]
        if index < 0 or index >= self.count:
            raise IndexError("Index out of range")
        return self.data[index]

    def __setitem__(self, index: int, value: TDataType) -> None:
        if not isinstance(value, self.data_type):
            raise ValueError("Value must be of type {}".format(self.data_type))
        if index < 0 or index >= self.count:
            raise IndexError("Index out of range")
        self.data[index] = value
        self.dirty = True
        # self.upload()
        #logger.debug(f"Uploading {self.data} to buffer")
        self.device.queue.write_buffer(
            self.buffer,
            index * ctypes.sizeof(self.data_type),
            #as_capsule(self.data),
            as_capsule(value),
            ctypes.sizeof(self.data_type)
        )

    def __iter__(self) -> Iterator[TDataType]:
        return iter(self.data)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(data_type={self.data_type}, count={self.count}, size={self.size}, usage={self.usage}, label={self.label})"

    """
    def update_data(self, index, new_data):
        if not isinstance(new_data, self.data_type):
            raise ValueError("new_data must be of type {}".format(self.data_type))
        self.data[index] = new_data
    """

    '''
    def upload(self) -> None:
        """
        Upload the data to the GPU buffer.
        """
        logger.debug(f"Uploading {self.data} to buffer")
        self.device.queue.write_buffer(
            self.buffer,
            0,
            as_capsule(self.data),
            self.size,
        )
        self.dirty = False
    '''

class UniformBuffer(CtypesBuffer[TDataType], Generic[TDataType]):
    def __init__(
        self,
        # data_type: ctypes.Structure,
        data_type: Type[TDataType],
        count: int,
        usage: wgpu.BufferUsage = wgpu.BufferUsage.UNIFORM,
        label: str = None,
    ) -> None:
        super().__init__(data_type, count, usage, label)
