# tests/conftest.py
import pytest
from pathlib import Path
from crunge.engine.resource.resource_manager import ResourceManager


def _find_repo_root(start: Path, marker=".git") -> Path:
    """Walk upward from `start` until a directory containing `marker` is found."""
    current = start.resolve()
    for candidate in (current, *current.parents):
        if (candidate / marker).exists():
            return candidate
    raise RuntimeError(f"Could not find repo root above {start} (looked for {marker!r})")


REPO_ROOT = _find_repo_root(Path(__file__))
RESOURCE_ROOT = REPO_ROOT / "resources"
DEPOT_ROOT = REPO_ROOT / "depot"
SPINE_ROOT = DEPOT_ROOT / "spine-runtimes"


@pytest.fixture(scope="session", autouse=True)
def _configure_resource_manager():
    ResourceManager().add_path_variables(
        resources=RESOURCE_ROOT,
        images=RESOURCE_ROOT / "images",
        spines=SPINE_ROOT / "examples",
    )


@pytest.fixture(autouse=True)
def _resource_paths(request):
    """Mirror the paths onto self for tests that want self.repo_root etc."""
    if request.instance is not None:
        request.instance.repo_root = REPO_ROOT
        request.instance.resource_root = RESOURCE_ROOT
        request.instance.depot_root = DEPOT_ROOT
        request.instance.spine_root = SPINE_ROOT