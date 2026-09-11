import os
import zipfile

from importlib.resources import files


def load(name: str):
    return files(__name__).joinpath(name).open("r", encoding="utf-8")

#assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../assets'))

def asset(name):
    return files(__name__).joinpath(name)

'''
assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../assets'))

def asset(filename):
    return os.path.join(assets_dir, filename)

def load(filename, mode='r'):
    return open(os.path.join(assets_dir, filename), mode)

def load_zip(filename):
    return zipfile.ZipFile(os.path.join(assets_dir, filename))
'''