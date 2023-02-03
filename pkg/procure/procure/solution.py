import subprocess
from pathlib import Path

from .project import Project


class Solution(Project):
    def update(self):
        pass


class GitSolution(Solution):
    path = ""
    url = ""
    branch = ""

    def update(self):
        path = Path(self.path)
        if not path.exists():
            self.clone()
        else:
            self.pull()

    def clone(self):
        args = ["git", "clone"]
        if self.branch:
            args = args + ["-b", self.branch]
        args = args + [self.url, self.path]
        subprocess.run(args)

    def pull(self):
        path = Path(self.path)
        args = ["git", f"--git-dir={path / '.git'}", f"--work-tree={path}", "pull"]
        subprocess.run(args)
