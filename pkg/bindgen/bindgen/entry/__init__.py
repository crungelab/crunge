class Entry:
    exclude: bool = False
    overload: bool = False

    def __init__(self, config):
        self.configure(config)

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

class StructEntry(Entry):
    pass

entry_map = {
    'function': FunctionEntry,
    'ctor': CtorEntry,
    'field': FieldEntry,
    'method': MethodEntry,
    'struct': StructEntry
}

registry = {}

def create_entry(key, value):
    s = key.split('.')
    cls = entry_map[s[0]]
    entry = cls(value)
    registry[s[1]] = entry
    return entry