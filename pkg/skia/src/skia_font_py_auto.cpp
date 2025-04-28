#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/conversions.h>

#include <include/core/SkFont.h>

#include <include/core/SkPaint.h>
#include <include/core/SkFontMetrics.h>
#include <include/core/SkPath.h>


namespace py = pybind11;

void init_skia_font_py_auto(py::module &_skia, Registry &registry) {
    py::class_<SkFont> Font(_skia, "Font");
    registry.on(_skia, "Font", Font);
    Font
        ;

        py::enum_<SkFont::Edging>(_skia, "Edging", py::arithmetic())
            .value("K_ALIAS", SkFont::Edging::kAlias)
            .value("K_ANTI_ALIAS", SkFont::Edging::kAntiAlias)
            .value("K_SUBPIXEL_ANTI_ALIAS", SkFont::Edging::kSubpixelAntiAlias)
            .export_values()
        ;

        Font
        .def("is_force_auto_hinting", &SkFont::isForceAutoHinting
            , py::return_value_policy::automatic_reference)
        .def("is_embedded_bitmaps", &SkFont::isEmbeddedBitmaps
            , py::return_value_policy::automatic_reference)
        .def("is_subpixel", &SkFont::isSubpixel
            , py::return_value_policy::automatic_reference)
        .def("is_linear_metrics", &SkFont::isLinearMetrics
            , py::return_value_policy::automatic_reference)
        .def("is_embolden", &SkFont::isEmbolden
            , py::return_value_policy::automatic_reference)
        .def("is_baseline_snap", &SkFont::isBaselineSnap
            , py::return_value_policy::automatic_reference)
        .def("set_force_auto_hinting", &SkFont::setForceAutoHinting
            , py::arg("force_auto_hinting")
            , py::return_value_policy::automatic_reference)
        .def("set_embedded_bitmaps", &SkFont::setEmbeddedBitmaps
            , py::arg("embedded_bitmaps")
            , py::return_value_policy::automatic_reference)
        .def("set_subpixel", &SkFont::setSubpixel
            , py::arg("subpixel")
            , py::return_value_policy::automatic_reference)
        .def("set_linear_metrics", &SkFont::setLinearMetrics
            , py::arg("linear_metrics")
            , py::return_value_policy::automatic_reference)
        .def("set_embolden", &SkFont::setEmbolden
            , py::arg("embolden")
            , py::return_value_policy::automatic_reference)
        .def("set_baseline_snap", &SkFont::setBaselineSnap
            , py::arg("baseline_snap")
            , py::return_value_policy::automatic_reference)
        .def("get_edging", &SkFont::getEdging
            , py::return_value_policy::automatic_reference)
        .def("set_edging", &SkFont::setEdging
            , py::arg("edging")
            , py::return_value_policy::automatic_reference)
        .def("set_hinting", &SkFont::setHinting
            , py::arg("hinting_level")
            , py::return_value_policy::automatic_reference)
        .def("get_hinting", &SkFont::getHinting
            , py::return_value_policy::automatic_reference)
        .def("make_with_size", &SkFont::makeWithSize
            , py::arg("size")
            , py::return_value_policy::automatic_reference)
        .def("get_typeface", &SkFont::getTypeface
            , py::return_value_policy::automatic_reference)
        .def("get_size", &SkFont::getSize
            , py::return_value_policy::automatic_reference)
        .def("get_scale_x", &SkFont::getScaleX
            , py::return_value_policy::automatic_reference)
        .def("get_skew_x", &SkFont::getSkewX
            , py::return_value_policy::automatic_reference)
        .def("ref_typeface", &SkFont::refTypeface
            , py::return_value_policy::automatic_reference)
        .def("set_typeface", &SkFont::setTypeface
            , py::arg("tf")
            , py::return_value_policy::automatic_reference)
        .def("set_size", &SkFont::setSize
            , py::arg("text_size")
            , py::return_value_policy::automatic_reference)
        .def("set_scale_x", &SkFont::setScaleX
            , py::arg("scale_x")
            , py::return_value_policy::automatic_reference)
        .def("set_skew_x", &SkFont::setSkewX
            , py::arg("skew_x")
            , py::return_value_policy::automatic_reference)
        .def("text_to_glyphs", &SkFont::textToGlyphs
            , py::arg("text")
            , py::arg("byte_length")
            , py::arg("encoding")
            , py::arg("glyphs")
            , py::arg("max_glyph_count")
            , py::return_value_policy::automatic_reference)
        .def("unichar_to_glyph", &SkFont::unicharToGlyph
            , py::arg("uni")
            , py::return_value_policy::automatic_reference)
        .def("unichars_to_glyphs", &SkFont::unicharsToGlyphs
            , py::arg("uni")
            , py::arg("count")
            , py::arg("glyphs")
            , py::return_value_policy::automatic_reference)
        .def("count_text", &SkFont::countText
            , py::arg("text")
            , py::arg("byte_length")
            , py::arg("encoding")
            , py::return_value_policy::automatic_reference)
        .def("measure_text", py::overload_cast<const void *, unsigned long, SkTextEncoding, SkRect *>(&SkFont::measureText, py::const_)
            , py::arg("text")
            , py::arg("byte_length")
            , py::arg("encoding")
            , py::arg("bounds") = nullptr
            , py::return_value_policy::automatic_reference)
        .def("get_widths", py::overload_cast<const unsigned short[], int, float[], SkRect[]>(&SkFont::getWidths, py::const_)
            , py::arg("glyphs")
            , py::arg("count")
            , py::arg("widths")
            , py::arg("bounds")
            , py::return_value_policy::automatic_reference)
        .def("get_widths_bounds", &SkFont::getWidthsBounds
            , py::arg("glyphs")
            , py::arg("count")
            , py::arg("widths")
            , py::arg("bounds")
            , py::arg("paint")
            , py::return_value_policy::automatic_reference)
        .def("get_bounds", &SkFont::getBounds
            , py::arg("glyphs")
            , py::arg("count")
            , py::arg("bounds")
            , py::arg("paint")
            , py::return_value_policy::automatic_reference)
        .def("get_pos", &SkFont::getPos
            , py::arg("glyphs")
            , py::arg("count")
            , py::arg("pos")
            , py::arg("origin") = SkPoint{0,0}
            , py::return_value_policy::automatic_reference)
        .def("get_x_pos", &SkFont::getXPos
            , py::arg("glyphs")
            , py::arg("count")
            , py::arg("xpos")
            , py::arg("origin") = 0
            , py::return_value_policy::automatic_reference)
        .def("get_intercepts", &SkFont::getIntercepts
            , py::arg("glyphs")
            , py::arg("count")
            , py::arg("pos")
            , py::arg("top")
            , py::arg("bottom")
            , py::arg("") = nullptr
            , py::return_value_policy::automatic_reference)
        .def("get_path", &SkFont::getPath
            , py::arg("glyph_id")
            , py::arg("path")
            , py::return_value_policy::automatic_reference)
        .def("get_metrics", &SkFont::getMetrics
            , py::arg("metrics")
            , py::return_value_policy::automatic_reference)
        .def("get_spacing", &SkFont::getSpacing
            , py::return_value_policy::automatic_reference)
        .def("dump", &SkFont::dump
            , py::return_value_policy::automatic_reference)
    ;


}