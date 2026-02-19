#include <pybind11/pybind11.h>

#include <cxbind/cxbind.h>

namespace py = pybind11;

void init_box2d_py_auto(py::module &, Registry& registry);
void init_types_py_auto(py::module &, Registry& registry);
void init_math_functions_py_auto(py::module &, Registry& registry);
void init_id_py_auto(py::module &, Registry& registry);
void init_collision_py_auto(py::module &, Registry& registry);


PYBIND11_MODULE(_box2d, m) {
    Registry r;
    init_box2d_py_auto(m, r);
    init_types_py_auto(m, r);
    init_math_functions_py_auto(m, r);
    init_id_py_auto(m, r);
    init_collision_py_auto(m, r);
}