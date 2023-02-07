#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <crunge/core/bindtools.h>

#include <crunge/bgfx/crunge-bgfx.h>
#include <bx/allocator.h>
#include <bgfx/embedded_shader.h>

using namespace bgfx;

namespace py = pybind11;

void init_embedded_shader(py::module &_bgfx, Registry &registry) {
    PYCLASS_BEGIN(_bgfx, bgfx::EmbeddedShader, EmbeddedShader)
    EmbeddedShader.def_property("name",
        [](const bgfx::EmbeddedShader& self){ return self.name; },[](bgfx::EmbeddedShader& self, std::string source){ char* c = (char *)malloc(source.size()); strcpy(c, source.c_str()); self.name = c; }
    );
    EmbeddedShader.def_readonly("data", &bgfx::EmbeddedShader::data);
    PYCLASS_END(_bgfx, bgfx::EmbeddedShader, EmbeddedShader)

    _bgfx.def("create_embedded_shader", &bgfx::createEmbeddedShader
    , py::arg("_es")
    , py::arg("_type")
    , py::arg("_name")
    , py::return_value_policy::automatic_reference);

}