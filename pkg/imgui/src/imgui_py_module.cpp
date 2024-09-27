#include <pybind11/pybind11.h>

#include <cxbind/cxbind.h>

namespace py = pybind11;

void init_imgui_py(py::module &, Registry& registry);
void init_imgui_py_auto(py::module &, Registry& registry);


PYBIND11_MODULE(_imgui, m) {
    Registry r;
    init_imgui_py(m, r);
    init_imgui_py_auto(m, r);
}