#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

#include "imgui.h"
#include "imgui_internal.h"

#include <crunge/core/bindtools.h>
#include <crunge/imgui/conversions.h>

namespace py = pybind11;

void init_generated(py::module &_imgui, Registry &registry) {
{{body}}
}