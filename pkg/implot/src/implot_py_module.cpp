#include <pybind11/pybind11.h>

#include <cxbind/cxbind.h>

namespace py = pybind11;

void init_main(py::module &, Registry& registry);
void init_generated(py::module &, Registry& registry);


PYBIND11_MODULE(_implot, m) {
        Registry r;
        init_main(m, r);
        init_generated(m, r);
}