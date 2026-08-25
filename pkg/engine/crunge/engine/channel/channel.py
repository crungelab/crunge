from ..factory import Factory
from ..display import Display


class Channel:
    def __init__(
        self,
        display_factory: Factory[Display],
        name: str,
        title: str = None,
        next_channel: str = None,
    ) -> None:
        super().__init__()
        self.display_factory = display_factory
        self.name = name
        self.title = title if title is not None else name
        self.next_channel = next_channel

    def __call__(self, *args, **kwargs) -> Display:
        return self.produce_display(*args, **kwargs)

    def produce_display(self, *args, **kwargs) -> Display:
        return self.display_factory(*args, **kwargs)
