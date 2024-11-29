from ..service import Service
from ..view import View


class Channel(Service):
    def produce_view(self) -> View:
        raise NotImplementedError