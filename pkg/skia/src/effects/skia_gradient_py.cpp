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

sk_sp<SkShader> CreateLinearGradient(SkPoint p0, SkPoint p1,
                                     std::vector<SkColor4f> colors,
                                     std::vector<SkScalar> pos, SkTileMode mode,
                                     sk_sp<SkColorSpace> cs,
                                     SkGradient::Interpolation interp,
                                     const SkMatrix *lm = nullptr) {
    SkPoint pts[2] = {p0, p1};

    SkGradient::Colors gcolors(
        SkSpan<const SkColor4f>(colors.data(), colors.size()),
        SkSpan<const SkScalar>(pos.data(), pos.size()), mode, std::move(cs));

    SkGradient grad(gcolors, interp);

    return SkShaders::LinearGradient(pts, grad, lm);
}

sk_sp<SkShader> CreateRadialGradient(SkPoint center, float radius,
                                     std::vector<SkColor4f> colors,
                                     std::vector<SkScalar> pos, SkTileMode mode,
                                     sk_sp<SkColorSpace> cs,
                                     SkGradient::Interpolation interp,
                                     const SkMatrix *lm = nullptr) {
    SkGradient::Colors gcolors(
        SkSpan<const SkColor4f>(colors.data(), colors.size()),
        SkSpan<const SkScalar>(pos.data(), pos.size()), mode, std::move(cs));

    SkGradient grad(gcolors, interp);

    return SkShaders::RadialGradient(center, radius, grad, lm);
}

sk_sp<SkShader> CreateTwoPointConicalGradient(
    SkPoint start, float startRadius, SkPoint end, float endRadius,
    std::vector<SkColor4f> colors, std::vector<SkScalar> pos, SkTileMode mode,
    sk_sp<SkColorSpace> cs, SkGradient::Interpolation interp,
    const SkMatrix *lm = nullptr) {
    SkGradient::Colors gcolors(
        SkSpan<const SkColor4f>(colors.data(), colors.size()),
        SkSpan<const SkScalar>(pos.data(), pos.size()), mode, std::move(cs));

    SkGradient grad(gcolors, interp);

    return SkShaders::TwoPointConicalGradient(start, startRadius, end,
                                              endRadius, grad, lm);
}

sk_sp<SkShader>
CreateSweepGradient(SkPoint center, std::vector<SkColor4f> colors,
                    std::vector<SkScalar> pos, SkTileMode mode,
                    sk_sp<SkColorSpace> cs, SkGradient::Interpolation interp,
                    float startAngle = 0.0f, float endAngle = 360.0f,
                    const SkMatrix *lm = nullptr) {
    SkGradient::Colors gcolors(
        SkSpan<const SkColor4f>(colors.data(), colors.size()),
        SkSpan<const SkScalar>(pos.data(), pos.size()), mode, std::move(cs));
    SkGradient grad(gcolors, interp);
    return SkShaders::SweepGradient(center, startAngle, endAngle, grad, lm);
}

void init_skia_gradient_py(py::module &_skia, Registry &registry) {
    _skia.def("create_linear_gradient", &CreateLinearGradient, py::arg("p0"),
              py::arg("p1"), py::arg("colors"),
              py::arg("pos") = std::vector<SkScalar>(),
              py::arg("mode") = SkTileMode::kClamp, py::arg("cs") = nullptr,
              py::arg("interpolation") = SkGradient::Interpolation{},
              py::arg("local_matrix") = nullptr);

    _skia.def("create_radial_gradient", &CreateRadialGradient,
              py::arg("center"), py::arg("radius"), py::arg("colors"),
              py::arg("pos") = std::vector<SkScalar>(),
              py::arg("mode") = SkTileMode::kClamp, py::arg("cs") = nullptr,
              py::arg("interpolation") = SkGradient::Interpolation{},
              py::arg("local_matrix") = nullptr);

    _skia.def("create_two_point_conical_gradient",
              &CreateTwoPointConicalGradient, py::arg("start"),
              py::arg("start_radius"), py::arg("end"), py::arg("end_radius"),
              py::arg("colors"), py::arg("pos") = std::vector<SkScalar>(),
              py::arg("mode") = SkTileMode::kClamp, py::arg("cs") = nullptr,
              py::arg("interpolation") = SkGradient::Interpolation{},
              py::arg("local_matrix") = nullptr);

    _skia.def("create_sweep_gradient", &CreateSweepGradient, py::arg("center"),
              py::arg("colors"), py::arg("pos") = std::vector<SkScalar>(),
              py::arg("mode") = SkTileMode::kClamp, py::arg("cs") = nullptr,
              py::arg("interpolation") = SkGradient::Interpolation{},
              py::arg("start_angle") = 0.0f, py::arg("end_angle") = 360.0f,
              py::arg("local_matrix") = nullptr);

    PYEXTEND_BEGIN(SkGradient::Interpolation, GradientInterpolation)
    _GradientInterpolation.def(py::init<>());
    PYEXTEND_END
}
