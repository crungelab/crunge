from ..service import Service
from ..view import View


class Channel(Service):
    def __init__(self, name: str, title: str = None) -> None:
        self.name = name
        self.title = title if title is not None else name

    def __call__(self, *args, **kwargs) -> View:
        #return self.klass(*args, **kwargs)
        return self.produce(*args, **kwargs)
    
    def produce(self) -> View:
        #return self.klass()
        raise NotImplementedError
    

class ClassChannel(Channel):
    #def __init__(self, name: str, klass: type[Channel]) -> None:
    def __init__(self, klass: type[Channel], name: str, title: str = None) -> None:
        super().__init__(name, title)
        self.klass = klass

    def __call__(self, *args, **kwargs) -> View:
        #return self.klass(*args, **kwargs)
        #return self.produce(*args, **kwargs)
        return self.produce(self.name, self.title, *args, **kwargs)
    
    def produce(self, *args, **kwargs) -> View:
        return self.klass(*args, **kwargs)