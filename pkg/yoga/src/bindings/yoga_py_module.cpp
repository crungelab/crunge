#include <pybind11/pybind11.h>

#include <cxbind/cxbind.h>

namespace py = pybind11;

void init_yoga_numeric_py_auto(py::module &, Registry& registry);
void init_yoga_enums_py_auto(py::module &, Registry& registry);
void init_yoga_style_py_auto(py::module &, Registry& registry);
void init_yoga_node_py(py::module &, Registry& registry);
void init_yoga_node_py_auto(py::module &, Registry& registry);
void init_yoga_algorithm_py_auto(py::module &, Registry& registry);


PYBIND11_MODULE(_yoga, m) {
    Registry r;
    //init_yoga_numeric_py_auto(m, r);
    init_yoga_enums_py_auto(m, r);
    init_yoga_style_py_auto(m, r);
    init_yoga_node_py(m, r);
    init_yoga_node_py_auto(m, r);
    //init_yoga_algorithm_py_auto(m, r);
}
