#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/core/SkColor.h>

namespace py = pybind11;

enum class Colors : uint32_t {
    TRANSPARENT = SK_ColorTRANSPARENT,
    BLACK = SK_ColorBLACK,
    DKGRAY = SK_ColorDKGRAY,
    GRAY = SK_ColorGRAY,
    LTGRAY = SK_ColorLTGRAY,
    WHITE = SK_ColorWHITE,
    RED = SK_ColorRED,
    GREEN = SK_ColorGREEN,
    BLUE = SK_ColorBLUE,
    YELLOW = SK_ColorYELLOW,
    CYAN = SK_ColorCYAN,
    MAGENTA = SK_ColorMAGENTA,
};


enum class Colors4f : SkColor4f {
    TRANSPARENT = SkColors::kTransparent,
    BLACK = SkColors::kBlack,
    DKGRAY = SkColors::kDkGray,
    GRAY = SkColors::kGray,
    LTGRAY = SkColors::kLtGray,
    WHITE = SkColors::kWhite,
    RED = SkColors::kRed,
    GREEN = SkColors::kGreen,
    BLUE = SkColors::kBlue,
    YELLOW = SkColors::kYellow,
    CYAN = SkColors::kCyan,
    MAGENTA = SkColors::kMagenta,
};

void init_skia_color_py(py::module &_skia, Registry &registry) {
    py::enum_<Colors>(_skia, "Colors")
        .value("TRANSPARENT", Colors::TRANSPARENT)
        .value("BLACK", Colors::BLACK)
        .value("DKGRAY", Colors::DKGRAY)
        .value("GRAY", Colors::GRAY)
        .value("LTGRAY", Colors::LTGRAY)
        .value("WHITE", Colors::WHITE)
        .value("RED", Colors::RED)
        .value("GREEN", Colors::GREEN)
        .value("BLUE", Colors::BLUE)
        .value("YELLOW", Colors::YELLOW)
        .value("CYAN", Colors::CYAN)
        .value("MAGENTA", Colors::MAGENTA)
        .export_values();

    py::enum_<Colors4f>(_skia, "Colors4f")
        .value("TRANSPARENT", Colors4f::TRANSPARENT)
        .value("BLACK", Colors4f::BLACK)
        .value("DKGRAY", Colors4f::DKGRAY)
        .value("GRAY", Colors4f::GRAY)
        .value("LTGRAY", Colors4f::LTGRAY)
        .value("WHITE", Colors4f::WHITE)
        .value("RED", Colors4f::RED)
        .value("GREEN", Colors4f::GREEN)
        .value("BLUE", Colors4f::BLUE)
        .value("YELLOW", Colors4f::YELLOW)
        .value("CYAN", Colors4f::CYAN)
        .value("MAGENTA", Colors4f::MAGENTA)
        .export_values();
}
