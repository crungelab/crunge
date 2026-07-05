#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/effects/SkGradient.h>
#include <include/core/SkMatrix.h>


namespace py = pybind11;

void init_skia_gradient_py_auto(py::module &_skia, Registry &registry) {
    py::class_<SkGradient> _Gradient(_skia, "Gradient");
    registry.on(_skia, "Gradient", _Gradient);
        py::class_<SkGradient::Interpolation> _GradientInterpolation(_skia, "GradientInterpolation");
        registry.on(_skia, "GradientInterpolation", _GradientInterpolation);
            py::enum_<SkGradient::Interpolation::InPremul>(_GradientInterpolation, "InPremul", py::arithmetic())
                .value("K_NO", SkGradient::Interpolation::InPremul::kNo)
                .value("K_YES", SkGradient::Interpolation::InPremul::kYes)
                .export_values()
            ;
            py::enum_<SkGradient::Interpolation::ColorSpace>(_GradientInterpolation, "ColorSpace", py::arithmetic())
                .value("K_DESTINATION", SkGradient::Interpolation::ColorSpace::kDestination)
                .value("K_SRGB_LINEAR", SkGradient::Interpolation::ColorSpace::kSRGBLinear)
                .value("K_LAB", SkGradient::Interpolation::ColorSpace::kLab)
                .value("K_OK_LAB", SkGradient::Interpolation::ColorSpace::kOKLab)
                .value("K_OK_LAB_GAMUT_MAP", SkGradient::Interpolation::ColorSpace::kOKLabGamutMap)
                .value("K_LCH", SkGradient::Interpolation::ColorSpace::kLCH)
                .value("K_OKLCH", SkGradient::Interpolation::ColorSpace::kOKLCH)
                .value("K_OKLCH_GAMUT_MAP", SkGradient::Interpolation::ColorSpace::kOKLCHGamutMap)
                .value("K_SRGB", SkGradient::Interpolation::ColorSpace::kSRGB)
                .value("K_HSL", SkGradient::Interpolation::ColorSpace::kHSL)
                .value("K_HWB", SkGradient::Interpolation::ColorSpace::kHWB)
                .value("K_DISPLAY_P3", SkGradient::Interpolation::ColorSpace::kDisplayP3)
                .value("K_REC2020", SkGradient::Interpolation::ColorSpace::kRec2020)
                .value("K_PROPHOTO_RGB", SkGradient::Interpolation::ColorSpace::kProphotoRGB)
                .value("K_A98_RGB", SkGradient::Interpolation::ColorSpace::kA98RGB)
                .value("K_LAST_COLOR_SPACE", SkGradient::Interpolation::ColorSpace::kLastColorSpace)
                .export_values()
            ;
            py::enum_<SkGradient::Interpolation::HueMethod>(_GradientInterpolation, "HueMethod", py::arithmetic())
                .value("K_SHORTER", SkGradient::Interpolation::HueMethod::kShorter)
                .value("K_LONGER", SkGradient::Interpolation::HueMethod::kLonger)
                .value("K_INCREASING", SkGradient::Interpolation::HueMethod::kIncreasing)
                .value("K_DECREASING", SkGradient::Interpolation::HueMethod::kDecreasing)
                .value("K_LAST_HUE_METHOD", SkGradient::Interpolation::HueMethod::kLastHueMethod)
                .export_values()
            ;
            _GradientInterpolation
            .def_readwrite("f_in_premul", &SkGradient::Interpolation::fInPremul)
            .def_readwrite("f_color_space", &SkGradient::Interpolation::fColorSpace)
            .def_readwrite("f_hue_method", &SkGradient::Interpolation::fHueMethod)
            .def_static("from_flags", &SkGradient::Interpolation::FromFlags
                , py::arg("flags")
                )
        ;

        py::class_<SkGradient::Colors> _GradientColors(_skia, "GradientColors");
        registry.on(_skia, "GradientColors", _GradientColors);
            _GradientColors
            .def(py::init<>())
            .def(py::init<SkSpan<const SkColor4f>, SkSpan<const float>, SkTileMode, sk_sp<SkColorSpace>>()
            , py::arg("colors")
            , py::arg("pos")
            , py::arg("mode")
            , py::arg("cs") = nullptr
            )
            .def(py::init<SkSpan<const SkColor4f>, SkTileMode, sk_sp<SkColorSpace>>()
            , py::arg("colors")
            , py::arg("tm")
            , py::arg("cs") = nullptr
            )
            .def("colors", &SkGradient::Colors::colors
                )
            .def("positions", &SkGradient::Colors::positions
                )
            .def("color_space", &SkGradient::Colors::colorSpace
                )
            .def("tile_mode", &SkGradient::Colors::tileMode
                )
        ;

        _Gradient
        .def(py::init<>())
        .def(py::init<const SkGradient::Colors &, const SkGradient::Interpolation &>()
        , py::arg("colors")
        , py::arg("interp")
        )
        .def("colors", &SkGradient::colors
            )
        .def("interpolation", &SkGradient::interpolation
            )
    ;

    _skia
    .def("linear_gradient", [](std::array<SkPoint, 2>& pts, const SkGradient & arg1, const SkMatrix * lm)
        {
            return SkShaders::LinearGradient(&pts[0], arg1, lm);
        }
        , py::arg("pts")
        , py::arg("arg1")
        , py::arg("lm") = nullptr
        )
    .def("radial_gradient", &SkShaders::RadialGradient
        , py::arg("center")
        , py::arg("radius")
        , py::arg("grad")
        , py::arg("lm") = nullptr
        )
    .def("two_point_conical_gradient", &SkShaders::TwoPointConicalGradient
        , py::arg("start")
        , py::arg("start_radius")
        , py::arg("end")
        , py::arg("end_radius")
        , py::arg("grad")
        , py::arg("lm") = nullptr
        )
    .def("sweep_gradient", py::overload_cast<SkPoint, float, float, const SkGradient &, const SkMatrix *>(&SkShaders::SweepGradient)
        , py::arg("center")
        , py::arg("start_angle")
        , py::arg("end_angle")
        , py::arg("arg3")
        , py::arg("lm") = nullptr
        )
    ;


}