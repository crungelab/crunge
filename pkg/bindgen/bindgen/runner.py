import os, sys

from pathlib import Path
import importlib.util

#from clang import cindex
from crunge.clang import cindex

from . import generator as dot_bindgen

class Runner:
    def __init__(self):
        if sys.platform == 'darwin':
            cindex.Config.set_library_path('/usr/local/opt/llvm@6/lib')
        elif sys.platform == 'linux':
            cindex.Config.set_library_file('libclang-10.so')
        else:
            cindex.Config.set_library_path('C:/Program Files/LLVM/bin')

    def gen(self, name):
        global dot_bindgen
        path = Path(os.getcwd(), '.bindgen', '__init__.py')
        if os.path.exists(path):
            spec = importlib.util.spec_from_file_location(
                "dot_bindgen", path
            )
            dot_bindgen = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(dot_bindgen)

        generator = dot_bindgen.Generator.create(name)
        generator.generate()

    def gen_all(self):
        path = Path(os.getcwd(), '.bindgen')
        files = path.glob('*.yaml')
        for file in files:
            self.gen(file.stem)