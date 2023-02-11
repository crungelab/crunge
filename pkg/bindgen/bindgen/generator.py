import os
from pathlib import Path
import importlib
from loguru import logger
import jinja2
#from clang import cindex
from crunge.clang import cindex

from . import UserSet

from .transpiler import Transpiler
from .entry import Entry, FunctionEntry, CtorEntry, FieldEntry, MethodEntry, StructEntry, create_entry
from .yaml import load_yaml

entry_cls_map = {
    'function': FunctionEntry,
    'ctor': CtorEntry,
    'field': FieldEntry,
    'method': MethodEntry,
    'struct': StructEntry
}

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
        self.excludes = []
        self.overloads = []
        self.config = config
        self.options = { 'save': True }
        for key, value in config.items():
            #logger.debug(config[key])
            if '.' in key:
                self.create_entry(key, value)
            else:
                setattr(self, key, value)

        for key in kwargs:
            if key == 'options':
                options = kwargs[key]
                options.update(self.options)
                self.options = options

            setattr(self, key, kwargs[key])
        
        self.options = Options(self.options)
        self.excluded = set(self.excludes)
        self.overloaded = Overloaded(self.overloads)

        BASE_PATH = Path('.')
        self.path = BASE_PATH / self.source
        #self.path = Path(self.source).absolute()
        self.mapped.append(self.path.name)

    def create_entry(self, key, value):
        s = key.split('.')
        cls = entry_cls_map[s[0]]
        entry = cls(value)

        if entry.exclude:
            self.excludes.append(s[1])
        if entry.overload:
            self.overloads.append(s[1])

        self.entries[s[1]] = entry

        return entry

    @classmethod
    def create(self, name="bindgen"):
        filename = f'{name}.yaml'
        print(f'processing:  {filename}')
        path = Path(os.getcwd(), '.bindgen', filename)
        #logger.debug(path)
        config = load_yaml(path)
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

        with self:
            self.visit_overloads(tu.cursor)
            self.visit_children(tu.cursor)

        #Jinja
        config = self.config
        #logger.debug(self.config)
        config['body'] = self.text
        self.searchpath = Path('.')  / '.bindgen'
        loader = jinja2.FileSystemLoader(searchpath=self.searchpath)
        env = jinja2.Environment(loader=loader)

        template = env.get_template(f'{self.name}.cpp')
        rendered = template.render(config)
        filename = self.target
        with open(filename,'w') as fh:
            fh.write(rendered)
