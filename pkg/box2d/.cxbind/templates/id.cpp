#include <limits>
//#include <iostream>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>


#include <cxbind/cxbind.h>
#include <cxbind/callback.h>

//#include <crunge/box2d/crunge-box2d.h>
//#include <crunge/box2d/conversions.h>

#include <box2d/id.h>
#include <box2d/box2d.h>

#include "box2d_internal.h"

namespace py = pybind11;

void init_id_py_auto(py::module &_box2d, Registry &registry) {
{{body}}
}