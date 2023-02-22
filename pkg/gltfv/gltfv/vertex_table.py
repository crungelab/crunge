import numpy as np

from .vertex_column import VertexColumn


class VertexTable:
    columns: list[VertexColumn]

    def __init__(self) -> None:
        self.columns = []

    def add_column(self, column):
        self.columns.append(column)

    def has(self, name):
        return name in self.columns

    @property
    def count(self):
        return len(self.columns)

    @property
    def data(self):
        return np.concatenate([x.data for x in self.columns], axis=1)
    
    @property
    def vertex_size(self):
        return sum([x.struct_size for x in self.columns])