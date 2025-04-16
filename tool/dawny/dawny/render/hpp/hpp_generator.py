from typing import TYPE_CHECKING
from typing import List

if TYPE_CHECKING:
    from ...backend import Backend

import networkx as nx

from ..generator import Generator, SpecialStructures
from ...node import ObjectType, StructureType

from .hpp_render_context import HppRenderContext

def topological_sort(G):
    result = list(nx.topological_sort(G))
    result.reverse()
    return result

class HppGenerator(Generator):
    def __init__(self, backend: "Backend") -> None:
        context = HppRenderContext(backend.program.root, backend.jinja_env)
        super().__init__(context, backend)

    def render(self):
        # using declarations
        '''
        self.out << """
using BufferMapCallback = WGPUBufferMapCallback;
using Callback = WGPUCallback;
using CompilationInfoCallback = WGPUCompilationInfoCallback;
using CreateComputePipelineAsyncCallback = WGPUCreateComputePipelineAsyncCallback;
using CreateRenderPipelineAsyncCallback = WGPUCreateRenderPipelineAsyncCallback;
using DawnLoadCacheDataFunction = WGPUDawnLoadCacheDataFunction;
using DawnStoreCacheDataFunction = WGPUDawnStoreCacheDataFunction;
using DeviceLostCallback = WGPUDeviceLostCallback;
using DeviceLostCallbackNew = WGPUDeviceLostCallbackNew;
using ErrorCallback = WGPUErrorCallback;
using LoggingCallback = WGPULoggingCallback;
using PopErrorScopeCallback = WGPUPopErrorScopeCallback;
using Proc = WGPUProc;
using QueueWorkDoneCallback = WGPUQueueWorkDoneCallback;
using RequestAdapterCallback = WGPURequestAdapterCallback;
using RequestDeviceCallback = WGPURequestDeviceCallback;

using UncapturedErrorCallback = WGPUUncapturedErrorCallback;
using DeviceLostCallback2 = WGPUDeviceLostCallback2;
using RequestDeviceCallback2 = WGPURequestDeviceCallback2;
using QueueWorkDoneCallback2 = WGPUQueueWorkDoneCallback2;
using PopErrorScopeCallback2 = WGPUPopErrorScopeCallback2;
using CreateRenderPipelineAsyncCallback2 = WGPUCreateRenderPipelineAsyncCallback2;
using CreateComputePipelineAsyncCallback2 = WGPUCreateComputePipelineAsyncCallback2;
using CompilationInfoCallback2 = WGPUCompilationInfoCallback2;
using BufferMapCallback2 = WGPUBufferMapCallback2;
using RequestAdapterCallback2 = WGPURequestAdapterCallback2;
""" << "\n"
        '''

        '''
        using {{as_cppType(type.name)}} = {{as_cType(type.name)}};
        '''
        
        for node in self.backend.function_pointer_types:
            #self.out << f"using {node.name.CamelCase()} = {self.as_cppType(node.name)};" << "\n"
            self.out << f"using {self.as_cppType(node.name)} = {self.as_cType(node.name)};" << "\n"
        self.out << "\n"

        for node in self.backend.callback_info_types:
            #self.out << f"using {node.name.CamelCase()} = {self.as_cppType(node.name)};" << "\n"
            self.out << f"using {self.as_cppType(node.name)} = {self.as_cType(node.name)};" << "\n"
        self.out << "\n"

        # forward declarations
        for node in self.backend.structure_types:
            if self.exclude_structure_type(node):
                continue
            self.out << f"struct {node.name.CamelCase()};" << "\n"

        self.out << "\n"

        # calback templates
        #cb_template = self.context.jinja_env.get_template('_callback.h.j2')
        #self.out << cb_template.render() << "\n" << "\n"

        for node in self.backend.object_types:
            self.out << f"class {node.name.CamelCase()};" << "\n"

        self.out << "\n"
        
        self.render_constant_definitions()
        self.render_enum_types()
        self.render_bitmask_types()

        # calback templates
        cb_template = self.context.jinja_env.get_template('_callback.h.j2')
        self.out << cb_template.render() << "\n" << "\n"

        #self.render_structure_types()
        #self.render_object_types()
        custom_template = self.context.jinja_env.get_template('_custom.h.j2')
        self.out << custom_template.render() << "\n" << "\n"

        self.render_declarations()

        self.render_function_declarations()

        super().render()

    '''
    {% for constant in by_category["constant"] %}
        {% set type = as_cppType(constant.type.name) %}
        {% if constant.cpp_value %}
            static constexpr {{type}} k{{constant.name.CamelCase()}} = {{ constant.cpp_value }};
        {% else %}
            {% set value = c_prefix + "_" +  constant.name.SNAKE_CASE() %}
            static constexpr {{type}} k{{constant.name.CamelCase()}} = {{ value }};
        {% endif %}
    {% endfor %}
    '''

    def render_constant_definitions(self):
        for constant in self.backend.constant_definitions:
            constant_type = self.lookup(constant.type)
            type = self.as_cppType(constant_type.name)
            if constant.cpp_value:
                self.out << f"static constexpr {type} k{constant.name.CamelCase()} = {constant.cpp_value};" << "\n"
            else:
                value = f"{self.context.c_prefix}_{constant.name.SNAKE_CASE()}"
                self.out << f"static constexpr {type} k{constant.name.CamelCase()} = {value};" << "\n"
        self.out << "\n"

    def render_declarations(self):
        declarations = []
        for node in self.backend.object_types:
            if self.exclude_object_type(node):
                continue
            declarations.append(node)
        for node in self.backend.structure_types:
            if self.exclude_structure_type(node):
                continue
            declarations.append(node)
        graph = self.create_dependency_graph(declarations)
        sorted_declarations = topological_sort(graph)
        for decl in sorted_declarations:
            self.render_node(decl)

    def create_dependency_graph(self, declarations):
        G = nx.DiGraph()

        for decl in declarations:
            G.add_node(decl)

        for decl in declarations:
            if isinstance(decl, StructureType):
                for member in decl.members:
                    member_type = self.context.root[member.type]
                    if member_type in G.nodes:
                        G.add_edge(decl, member_type)
        return G
