#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

//#include "imgui_internal.h"
#include "imgui.h"

#include <cxbind/cxbind.h>
#include <crunge/imgui/conversions.h>

namespace py = pybind11;

void init_imgui_py_auto(py::module &_imgui, Registry &registry) {
{{body}}
}