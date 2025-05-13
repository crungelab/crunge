#include <pybind11/pybind11.h>

#include <cxbind/cxbind.h>

namespace py = pybind11;

void init_wgpu_py(py::module &, Registry& registry);
void init_chained_struct(py::module &, Registry& registry);
void init_wgpu_py_auto(py::module &, Registry& registry);
void init_callbacks(py::module &, Registry& registry);


PYBIND11_MODULE(_wgpu, m) {
        Registry r;
        init_wgpu_py(m, r);
        init_chained_struct(m, r);
        init_wgpu_py_auto(m, r);
        init_callbacks(m, r);
}