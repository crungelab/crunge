#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/operators.h>
#include <pybind11/stl.h>
#include <limits>

#include <dawn/webgpu_cpp.h>

#include <cxbind/cxbind.h>
#include <crunge/wgpu/conversions.h>

namespace py = pybind11;

using namespace wgpu;

void init_wgpu(py::module &_wgpu, Registry &registry) {
{{body}}
}