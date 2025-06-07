import numpy as np

from .vertex_column import VertexColumn


def dtype_from_struct(struct_cls):
    return np.dtype(struct_cls)


class VertexTable:
    columns: list[VertexColumn]

    def __init__(self) -> None:
        self.columns = []
        self.column_map = {}

    def add_column(self, column: VertexColumn):
        column.location = len(self.columns)
        self.columns.append(column)
        self.column_map[column.name] = column

    def has(self, name: str):
        return name in self.column_map

    def get(self, name: str):
        return self.column_map[name]

    @property
    def count(self):
        return len(self.columns)

    @property
    def has_color(self):
        return self.has('color')

    @property
    def has_uv(self):
        return self.has('uv')

    @property
    def vertex_dtype(self) -> np.dtype:
        """Build combined structured dtype from ctypes.Structures."""
        fields = []
        for column in self.columns:
            struct_dtype = dtype_from_struct(column.struct)
            fields.append((column.name, struct_dtype))
        return np.dtype(fields)

    @property
    def vertex_count(self) -> int:
        return self.columns[0].data.shape[0] if self.columns else 0

    @property
    def interleaved(self) -> np.ndarray:
        """Preallocate and interleave structured vertex data."""
        dtype = self.vertex_dtype
        count = self.vertex_count
        buffer = np.empty(count, dtype=dtype)

        for column in self.columns:
            field_dtype = dtype_from_struct(column.struct)
            buffer[column.name] = column.data.view(field_dtype).reshape(count)

        return buffer

    @property
    def data(self) -> np.ndarray:
        """Return raw bytes view (uint8) suitable for GPU upload."""
        return self.interleaved.view(np.uint8).ravel()

    @property
    def vertex_size(self) -> int:
        """Size in bytes of one vertex."""
        return self.vertex_dtype.itemsize
