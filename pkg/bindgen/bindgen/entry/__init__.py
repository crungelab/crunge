class Entry:
    exclude: bool = False
    overload: bool = False

    def __init__(self, key, config):
        self.key = key
        self.configure(config)

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} key={self.key}>'

    def configure(self, config):
        #logger.debug(f"config: {config}")
        for key, value in config.items():
            setattr(self, key, value)

class FunctionEntry(Entry):
    pass

class CtorEntry(Entry):
    pass

class FieldEntry(Entry):
    pass

class MethodEntry(Entry):
    pass

class StructOrClassEntry(Entry):
    constructible: bool = True
    has_constructor: bool = False

class StructEntry(StructOrClassEntry):
    pass

class ClassEntry(StructOrClassEntry):
    pass
