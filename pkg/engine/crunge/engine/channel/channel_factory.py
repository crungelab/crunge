from .channel import Channel


class ChannelFactory:
    def __init__(self, name: str, title: str = None) -> None:
        self.name = name
        self.title = title if title is not None else name

    def __call__(self, *args, **kwargs):
        #return self.klass(*args, **kwargs)
        return self.produce(*args, **kwargs)
    
    def produce(self):
        #return self.klass()
        raise NotImplementedError
    

class ClassChannelFactory(ChannelFactory):
    #def __init__(self, name: str, klass: type[Channel]) -> None:
    def __init__(self, klass: type[Channel], name: str, title: str = None) -> None:
        super().__init__(name, title)
        self.klass = klass

    def __call__(self, *args, **kwargs):
        #return self.klass(*args, **kwargs)
        #return self.produce(*args, **kwargs)
        return self.produce(self.name, self.title, *args, **kwargs)
    
    def produce(self, *args, **kwargs):
        return self.klass(*args, **kwargs)