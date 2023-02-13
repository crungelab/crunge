from enum import Enum

from crunge.clang import cindex

"""
entry_cls_map = {
    'function': FunctionEntry,
    'ctor': CtorEntry,
    'field': FieldEntry,
    'method': MethodEntry,
    'struct': StructEntry,
    'class': ClassEntry
}
"""
class EntryKind(Enum):
    FUNCTION = 0
    CTOR = 1
    FIELD = 2
    METHOD = 3
    STRUCT = 4
    CLASS = 5

class Entry:
    fqname: str = None
    name: str = None
    pyname: str = None
    config: dict = {}
    node: cindex.Cursor = None
    children: list["Entry"] = []
    exclude: bool = False
    overload: bool = False

    def __init__(self, fqname: str, name: str, pyname: str, config: dict={}, node: cindex.Cursor = None):
        self.fqname = fqname
        self.name = name
        self.pyname = pyname
        self.configure(config)
        self.node = node
        self.children = []

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} fqname={self.fqname}, name={self.name}, pyname={self.pyname}>'

    def configure(self, config):
        #logger.debug(f"config: {config}")
        for key, value in config.items():
            setattr(self, key, value)

    def add_child(self, entry: "Entry"):
        self.children.append(entry)

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
