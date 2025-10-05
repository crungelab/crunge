#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

#include <nanort.h>
#include <iostream>

#include <cxbind/cxbind.h>
#include <crunge/nanort/conversions.h>

namespace py = pybind11;

using namespace nanort;

void init_nanort_py_auto(py::module &_nanort, Registry &registry) {
{{body}}
}