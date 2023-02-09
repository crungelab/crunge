import os
from pathlib import Path
import importlib
import toml
#from clang import cindex
from crunge.clang import cindex
from loguru import logger

from . import UserSet

from .transpiler import Transpiler

import jinja2

class Options:
    def __init__(self, *options, **kwargs):
        for dictionary in options:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])

class Overloaded(UserSet):
    def __init__(self, data) -> None:
        super().__init__(data)
        self.visited = set()

    def is_overloaded(self, node):
        return self.name(node) in self

class Generator(Transpiler):
    def __init__(self, config, **kwargs):
        super().__init__()
        self.config = config
        self.options = { 'save': True }
        for key in config:
            #print(config[key])
            setattr(self, key, config[key])
        for key in kwargs:
            if key == 'options':
                options = kwargs[key]
                options.update(self.options)
                self.options = options

            setattr(self, key, kwargs[key])
        
        self.options = Options(self.options)
        self.overloaded = Overloaded(self.overloaded)

        BASE_PATH = Path('.')
        self.path = BASE_PATH / self.source
        #self.path = Path(self.source).absolute()
        self.mapped.append(self.path.name)

    @classmethod
    def create(self, name="bindgen"):
        filename = f'{name}.toml'
        print(f'processing:  {filename}')
        path = Path(os.getcwd(), '.bindgen', filename)
        #print(path)
        config = toml.load(path)
        config['name'] = name
        instance = Generator(config)
        instance.import_actions()
        return instance

    def import_actions(self):
        path = Path(os.path.dirname(os.path.abspath(__file__)), 'actions.py')
        spec = importlib.util.spec_from_file_location(
            "actions", path
        )
        __actions__ = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(__actions__)

        self.actions = __actions__.MAP

    def generate(self):
        logger.debug(self.path)
        #tu = cindex.Index.create().parse(self.path, args=self.flags)
        tu = cindex.TranslationUnit.from_source(self.path, args=self.flags, options=cindex.TranslationUnit.PARSE_DETAILED_PROCESSING_RECORD)
        self.begin(tu)
        self.scope.indent = 1
        self.parse_overloads(tu.cursor)
        self.parse_definitions(tu.cursor)
        self.scope.indent = 0
        #self.scope(self.footer)
        #Jinja
        config = self.config
        #print(self.config)
        config['body'] = self.scope.text
        self.searchpath = Path('.')  / '.bindgen'
        loader = jinja2.FileSystemLoader(searchpath=self.searchpath)
        env = jinja2.Environment(loader=loader)

        template = env.get_template(f'{self.name}.cpp')
        rendered = template.render(config)
        filename = self.target
        with open(filename,'w') as fh:
            fh.write(rendered)
