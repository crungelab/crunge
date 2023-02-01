"""Build script."""

import shutil
from distutils import log as distutils_log
from pathlib import Path
from typing import Any, Dict

from skbuild import setup
import skbuild.constants
import setuptools

__all__ = ("build",)


def build(setup_kwargs: Dict[str, Any]) -> None:
    """Build C-extensions."""
    #skbuild.setup(**setup_kwargs, script_args=["build_ext"])
    setup(
        name             = 'crunge',
        description      = 'Creative Coding Extensions',
        version          = '0.1.0',
        url              = 'http://github.com/crungelab/crunge',
        license          = 'MIT',
        author           = 'kfields',
        packages         = setuptools.find_packages(exclude=[".bindgen"]),
        #package_data={'aimgui': ['*.so']},
        #ext_modules      = [module],
        #setup_requires   = ['pybind11', "wheel", "scikit-build", "cmake", "ninja"],
        #install_requires=INSTALL_REQUIRES,
    )

if __name__ == "__main__":
    build({})