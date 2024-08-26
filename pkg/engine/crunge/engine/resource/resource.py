class Resource:
    def __init__(self, name: str, path: str):
        self.name = name
        self.path = path

    def __str__(self):
        return f"Resource(name={self.name}, path={self.path})"

    def __repr__(self):
        return str(self)

    def __eq__(self, other):
        return self.name == other.name and self.path == other.path

    def __hash__(self):
        return hash((self.name, self.path))