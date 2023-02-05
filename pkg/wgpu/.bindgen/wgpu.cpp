#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

#include <dawn/webgpu_cpp.h>

#include <crunge/core/bindtools.h>

namespace py = pybind11;

void init_generated(py::module &_wgpu, Registry &registry) {
{{body}}
}