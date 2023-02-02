import sys
import setuptools
from skbuild import setup

setup(
    name             = 'crunge',
    description      = 'Creative Coding Extensions',
    version          = '0.1.0',
    url              = 'http://github.com/crungelab/crunge',
    license          = 'MIT',
    author           = 'kfields',
    packages         = setuptools.find_packages(exclude=[".bindgen"]),
)
