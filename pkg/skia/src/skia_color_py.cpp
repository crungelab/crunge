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

/*
constexpr SkAlpha SK_AlphaTRANSPARENT = 0x00;

constexpr SkAlpha SK_AlphaOPAQUE      = 0xFF;

constexpr SkColor SK_ColorTRANSPARENT = SkColorSetARGB(0x00, 0x00, 0x00, 0x00);

constexpr SkColor SK_ColorBLACK       = SkColorSetARGB(0xFF, 0x00, 0x00, 0x00);

constexpr SkColor SK_ColorDKGRAY      = SkColorSetARGB(0xFF, 0x44, 0x44, 0x44);

constexpr SkColor SK_ColorGRAY        = SkColorSetARGB(0xFF, 0x88, 0x88, 0x88);

constexpr SkColor SK_ColorLTGRAY      = SkColorSetARGB(0xFF, 0xCC, 0xCC, 0xCC);

constexpr SkColor SK_ColorWHITE       = SkColorSetARGB(0xFF, 0xFF, 0xFF, 0xFF);

constexpr SkColor SK_ColorRED         = SkColorSetARGB(0xFF, 0xFF, 0x00, 0x00);

constexpr SkColor SK_ColorGREEN       = SkColorSetARGB(0xFF, 0x00, 0xFF, 0x00);

constexpr SkColor SK_ColorBLUE        = SkColorSetARGB(0xFF, 0x00, 0x00, 0xFF);

constexpr SkColor SK_ColorYELLOW      = SkColorSetARGB(0xFF, 0xFF, 0xFF, 0x00);

constexpr SkColor SK_ColorCYAN        = SkColorSetARGB(0xFF, 0x00, 0xFF, 0xFF);

constexpr SkColor SK_ColorMAGENTA     = SkColorSetARGB(0xFF, 0xFF, 0x00, 0xFF);

*/


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
}
