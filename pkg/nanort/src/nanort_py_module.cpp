#include <pybind11/pybind11.h>

#include <cxbind/cxbind.h>

namespace py = pybind11;

void init_nanort_py(py::module &, Registry& registry);
void init_nanort_py_auto(py::module &, Registry& registry);


PYBIND11_MODULE(_nanort, m) {
    Registry r;
    init_nanort_py(m, r);
    init_nanort_py_auto(m, r);
}