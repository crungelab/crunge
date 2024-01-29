#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include "implot.h"
#include "implot_internal.h"

#include <cxbind/cxbind.h>
#include <crunge/imgui/crunge-imgui.h>
#include <crunge/imgui/conversions.h>

namespace py = pybind11;

void init_generated(py::module &_implot, Registry &registry) {
{{body}}
}