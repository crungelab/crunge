#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include "imgui.h"
#include "imgui_internal.h"

#include <crunge/imgui/crunge-imgui.h>
#include <crunge/imgui/conversions.h>
#include <cxbind/cxbind.h>

#include "imnodes.h"
#include "imnodes_internal.h"

namespace py = pybind11;

void init_generated(py::module &_imnodes, Registry &registry) {
{{body}}
}