from crunge.engine.factory import ClassFactory
from crunge.engine.channel import Channel

from .page import Page


class PageChannel(Channel):
    def __init__(self, klass: type[Page], name: str, title: str = None):
        super().__init__(ClassFactory(klass), name, title)

    def produce_view(self, *args, **kwargs) -> Page:
        return super().produce_view(self.name, self.title, *args, **kwargs)
