#include <pybind11/pybind11.h>

#include <cxbind/cxbind.h>

namespace py = pybind11;

void init_rtaudio_py(py::module &, Registry& registry);
void init_rtaudio_py_auto(py::module &, Registry& registry);
void init_augr_py_auto(py::module &, Registry& registry);


PYBIND11_MODULE(_rtaudio, m) {
    Registry r;
    init_rtaudio_py(m, r);
    init_rtaudio_py_auto(m, r);
    init_augr_py_auto(m, r);
}