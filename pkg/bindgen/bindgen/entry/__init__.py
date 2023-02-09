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

class FieldEntry(Entry):
    pass

class MethodEntry(Entry):
    pass

class StructEntry(Entry):
    pass