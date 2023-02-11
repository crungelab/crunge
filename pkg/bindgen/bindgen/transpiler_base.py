import re
from pathlib import Path
from contextlib import contextmanager

from loguru import logger

#from clang import cindex
from crunge.clang import cindex

from .entry import Entry, FunctionEntry, CtorEntry, FieldEntry, MethodEntry, StructEntry, ClassEntry

entry_cls_map = {
    'function': FunctionEntry,
    'ctor': CtorEntry,
    'field': FieldEntry,
    'method': MethodEntry,
    'struct': StructEntry,
    'class': ClassEntry
}

class TranspilerBase:
    def __init__(self):
        self.indentation = 0
        self.text = ''
        self.source = ''
        self.mapped = [] #headers we want to generate bindings for
        self.target = ''
        self.prefix = ''
        self.short_prefix = ''
        self.module = ''
        self.flags = []
        self.defaults = {}
        self.excludes = []
        self.overloads = []
        self.entries = {}
        self.entry_stack = []

    @property
    def entry(self):
        return self.entry_stack [-1]

    def __call__(self, line=""):
        if len(line):
            self.text += ' ' * self.indentation * 4
            self.text += line.replace('>>', '> >')
        self.text += '\n'

    @contextmanager
    def enter(self, entry_key, value={}):
        kind, key = entry_key.split('.')
        entry = self.lookup_or_create(entry_key, value)
        self.entry_stack.append(entry)

        self.indent()
        yield entry
        self.dedent()
        self.entry_stack.pop()

    def __enter__(self):
        self.indent()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dedent()

    def indent(self):
        self.indentation +=1

    def dedent(self):
        self.indentation -=1

    def lookup(self, entry_key):
        kind, key = entry_key.split('.')
        if key in self.entries:
            return self.entries[key]
        return None

    def lookup_or_create(self, entry_key, value):
        kind, key = entry_key.split('.')
        entry = self.lookup(entry_key)
        if not entry:
            entry = self.create_entry(entry_key, value)
        return entry

    def create_entry(self, entry_key, value):
        kind, key = entry_key.split('.')
        cls = entry_cls_map[kind]
        entry = cls(key, value)

        if entry.exclude:
            self.excludes.append(key)
        if entry.overload:
            self.overloads.append(key)

        self.entries[key] = entry

        return entry

    def snake(self, name):
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def format_attribute(self, name):
        name = self.snake(name)
        name = name.rstrip('_')
        name = name.replace('__', '_')
        return name

    def format_type(self, name):
        name = name.replace(self.prefix, '')
        name = name.replace(self.short_prefix, '')
        name = name.replace('<', '_')
        name = name.replace('>', '')
        name = name.replace(' ', '')
        name = name.rstrip('_')
        return name

    def format_enum(self, name):
        name = name.replace(self.prefix, '')
        name = name.replace(self.short_prefix, '')
        name = self.snake(name).upper()
        name = name.replace('__', '_')
        name = name.rstrip('_')
        return name

    def module_(self, node):
        if node is None:
            return self.module
        else:
            return self.format_type(node.spelling)

    def is_excluded(self, node):
        #logger.debug(self.spell(node))
        #logger.debug(node.spelling)
        if self.spell(node) in self.excluded:
            return True
        if node.spelling.startswith('_'):
            return True
        return False

    def spell(self, node):
        if node is None:
            return ''
        elif node.kind == cindex.CursorKind.TRANSLATION_UNIT:
            return ''
        else:
            res = self.spell(node.semantic_parent)
            if res != '':
                return res + '::' + node.spelling
        return node.spelling

    def is_class_mappable(self, node):
        if not node.is_definition():
            return False
        if self.is_excluded(node):
            return False
        return True

    def is_function_mappable(self, node):
        if 'operator' in node.spelling:
            return False
        if self.is_excluded(node):
            return False
        for argument in node.get_arguments():
            if argument.type.get_canonical().kind == cindex.TypeKind.POINTER:
                ptr = argument.type.get_canonical().get_pointee().kind
                if ptr == cindex.TypeKind.FUNCTIONPROTO:
                    return False
            if argument.type.spelling == 'va_list':
                return False
        return True

    def is_char_pointer(self, node):
        if node.type.get_canonical().kind == cindex.TypeKind.POINTER:
            ptr = node.type.get_canonical().get_pointee().kind
            if ptr == cindex.TypeKind.CHAR_S:
                return True
        return False

    def is_forward_declaration(self, node):
        definition = node.get_definition()

        # If the definition is null, then there is no definition in this translation
        # unit, so this cursor must be a forward declaration.
        if not definition:
            return True
        # If there is a definition, then the forward declaration and the definition
        # are in the same translation unit. This cursor is the forward declaration if
        # it is _not_ the definition.
        return node != definition

    def is_function_void_return(self, node):
        result = node.type.get_result()
        return result.kind == cindex.TypeKind.VOID

    def is_property_mappable(self, node):
        if self.is_excluded(node):
            return False
        return True

    def is_node_mappable(self, node):
        #print(node.location.file.name)
        if node.location.file:
            node_path = Path(node.location.file.name)
            return node_path.name in self.mapped
        return False

    def is_property_readonly(self, node):
        if node.type.kind == cindex.TypeKind.CONSTANTARRAY:
            return True
        return False

    def is_overloaded(self, node):
        return self.spell(node) in self.overloaded

    def arg_type(self, argument):
        if argument.type.kind == cindex.TypeKind.CONSTANTARRAY:
            return f'std::array<{argument.type.get_array_element_type().spelling}, {argument.type.get_array_size()}>&'
        return argument.type.spelling

    def arg_name(self, argument):
        if argument.type.kind == cindex.TypeKind.CONSTANTARRAY:
            return f'&{argument.spelling}[0]'
        return argument.spelling

    def arg_types(self, arguments):
        return ', '.join([self.arg_type(a) for a in arguments])

    def arg_names(self, arguments):
        return ', '.join([self.arg_name(a) for a in arguments])

    def arg_string(self, arguments):
        return ', '.join(['{} {}'.format(self.arg_type(a), a.spelling) for a in arguments])

    def default_from_tokens(self, tokens):
        joined = ''.join([t.spelling for t in tokens])
        parts = joined.split('=')
        if len(parts) == 2:
            return parts[1]
        return ''

    def write_pyargs(self, arguments):
        for argument in arguments:
            default = self.default_from_tokens(argument.get_tokens())
            for child in argument.get_children():
                if child.type.kind in [cindex.TypeKind.POINTER]:
                    default = 'nullptr'
                elif not len(default):
                    default = self.default_from_tokens(child.get_tokens())
            default = self.defaults.get(argument.spelling, default)
            #logger.debug(argument.spelling)
            #logger.debug(default)
            if len(default):
                default = ' = ' + default
            self(f', py::arg("{self.format_attribute(argument.spelling)}"){default}')
