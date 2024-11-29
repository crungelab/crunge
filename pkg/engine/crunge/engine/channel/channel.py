from ..factory import Factory
from ..view import View


class Channel:
    def __init__(self, view_factory: Factory[View], name: str, title: str = None) -> None:
        super().__init__()
        self.name = name
        self.title = title if title is not None else name
        self.view_factory = view_factory

    def __call__(self, *args, **kwargs) -> View:
        return self.produce_view(self.name, self.title, *args, **kwargs)
    
    def produce_view(self, *args, **kwargs) -> View:
        return self.view_factory(*args, **kwargs)