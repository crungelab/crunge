#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/core/SkFontTypes.h>


namespace py = pybind11;

void init_skia_font_types_py_auto(py::module &_skia, Registry &registry) {
    py::enum_<SkTextEncoding>(_skia, "TextEncoding", py::arithmetic())
        .value("K_UTF8", SkTextEncoding::kUTF8)
        .value("K_UTF16", SkTextEncoding::kUTF16)
        .value("K_UTF32", SkTextEncoding::kUTF32)
        .value("K_GLYPH_ID", SkTextEncoding::kGlyphID)
        .export_values()
    ;
    py::enum_<SkFontHinting>(_skia, "FontHinting", py::arithmetic())
        .value("K_NONE", SkFontHinting::kNone)
        .value("K_SLIGHT", SkFontHinting::kSlight)
        .value("K_NORMAL", SkFontHinting::kNormal)
        .value("K_FULL", SkFontHinting::kFull)
        .export_values()
    ;

}