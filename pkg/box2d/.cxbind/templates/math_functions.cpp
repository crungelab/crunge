#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

//#include <iostream>

#include <cxbind/cxbind.h>

//#include <crunge/tmx/crunge-tmx.h>
//#include <crunge/tmx/conversions.h>

//#include <tmxlite/Map.hpp>
//#include <tmxlite/ImageLayer.hpp>

#include <box2d/math_functions.h>

namespace py = pybind11;

void init_math_functions_py_auto(py::module &_box2d, Registry &registry) {
{{body}}
}