#include <limits>
#include <filesystem>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#define BUILDING_DLL

#include <nanort.h>

#include <cxbind/cxbind.h>

#include <crunge/nanort/crunge-nanort.h>
#include <crunge/nanort/conversions.h>

namespace py = pybind11;

void init_nanort_py(py::module &_nanort, Registry &registry) {
}