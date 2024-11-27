from .map_builder import MapBuilder


class DefaultMapBuilder(MapBuilder):
    def __init__(self, context):
        super().__init__(context)
