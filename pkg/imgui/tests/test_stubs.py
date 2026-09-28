"""Check the generated _imgui.pyi against the built extension module.

Fails when the stub and the runtime disagree: a regenerated stub that no
longer matches, or a hand-written binding in imgui_py.cpp that isn't
declared in the stub (see the `stub:` specs and _imgui.pyi.j2).

Run after building: stubtest imports the compiled module.
"""

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

MODULE = "crunge.imgui._imgui"

# pkg/imgui/tests/test_stubs.py -> pkg/imgui
PKG_DIR = Path(__file__).resolve().parents[1]
ALLOWLIST = Path(__file__).resolve().parent / "stubtest_allowlist.txt"

def _importable(name: str) -> bool:
    try:
        return importlib.util.find_spec(name) is not None
    except ModuleNotFoundError:
        return False


@unittest.skipUnless(_importable("mypy"), "mypy is not installed")
@unittest.skipUnless(_importable(MODULE), f"{MODULE} is not built")
class TestStubs(unittest.TestCase):
    def test_stubtest(self):
        command = [sys.executable, "-m", "mypy.stubtest", MODULE, "--concise"]
        if ALLOWLIST.exists():
            command += ["--allowlist", str(ALLOWLIST)]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            cwd=PKG_DIR,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()