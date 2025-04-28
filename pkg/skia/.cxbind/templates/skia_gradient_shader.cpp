#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/conversions.h>

#include <include/effects/SkGradientShader.h>
#include <include/core/SkMatrix.h>


namespace py = pybind11;

void init_skia_gradient_shader_py_auto(py::module &_skia, Registry &registry) {
{{body}}
}