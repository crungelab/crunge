#include <iostream>
#include <limits>

#include <pybind11/functional.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <crunge/skia/conversions.h>
#include <crunge/skia/crunge-skia.h>
#include <cxbind/cxbind.h>

#include <include/core/SkMatrix.h>
#include <include/effects/SkGradient.h>

namespace py = pybind11;

void init_skia_gradient_py(py::module &_skia, Registry &registry) {
    PYEXTEND_BEGIN(SkGradient::Interpolation, GradientInterpolation)
    _GradientInterpolation.def(py::init<>());
    PYEXTEND_END
}
