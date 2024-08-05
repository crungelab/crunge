import numpy as np

from .vertex_column import VertexColumn


class VertexTable:
    columns: list[VertexColumn]

    def __init__(self) -> None:
        self.columns = []
        self.column_map = {}

    def add_column(self, column):
        column.location = len(self.columns)
        self.columns.append(column)
        self.column_map[column.name] = column

    def has(self, name):
        return name in self.column_map
    
    def get(self, name):
        return self.column_map[name]

    @property
    def count(self):
        return len(self.columns)

    @property
    def data(self):
        return np.concatenate([x.data for x in self.columns], axis=1)
        '''
        # Debugging output: Print the sizes of the arrays
        for i, column in enumerate(self.columns):
            print(f"Array {i} size: {column.data.shape}")

        # Find the minimum size along axis 0 to which all arrays will be truncated
        min_size = min(column.data.shape[0] for column in self.columns)

        # Truncate all arrays to the same size
        truncated_columns = [column.data[:min_size] for column in self.columns]

        # Concatenate the truncated arrays
        return np.concatenate(truncated_columns, axis=1)
        '''
    @property
    def vertex_size(self):
        return sum([x.struct_size for x in self.columns])
    
    @property
    def has_color(self):
        return self.has('color')
    
    @property
    def has_uv(self):
        return self.has('uv')