#include <limits>
// #include <iostream>
#include <sstream>

#include <pybind11/functional.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>

#include <crunge/box2d/conversions.h>
#include <crunge/box2d/crunge-box2d.h>

#include <box2d/math_functions.h>

namespace py = pybind11;

void init_math_functions_py(py::module &_box2d, Registry &registry) {
    PYEXTEND_BEGIN(b2Vec2, Vec2)
    _Vec2.def(
        "__add__", [](const b2Vec2 &a, const b2Vec2 &b) { return b2Add(a, b); },
        py::is_operator());
    PYEXTEND_END
}