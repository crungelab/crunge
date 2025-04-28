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

void init_skia_gradient_shader_py(py::module &_skia, Registry &registry) {
    PYEXTEND_BEGIN(SkGradientShader, GradientShader)
    GradientShader
    .def_static("make_linear", [](const std::vector<SkPoint>& pts, std::vector<SkColor>& colors, std::vector<SkScalar>& pos, int count, SkTileMode mode, unsigned int flags, const SkMatrix * localMatrix)
    {
        auto ret = SkGradientShader::MakeLinear(&pts[0], &colors[0], &pos[0], count, mode, flags, localMatrix);
        //return std::make_tuple(ret, pts);
        return ret.release();
    }
    , py::arg("pts")
    , py::arg("colors")
    , py::arg("pos")
    , py::arg("count")
    , py::arg("mode")
    , py::arg("flags") = 0
    , py::arg("local_matrix") = nullptr
    , py::return_value_policy::automatic_reference);

    PYEXTEND_END
}
