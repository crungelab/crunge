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
    py::class_<SkGradientShader> GradientShader(_skia, "GradientShader");
    registry.on(_skia, "GradientShader", GradientShader);
    GradientShader
        ;

        py::enum_<SkGradientShader::Flags>(_skia, "Flags", py::arithmetic())
            .value("K_INTERPOLATE_COLORS_IN_PREMUL_FLAG", SkGradientShader::Flags::kInterpolateColorsInPremul_Flag)
            .export_values()
        ;

        GradientShader
        .def_static("make_linear", [](std::array<SkPoint, 2>& pts, const unsigned int colors[], const float pos[], int count, SkTileMode mode, unsigned int flags, const SkMatrix * localMatrix)
            {
                auto ret = SkGradientShader::MakeLinear(&pts[0], colors, pos, count, mode, flags, localMatrix);
                return std::make_tuple(ret, pts);
            }
            , py::arg("pts")
            , py::arg("colors")
            , py::arg("pos")
            , py::arg("count")
            , py::arg("mode")
            , py::arg("flags") = 0
            , py::arg("local_matrix") = nullptr
            , py::return_value_policy::automatic_reference)
        .def_static("make_radial", py::overload_cast<const SkPoint &, float, const unsigned int[], const float[], int, SkTileMode, unsigned int, const SkMatrix *>(&SkGradientShader::MakeRadial)
            , py::arg("center")
            , py::arg("radius")
            , py::arg("colors")
            , py::arg("pos")
            , py::arg("count")
            , py::arg("mode")
            , py::arg("flags") = 0
            , py::arg("local_matrix") = nullptr
            , py::return_value_policy::automatic_reference)
        .def_static("make_two_point_conical", py::overload_cast<const SkPoint &, float, const SkPoint &, float, const unsigned int[], const float[], int, SkTileMode, unsigned int, const SkMatrix *>(&SkGradientShader::MakeTwoPointConical)
            , py::arg("start")
            , py::arg("start_radius")
            , py::arg("end")
            , py::arg("end_radius")
            , py::arg("colors")
            , py::arg("pos")
            , py::arg("count")
            , py::arg("mode")
            , py::arg("flags") = 0
            , py::arg("local_matrix") = nullptr
            , py::return_value_policy::automatic_reference)
        .def_static("make_sweep", py::overload_cast<float, float, const unsigned int[], const float[], int, SkTileMode, float, float, unsigned int, const SkMatrix *>(&SkGradientShader::MakeSweep)
            , py::arg("cx")
            , py::arg("cy")
            , py::arg("colors")
            , py::arg("pos")
            , py::arg("count")
            , py::arg("mode")
            , py::arg("start_angle")
            , py::arg("end_angle")
            , py::arg("flags")
            , py::arg("local_matrix")
            , py::return_value_policy::automatic_reference)
    ;


}