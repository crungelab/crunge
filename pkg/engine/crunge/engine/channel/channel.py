from ..factory import Factory
from ..view import View


class Channel:
    def __init__(
        self,
        view_factory: Factory[View],
        name: str,
        title: str = None,
        next_channel: str = None,
    ) -> None:
        super().__init__()
        self.view_factory = view_factory
        self.name = name
        self.title = title if title is not None else name
        self.next_channel = next_channel

    def __call__(self, *args, **kwargs) -> View:
        return self.produce_view(*args, **kwargs)

    def produce_view(self, *args, **kwargs) -> View:
        return self.view_factory(*args, **kwargs)


"""
class Channel:
    def __init__(self, view_factory: Factory[View], name: str, title: str = None, next_channel: str = None) -> None:
        super().__init__()
        self.view_factory = view_factory
        self.name = name
        self.title = title if title is not None else name
        self.next_channel = next_channel

    def __call__(self, *args, **kwargs) -> View:
        return self.produce_view(self.name, self.title, *args, **kwargs)
    
    def produce_view(self, *args, **kwargs) -> View:
        return self.view_factory(*args, **kwargs)
"""
