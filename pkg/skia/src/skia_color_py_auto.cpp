#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/conversions.h>

#include <include/core/SkColor.h>


namespace py = pybind11;

void init_skia_color_py_auto(py::module &_skia, Registry &registry) {
    _skia
    .def("color_set_argb", &SkColorSetARGB
        , py::arg("a")
        , py::arg("r")
        , py::arg("g")
        , py::arg("b")
        , py::return_value_policy::automatic_reference)
    .def("color_set_a", &SkColorSetA
        , py::arg("c")
        , py::arg("a")
        , py::return_value_policy::automatic_reference)
    .def("rgb_to_hsv", [](unsigned int red, unsigned int green, unsigned int blue, std::array<SkScalar, 3>& hsv)
        {
            SkRGBToHSV(red, green, blue, &hsv[0]);
            return hsv;
        }
        , py::arg("red")
        , py::arg("green")
        , py::arg("blue")
        , py::arg("hsv")
        , py::return_value_policy::automatic_reference)
    .def("color_to_hsv", [](unsigned int color, std::array<SkScalar, 3>& hsv)
        {
            SkColorToHSV(color, &hsv[0]);
            return hsv;
        }
        , py::arg("color")
        , py::arg("hsv")
        , py::return_value_policy::automatic_reference)
    .def("pre_multiply_argb", &SkPreMultiplyARGB
        , py::arg("a")
        , py::arg("r")
        , py::arg("g")
        , py::arg("b")
        , py::return_value_policy::automatic_reference)
    .def("pre_multiply_color", &SkPreMultiplyColor
        , py::arg("c")
        , py::return_value_policy::automatic_reference)
    ;

    py::enum_<SkColorChannel>(_skia, "ColorChannel", py::arithmetic())
        .value("K_R", SkColorChannel::kR)
        .value("K_G", SkColorChannel::kG)
        .value("K_B", SkColorChannel::kB)
        .value("K_A", SkColorChannel::kA)
        .value("K_LAST_ENUM", SkColorChannel::kLastEnum)
        .export_values()
    ;

    py::enum_<SkColorChannelFlag>(_skia, "ColorChannelFlag", py::arithmetic())
        .value("K_RED_SK_COLOR_CHANNEL_FLAG", SkColorChannelFlag::kRed_SkColorChannelFlag)
        .value("K_GREEN_SK_COLOR_CHANNEL_FLAG", SkColorChannelFlag::kGreen_SkColorChannelFlag)
        .value("K_BLUE_SK_COLOR_CHANNEL_FLAG", SkColorChannelFlag::kBlue_SkColorChannelFlag)
        .value("K_ALPHA_SK_COLOR_CHANNEL_FLAG", SkColorChannelFlag::kAlpha_SkColorChannelFlag)
        .value("K_GRAY_SK_COLOR_CHANNEL_FLAG", SkColorChannelFlag::kGray_SkColorChannelFlag)
        .value("K_GRAY_ALPHA_SK_COLOR_CHANNEL_FLAGS", SkColorChannelFlag::kGrayAlpha_SkColorChannelFlags)
        .value("K_RG_SK_COLOR_CHANNEL_FLAGS", SkColorChannelFlag::kRG_SkColorChannelFlags)
        .value("K_RGB_SK_COLOR_CHANNEL_FLAGS", SkColorChannelFlag::kRGB_SkColorChannelFlags)
        .value("K_RGBA_SK_COLOR_CHANNEL_FLAGS", SkColorChannelFlag::kRGBA_SkColorChannelFlags)
        .export_values()
    ;


}