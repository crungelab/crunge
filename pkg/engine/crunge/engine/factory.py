from typing import TYPE_CHECKING, TypeVar, Generic, Dict, List, Callable, Any


T_Type = TypeVar("T_Type")


class Factory(Generic[T_Type]):
    def __init__(self) -> None:
        super().__init__()

    def __call__(self, *args, **kwargs) -> T_Type:
        return self.produce(*args, **kwargs)

    def produce(self) -> T_Type:
        raise NotImplementedError


class ClassFactory(Factory, Generic[T_Type]):
    def __init__(self, klass: T_Type) -> None:
        super().__init__()
        self.klass = klass

    '''
    def __call__(self, *args, **kwargs) -> T_Type:
        return self.produce(*args, **kwargs)
    '''

    def produce(self, *args, **kwargs) -> T_Type:
        return self.klass(*args, **kwargs)


class ImportFactory(Factory, Generic[T_Type]):
    def __init__(self, module: str, name: str) -> None:
        super().__init__()
        self.module = module
        self.name = name

    '''
    def __call__(self, *args, **kwargs) -> T_Type:
        return self.produce(*args, **kwargs)
    '''

    def produce(self, *args, **kwargs) -> T_Type:
        import importlib.util

        spec = importlib.util.find_spec(self.module)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return getattr(module, self.name)(*args, **kwargs)
