#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/conversions.h>

#include <include/core/SkMatrix.h>
#include <include/core/SkPoint3.h>
#include <include/core/SkRSXform.h>


namespace py = pybind11;

void init_skia_matrix_py_auto(py::module &_skia, Registry &registry) {
{{body}}
}