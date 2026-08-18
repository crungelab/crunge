# tests/spine/__init__.py

from crunge.engine.resource.resource_manager import ResourceManager


def create_spine_path(name: str, version: str = "ess", ext: str = "json") -> str:
    if version == "":
        return f"${{spines}}/{name}/export/{name}.{ext}"
    return f"${{spines}}/{name}/export/{name}-{version}.{ext}"

def resolve_spine_path(name: str, version: str = "ess", ext: str = "json") -> str:
    path = create_spine_path(name, version, ext)
    return ResourceManager().resolve_path(path)