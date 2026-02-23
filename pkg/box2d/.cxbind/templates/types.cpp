#include <limits>
//#include <iostream>
#include <sstream>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>


#include <cxbind/cxbind.h>

//#include <crunge/box2d/crunge-box2d.h>
//#include <crunge/box2d/conversions.h>

#include <box2d/types.h>

namespace py = pybind11;

void init_types_py_auto(py::module &_box2d, Registry &registry) {
{{body}}
}