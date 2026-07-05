#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/core/SkFont.h>
#include <include/core/SkStrikeRef.h>

#include <include/core/SkPaint.h>
#include <include/core/SkFontMetrics.h>
#include <include/core/SkPath.h>


namespace py = pybind11;

void init_skia_font_py_auto(py::module &_skia, Registry &registry) {
    py::class_<SkFont> _Font(_skia, "Font");
    registry.on(_skia, "Font", _Font);
        py::enum_<SkFont::Edging>(_Font, "Edging", py::arithmetic())
            .value("K_ALIAS", SkFont::Edging::kAlias)
            .value("K_ANTI_ALIAS", SkFont::Edging::kAntiAlias)
            .value("K_SUBPIXEL_ANTI_ALIAS", SkFont::Edging::kSubpixelAntiAlias)
            .export_values()
        ;
        _Font
        .def("is_force_auto_hinting", &SkFont::isForceAutoHinting
            )
        .def("is_embedded_bitmaps", &SkFont::isEmbeddedBitmaps
            )
        .def("is_subpixel", &SkFont::isSubpixel
            )
        .def("is_linear_metrics", &SkFont::isLinearMetrics
            )
        .def("is_embolden", &SkFont::isEmbolden
            )
        .def("is_baseline_snap", &SkFont::isBaselineSnap
            )
        .def("set_force_auto_hinting", &SkFont::setForceAutoHinting
            , py::arg("force_auto_hinting")
            )
        .def("set_embedded_bitmaps", &SkFont::setEmbeddedBitmaps
            , py::arg("embedded_bitmaps")
            )
        .def("set_subpixel", &SkFont::setSubpixel
            , py::arg("subpixel")
            )
        .def("set_linear_metrics", &SkFont::setLinearMetrics
            , py::arg("linear_metrics")
            )
        .def("set_embolden", &SkFont::setEmbolden
            , py::arg("embolden")
            )
        .def("set_baseline_snap", &SkFont::setBaselineSnap
            , py::arg("baseline_snap")
            )
        .def("get_edging", &SkFont::getEdging
            )
        .def("set_edging", &SkFont::setEdging
            , py::arg("edging")
            )
        .def("set_hinting", &SkFont::setHinting
            , py::arg("hinting_level")
            )
        .def("get_hinting", &SkFont::getHinting
            )
        .def("make_with_size", &SkFont::makeWithSize
            , py::arg("size")
            )
        .def("get_typeface", &SkFont::getTypeface
            )
        .def("get_size", &SkFont::getSize
            )
        .def("get_scale_x", &SkFont::getScaleX
            )
        .def("get_skew_x", &SkFont::getSkewX
            )
        .def("ref_typeface", &SkFont::refTypeface
            )
        .def("set_typeface", &SkFont::setTypeface
            , py::arg("tf")
            )
        .def("set_size", &SkFont::setSize
            , py::arg("text_size")
            )
        .def("set_scale_x", &SkFont::setScaleX
            , py::arg("scale_x")
            )
        .def("set_skew_x", &SkFont::setSkewX
            , py::arg("skew_x")
            )
        .def("text_to_glyphs", &SkFont::textToGlyphs
            , py::arg("text")
            , py::arg("byte_length")
            , py::arg("encoding")
            , py::arg("glyphs")
            )
        .def("unichar_to_glyph", &SkFont::unicharToGlyph
            , py::arg("uni")
            )
        .def("unichars_to_glyphs", &SkFont::unicharsToGlyphs
            , py::arg("src")
            , py::arg("dst")
            )
        .def("count_text", &SkFont::countText
            , py::arg("text")
            , py::arg("byte_length")
            , py::arg("encoding")
            )
        .def("measure_text", py::overload_cast<const void *, size_t, SkTextEncoding, SkRect *>(&SkFont::measureText, py::const_)
            , py::arg("text")
            , py::arg("byte_length")
            , py::arg("encoding")
            , py::arg("bounds") = nullptr
            )
        .def("measure_text", py::overload_cast<const void *, size_t, SkTextEncoding, SkRect *, const SkPaint *>(&SkFont::measureText, py::const_)
            , py::arg("text")
            , py::arg("byte_length")
            , py::arg("encoding")
            , py::arg("bounds")
            , py::arg("paint")
            )
        .def("make_strike_ref", &SkFont::makeStrikeRef
            )
        .def("get_widths_bounds", &SkFont::getWidthsBounds
            , py::arg("glyphs")
            , py::arg("widths")
            , py::arg("bounds")
            , py::arg("paint")
            )
        .def("get_widths", &SkFont::getWidths
            , py::arg("glyphs")
            , py::arg("widths")
            )
        .def("get_width", &SkFont::getWidth
            , py::arg("glyph")
            )
        .def("get_bounds", py::overload_cast<SkSpan<const SkGlyphID>, SkSpan<SkRect>, const SkPaint *>(&SkFont::getBounds, py::const_)
            , py::arg("glyphs")
            , py::arg("bounds")
            , py::arg("paint")
            )
        .def("get_bounds", py::overload_cast<SkGlyphID, const SkPaint *>(&SkFont::getBounds, py::const_)
            , py::arg("glyph")
            , py::arg("paint")
            )
        .def("get_pos", &SkFont::getPos
            , py::arg("glyphs")
            , py::arg("pos")
            , py::arg("origin") = SkPoint{0,0}
            )
        .def("get_x_pos", &SkFont::getXPos
            , py::arg("glyphs")
            , py::arg("xpos")
            , py::arg("origin") = 0
            )
        .def("get_intercepts", &SkFont::getIntercepts
            , py::arg("glyphs")
            , py::arg("pos")
            , py::arg("top")
            , py::arg("bottom")
            , py::arg("arg4") = nullptr
            )
        .def("get_path", &SkFont::getPath
            , py::arg("glyph_id")
            )
        .def("get_paths", &SkFont::getPaths
            , py::arg("glyph_i_ds")
            , py::arg("glyph_path_proc") = nullptr
            , py::arg("ctx")
            )
        .def("get_metrics", &SkFont::getMetrics
            , py::arg("metrics")
            )
        .def("get_spacing", &SkFont::getSpacing
            )
        .def("dump", &SkFont::dump
            )
    ;


}