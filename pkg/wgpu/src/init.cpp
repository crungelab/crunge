#include <pybind11/pybind11.h>

#include <cxbind/cxbind.h>

namespace py = pybind11;

void init_main(py::module &, Registry& registry);
void init_chained_struct(py::module &, Registry& registry);
void init_wgpu(py::module &, Registry& registry);


PYBIND11_MODULE(_wgpu, m) {
        Registry r;
        init_main(m, r);
        init_chained_struct(m, r);
        init_wgpu(m, r);
}