from typing import TYPE_CHECKING, TypeVar, Generic, Dict, List

import re

from ..node import Node, RecordMember, Entry
from ..name import Name
from .render_context import RenderContext


# Define a generic type variable
T_Node = TypeVar("T_Node", bound=Node)


class Renderer(Generic[T_Node]):
    def __init__(
        self,
        context: RenderContext,
        node: Node = None,
    ) -> None:
        self.context = context
        self.out = context.out
        self.node = node

    def render(self):
        raise NotImplementedError

    #def lookup(self, name: str) -> Node:
    def lookup(self, name: str) -> Entry:
        return self.context.root[name]

    def exclude_node(self, node: Node) -> bool:
        if node.tags is not None:
            if len(node.tags) == 0:
                return True
            if "upstream" in node.tags:
                return True
        return False

    @staticmethod
    def as_varName(*names: Name) -> str:
        return names[0].camelCase() + "".join([name.CamelCase() for name in names[1:]])

    @staticmethod
    def as_cType(name: Name, c_prefix: str = "WGPU") -> str:
        # Special case for 'bool' because it has a typedef for compatibility.
        if name.native and name.get() != 'bool':
            return name.concatcase()
        elif name.get() == 'nullable string view':
            # nullable string view type doesn't exist in C.
            return c_prefix + 'StringView'
        else:
            return c_prefix + name.CamelCase()

    @staticmethod
    def as_cppType(name: Name) -> str:
        # Special case for 'bool' because it has a typedef for compatibility.
        if name.native and name.get() != "bool":
            return name.concatcase()
        else:
            return name.CamelCase()

    @staticmethod
    def as_cppFqType(name: Name, namespace: str = "wgpu") -> str:
        # Special case for 'bool' because it has a typedef for compatibility.
        if name.native and name.get() != "bool":
            return name.concatcase()
        else:
            return namespace + "::" + name.CamelCase()

    @staticmethod
    def as_cppEnum(value_name: Name) -> str:
        assert not value_name.native
        if value_name.concatcase()[0].isdigit():
            return "e" + value_name.CamelCase()
        return value_name.CamelCase()

    @staticmethod
    def snake(name: str) -> str:
        s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
        return re.sub("([a-z])([A-Z])", r"\1_\2", s1).lower()

    @staticmethod
    def as_pyEnum(name: Name) -> str:
        result = Renderer.as_cppEnum(name)
        result = Renderer.snake(result).upper()
        result = result.replace("__", "_")
        result = result.rstrip("_")
        return result

    @staticmethod
    def decorate_type(typ, arg: RecordMember, make_const=False):
        type_name = Renderer.as_cppFqType(typ.name)
        maybe_const = 'const ' if make_const else ''
        #if arg.annotation == 'value':
        if arg.annotation is None:
            #return type_name + maybe_const
            return maybe_const + type_name
        elif arg.annotation == '*':
            #return type_name + ' *' + maybe_const
            return maybe_const + type_name + ' *'
        elif arg.annotation == 'const*':
            #return type_name + ' const *' + maybe_const
            return maybe_const + type_name + ' const *'
        elif arg.annotation == 'const*const*':
            #return 'const ' + type_name + '* const *' + maybe_const
            return maybe_const + 'const ' + type_name + '* const *'
        else:
            assert False

    '''
    @staticmethod
    def decorate_type(typ, arg: RecordMember, make_const=False):
        #type_name = "wgpu::" + typ.name.get() if not typ.name.native else typ.name.concatcase()
        type_name = Renderer.as_cppFqType(typ.name)
        maybe_const = 'const ' if make_const else ''
        #if arg.annotation == 'value':
        if arg.annotation is None:
            #return typ + maybe_const
            return maybe_const + type_name
        elif arg.annotation == '*':
            #return typ + ' *' + maybe_const
            return maybe_const + type_name + ' *'
        elif arg.annotation == 'const*':
            #return typ + ' const *' + maybe_const
            return maybe_const + type_name + ' const *'
        elif arg.annotation == 'const*const*':
            #return 'const ' + typ + '* const *' + maybe_const
            return maybe_const + 'const ' + type_name + '* const *'
        else:
            assert False
    '''

    @staticmethod
    def decorate_member(name, typ, arg: RecordMember, make_const=False):
        maybe_const = ' const ' if make_const else ' '
        #if arg.annotation == 'value':
        if arg.annotation is None:
            return typ + maybe_const + name
        elif arg.annotation == '*':
            return typ + ' *' + maybe_const + name
        elif arg.annotation == 'const*':
            return typ + ' const *' + maybe_const + name
        elif arg.annotation == 'const*const*':
            return 'const ' + typ + '* const *' + maybe_const + name
        else:
            assert False

    '''
    @staticmethod
    def decorate(name, typ, arg: RecordMember, make_const=False):
        maybe_const = ' const ' if make_const else ' '
        #if arg.annotation == 'value':
        if arg.annotation is None:
            return typ + maybe_const + name
        elif arg.annotation == '*':
            return typ + ' *' + maybe_const + name
        elif arg.annotation == 'const*':
            return typ + ' const *' + maybe_const + name
        elif arg.annotation == 'const*const*':
            return 'const ' + typ + '* const *' + maybe_const + name
        else:
            assert False
    '''

    '''
    @staticmethod
    def annotated(typ: Entry, arg: RecordMember, make_const=False):
        name = Renderer.as_varName(arg.name)
        return Renderer.decorate(name, typ, arg, make_const)
    '''
    @staticmethod
    def annotated_type(typ: Entry, arg: RecordMember, make_const=False):
        return Renderer.decorate_type(typ, arg, make_const)

    @staticmethod
    def annotated_member(typ: Entry, arg: RecordMember, make_const=False):
        name = Renderer.as_varName(arg.name)
        return Renderer.decorate_member(name, typ, arg, make_const)

    def as_cTypeEnumSpecialCase(self, typ: Entry) -> str:
        return Renderer.as_cType(self.context.c_prefix, typ.name)

    def as_annotated_cType(self, arg: RecordMember, make_const=False) -> str:
        return Renderer.annotated(self.as_cTypeEnumSpecialCase(self.lookup(arg.type).name), arg, make_const)

    def as_annotated_cppType(self, arg: RecordMember, make_const=False) -> str:
        #return Renderer.annotated_type(self.as_cppType(self.lookup(arg.type).name), arg, make_const)
        return Renderer.annotated_type(self.lookup(arg.type), arg, make_const)

    def as_annotated_cppMember(self, arg: RecordMember, make_const=False) -> str:
        return Renderer.annotated_member(self.as_cppType(self.lookup(arg.type).name), arg, make_const)

    def render_cpp_default_value(self, member: RecordMember, is_struct: bool, force_default=False):
        member_type = self.lookup(member.type)
        if member.no_default is not None and member.no_default:
            pass
        elif member.annotation in ["*", "const*"] and member.optional or member.default_value == "nullptr":
            return " = nullptr"
        elif member_type.category == "object" and member.optional and is_struct:
            return " = nullptr"
        elif member_type.category in ["enum", "bitmask"] and member.default_value is not None:
            return f" = {Renderer.as_cppType(member_type.name)}::{Renderer.as_cppEnum(Name(member.default_value))}"
        elif member_type.category == "native" and member.default_value is not None:
            return f" = {member.default_value}"
        elif member.default_value is not None:
            return f" = {member.default_value}"
        #elif member_type.category == "structure" and member.annotation == "value" and is_struct:
        elif member_type.category == "structure" and not member.annotation and is_struct:
            return " = {}"
        else:
            assert member.default_value is None
            if force_default:
                return " = {}"
        return ""

    @staticmethod
    def wgpu_string_constructors(CppType: Node, is_nullable: bool):
        result = f'''\
        // NOLINTNEXTLINE(runtime/explicit) allow implicit construction
        inline constexpr {CppType}(const std::string_view& sv) noexcept {{
            this->data = sv.data();
            this->length = sv.length();
        }}
        // NOLINTNEXTLINE(runtime/explicit) allow implicit construction
        inline constexpr {CppType}(const char* s) {{
            this->data = s;
            this->length = SIZE_MAX;  // use strlen
        }}
        inline constexpr {CppType}(const char* data, size_t length) {{
            this->data = data;
            this->length = length;
        }}
        '''

        if is_nullable:
            result += f'''\
            inline constexpr {CppType}() noexcept = default;

            // NOLINTNEXTLINE(runtime/explicit) allow implicit construction
            inline constexpr {CppType}(std::nullptr_t) {{
                this->data = nullptr;
                this->length = SIZE_MAX;
            }}
            // NOLINTNEXTLINE(runtime/explicit) allow implicit construction
            inline constexpr {CppType}(std::nullopt_t) {{
                this->data = nullptr;
                this->length = SIZE_MAX;
            }}
        '''
        return result
