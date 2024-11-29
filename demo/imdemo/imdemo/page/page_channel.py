from crunge.engine.factory import ClassFactory
from crunge.engine.channel import Channel

from .page import Page


class PageChannel(Channel):
    def __init__(self, klass: type[Page], name, title = None):
        super().__init__(ClassFactory(klass), name, title)
