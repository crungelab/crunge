#include <pybind11/pybind11.h>

#include <cxbind/cxbind.h>

namespace py = pybind11;

void init_tmx_py(py::module &, Registry& registry);


PYBIND11_MODULE(_tmx, m) {
    Registry r;
    init_tmx_py(m, r);
}