'''
{% macro wgpu_string_constructors(CppType, is_nullable) %}
    // NOLINTNEXTLINE(runtime/explicit) allow implicit construction
    inline constexpr {{CppType}}(const std::string_view& sv) noexcept {
        this->data = sv.data();
        this->length = sv.length();
    }
    // NOLINTNEXTLINE(runtime/explicit) allow implicit construction
    inline constexpr {{CppType}}(const char* s) {
        this->data = s;
        this->length = SIZE_MAX;  // use strlen
    }
    inline constexpr {{CppType}}(const char* data, size_t length) {
        this->data = data;
        this->length = length;
    }
    {% if is_nullable %}
        inline constexpr {{CppType}}() noexcept = default;

        // NOLINTNEXTLINE(runtime/explicit) allow implicit construction
        inline constexpr {{CppType}}(std::nullptr_t) {
            this->data = nullptr;
            this->length = SIZE_MAX;
        }
        // NOLINTNEXTLINE(runtime/explicit) allow implicit construction
        inline constexpr {{CppType}}(std::nullopt_t) {
            this->data = nullptr;
            this->length = SIZE_MAX;
        }
    {% endif %}
{% endmacro %}
'''
class NullRenderer(Renderer[Node]):
    def render(self):
        pass


"""
class RendererBase:
    def __init__(self, context: RenderContext) -> None:
        self.context = context
        self.out = context.out

    def render(self):
        raise NotImplementedError
    

# Define a generic type variable
T_Node = TypeVar("T_Node", bound=Node)

class Renderer(RendererBase, Generic[T_Node]):
    def __init__(
        self,
        context: RenderContext,
        node: Node = None,
    ) -> None:
        super().__init__(context)
        self.node = node
"""
