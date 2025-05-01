#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/effects/SkGradientShader.h>
#include <include/core/SkMatrix.h>

namespace py = pybind11;

void init_skia_gradient_shader_py(py::module &_skia, Registry &registry) {
    PYEXTEND_BEGIN(SkGradientShader, GradientShader)
    GradientShader
    .def_static("make_linear",[](
        const std::vector<SkPoint>& pts,
        const std::vector<SkColor>& colors,
        const std::vector<SkScalar>& pos, SkTileMode mode, unsigned int flags, const SkMatrix * localMatrix)
    {
        auto count = static_cast<int>(pts.size());
        //auto ret = SkGradientShader::MakeLinear(&pts[0], &colors[0], &pos[0], count, mode, flags, localMatrix);
        //return ret.release();
        return SkGradientShader::MakeLinear(&pts[0], &colors[0], &pos[0], count, mode, flags, localMatrix);
    }
    , py::arg("pts")
    , py::arg("colors")
    //, py::arg("pos")
    //, py::arg("pos") = nullptr
    , py::arg("pos") = std::vector<SkScalar>()
    //, py::arg("mode")
    //, py::arg("mode") = SkTileMode::kClamp
    , py::arg_v("mode", SkTileMode::kClamp, "skia.TileMode.K_CLAMP")
    , py::arg("flags") = 0
    , py::arg("local_matrix") = nullptr
    //, py::return_value_policy::automatic_reference)
    //, py::return_value_policy::reference
    //, py::return_value_policy::take_ownership
    //, py::return_value_policy::reference_internal
    //, py::return_value_policy::copy
    //, py::return_value_policy::move
    )

    .def_static("make_radial",
        [] (const SkPoint& center, SkScalar radius,
            const std::vector<SkColor>& colors,
            const std::vector<SkScalar>& pos,
            SkTileMode mode, uint32_t flags,
            const SkMatrix* localMatrix) {
            if (colors.size() < 2)
                throw std::runtime_error("length of colors must be 2 or more.");
            /*
            auto ret = SkGradientShader::MakeRadial(
                center, radius, &colors[0], &pos[0],
                colors.size(), mode, flags, localMatrix);
            return ret.release();
            */
           return SkGradientShader::MakeRadial(
                center, radius, &colors[0], &pos[0],
                colors.size(), mode, flags, localMatrix);
        },
        py::arg("center"), py::arg("radius"), py::arg("colors"),
        py::arg("pos") = std::vector<SkScalar>(),
        py::arg_v("mode", SkTileMode::kClamp, "skia.TileMode.kClamp"),
        py::arg("flags") = 0, py::arg("localMatrix") = nullptr)

    .def_static("make_two_point_conical",
        [] (const SkPoint& start, float startRadius,
            const SkPoint& end, float endRadius,
            const std::vector<SkColor>& colors,
            const std::vector<SkScalar>& pos,
            SkTileMode mode, uint32_t flags,
            const SkMatrix* localMatrix) {
            if (colors.size() < 2)
                throw std::runtime_error("length of colors must be 2 or more.");
            /*
            auto ret = SkGradientShader::MakeTwoPointConical(
                start, startRadius, end, endRadius,
                &colors[0], &pos[0], colors.size(),
                mode, flags, localMatrix);
            return ret.release();
            */
            return SkGradientShader::MakeTwoPointConical(
                start, startRadius, end, endRadius,
                &colors[0], &pos[0], colors.size(),
                mode, flags, localMatrix);
        },
        py::arg("start"), py::arg("startRadius"),
        py::arg("end"), py::arg("endRadius"),
        py::arg("colors"),
        py::arg("pos") = std::vector<SkScalar>(),
        py::arg_v("mode", SkTileMode::kClamp, "skia.TileMode.kClamp"),
        py::arg("flags") = 0,
        py::arg("localMatrix") = nullptr)

    .def_static("make_sweep",
        [] (float cx, float cy,
            const std::vector<SkColor>& colors,
            const std::vector<SkScalar>& pos,
            SkTileMode mode, float startAngle,
            float endAngle, uint32_t flags,
            const SkMatrix* localMatrix) {
            if (colors.size() < 2)
                throw std::runtime_error("length of colors must be 2 or more.");
            /*
            auto ret = SkGradientShader::MakeSweep(
                cx, cy, &colors[0], &pos[0],
                colors.size(), mode, startAngle,
                endAngle, flags, localMatrix);
            return ret.release();
            */
            return SkGradientShader::MakeSweep(
                cx, cy, &colors[0], &pos[0],
                colors.size(), mode, startAngle,
                endAngle, flags, localMatrix);
        },
        py::arg("cx"), py::arg("cy"), py::arg("colors"),
        py::arg("pos") = std::vector<SkScalar>(),
        py::arg_v("mode", SkTileMode::kClamp, "skia.TileMode.kClamp"),
        py::arg("startAngle") = 0.0f,
        py::arg("endAngle") = 360.0f,
        py::arg("flags") = 0,
        py::arg("localMatrix") = nullptr)
    ;
    PYEXTEND_END
}
