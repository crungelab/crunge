#include <pybind11/pybind11.h>

#include <cxbind/cxbind.h>

namespace py = pybind11;

void init_main(py::module &, Registry& registry);
void init_skia_context_py_auto(py::module &, Registry& registry);
void init_skia_canvas_py_auto(py::module &, Registry& registry);


PYBIND11_MODULE(_wgpu, m) {
        Registry r;
        init_main(m, r);
        init_skia_context_py_auto(m, r);
        init_skia_canvas_py_auto(m, r);
}