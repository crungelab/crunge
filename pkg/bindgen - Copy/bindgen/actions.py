#from clang import cindex
from crunge.clang import cindex

MAP = {
    cindex.CursorKind.STRUCT_DECL : lambda self, node : self.parse_struct(node),
    cindex.CursorKind.CLASS_DECL : lambda self, node : self.parse_class(node),
    cindex.CursorKind.ENUM_DECL : lambda self, node : self.parse_enum(node),
    cindex.CursorKind.VAR_DECL : lambda self, node : self.parse_var(node),
    cindex.CursorKind.FUNCTION_DECL : lambda self, node : self.parse_function(node),
    cindex.CursorKind.NAMESPACE : lambda self, node : self.parse_definitions(node),
    cindex.CursorKind.UNEXPOSED_DECL : lambda self, node : self.parse_definitions(node),
}