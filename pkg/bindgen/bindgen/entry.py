from crunge.clang import cindex

class Entry:
    key: str = None
    config: dict = {}
    node: cindex.Cursor = None

    exclude: bool = False
    overload: bool = False

    def __init__(self, key: str, config: dict={}, node: cindex.Cursor = None):
        self.key = key
        self.configure(config)
        self.node = node

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
    gen_init: bool = False
    gen_kw_init: bool = False

class StructEntry(StructOrClassEntry):
    pass

class ClassEntry(StructOrClassEntry):
    pass
