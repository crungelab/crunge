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
    py::class_<SkFontMetrics> _FontMetrics(_skia, "FontMetrics");
    registry.on(_skia, "FontMetrics", _FontMetrics);
        py::enum_<SkFontMetrics::FontMetricsFlags>(_FontMetrics, "FontMetricsFlags", py::arithmetic())
            .value("K_UNDERLINE_THICKNESS_IS_VALID_FLAG", SkFontMetrics::FontMetricsFlags::kUnderlineThicknessIsValid_Flag)
            .value("K_UNDERLINE_POSITION_IS_VALID_FLAG", SkFontMetrics::FontMetricsFlags::kUnderlinePositionIsValid_Flag)
            .value("K_STRIKEOUT_THICKNESS_IS_VALID_FLAG", SkFontMetrics::FontMetricsFlags::kStrikeoutThicknessIsValid_Flag)
            .value("K_STRIKEOUT_POSITION_IS_VALID_FLAG", SkFontMetrics::FontMetricsFlags::kStrikeoutPositionIsValid_Flag)
            .value("K_BOUNDS_INVALID_FLAG", SkFontMetrics::FontMetricsFlags::kBoundsInvalid_Flag)
            .export_values()
        ;
        _FontMetrics
        .def_readwrite("f_flags", &SkFontMetrics::fFlags)
        .def_readwrite("f_top", &SkFontMetrics::fTop)
        .def_readwrite("f_ascent", &SkFontMetrics::fAscent)
        .def_readwrite("f_descent", &SkFontMetrics::fDescent)
        .def_readwrite("f_bottom", &SkFontMetrics::fBottom)
        .def_readwrite("f_leading", &SkFontMetrics::fLeading)
        .def_readwrite("f_avg_char_width", &SkFontMetrics::fAvgCharWidth)
        .def_readwrite("f_max_char_width", &SkFontMetrics::fMaxCharWidth)
        .def_readwrite("f_x_min", &SkFontMetrics::fXMin)
        .def_readwrite("f_x_max", &SkFontMetrics::fXMax)
        .def_readwrite("f_x_height", &SkFontMetrics::fXHeight)
        .def_readwrite("f_cap_height", &SkFontMetrics::fCapHeight)
        .def_readwrite("f_underline_thickness", &SkFontMetrics::fUnderlineThickness)
        .def_readwrite("f_underline_position", &SkFontMetrics::fUnderlinePosition)
        .def_readwrite("f_strikeout_thickness", &SkFontMetrics::fStrikeoutThickness)
        .def_readwrite("f_strikeout_position", &SkFontMetrics::fStrikeoutPosition)
        .def("has_underline_thickness", [](SkFontMetrics& self, SkScalar * thickness)
            {
                auto _ret = self.hasUnderlineThickness(thickness);
                return std::make_tuple(_ret, thickness);
            }
            , py::arg("thickness")
            )
        .def("has_underline_position", [](SkFontMetrics& self, SkScalar * position)
            {
                auto _ret = self.hasUnderlinePosition(position);
                return std::make_tuple(_ret, position);
            }
            , py::arg("position")
            )
        .def("has_strikeout_thickness", [](SkFontMetrics& self, SkScalar * thickness)
            {
                auto _ret = self.hasStrikeoutThickness(thickness);
                return std::make_tuple(_ret, thickness);
            }
            , py::arg("thickness")
            )
        .def("has_strikeout_position", [](SkFontMetrics& self, SkScalar * position)
            {
                auto _ret = self.hasStrikeoutPosition(position);
                return std::make_tuple(_ret, position);
            }
            , py::arg("position")
            )
        .def("has_bounds", &SkFontMetrics::hasBounds
            )
        .def(py::init<>())
    ;


    py::class_<SkFont> _Font(_skia, "Font");
    registry.on(_skia, "Font", _Font);
        py::enum_<SkFont::Edging>(_Font, "Edging", py::arithmetic())
            .value("K_ALIAS", SkFont::Edging::kAlias)
            .value("K_ANTI_ALIAS", SkFont::Edging::kAntiAlias)
            .value("K_SUBPIXEL_ANTI_ALIAS", SkFont::Edging::kSubpixelAntiAlias)
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
            , py::return_value_policy::reference)
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