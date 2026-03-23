#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/core/SkPaint.h>
#include <include/core/SkColorSpace.h>
#include <include/core/SkShader.h>
#include <include/core/SkColorFilter.h>
#include <include/core/SkBlender.h>
#include <include/core/SkPathEffect.h>
#include <include/core/SkMaskFilter.h>
#include <include/core/SkImageFilter.h>
#include <include/core/SkRect.h>


namespace py = pybind11;

void init_skia_paint_py_auto(py::module &_skia, Registry &registry) {
    py::class_<SkPaint> _Paint(_skia, "Paint");
    registry.on(_skia, "Paint", _Paint);
        _Paint
        .def(py::init<>())
        .def(py::init<const SkColor4f &, SkColorSpace *>()
        , py::arg("color")
        , py::arg("color_space") = nullptr
        )
        .def("reset", &SkPaint::reset
            )
        .def("is_anti_alias", &SkPaint::isAntiAlias
            )
        .def("set_anti_alias", &SkPaint::setAntiAlias
            , py::arg("aa")
            )
        .def("is_dither", &SkPaint::isDither
            )
        .def("set_dither", &SkPaint::setDither
            , py::arg("dither")
            )
        ;

        py::enum_<SkPaint::Style>(_Paint, "Style", py::arithmetic())
            .value("K_FILL_STYLE", SkPaint::Style::kFill_Style)
            .value("K_STROKE_STYLE", SkPaint::Style::kStroke_Style)
            .value("K_STROKE_AND_FILL_STYLE", SkPaint::Style::kStrokeAndFill_Style)
            .export_values()
        ;
        _Paint
        .def("get_style", &SkPaint::getStyle
            )
        .def("set_style", &SkPaint::setStyle
            , py::arg("style")
            )
        .def("set_stroke", &SkPaint::setStroke
            , py::arg("arg0")
            )
        .def("get_color", &SkPaint::getColor
            )
        .def("get_color4f", &SkPaint::getColor4f
            )
        .def("set_color", py::overload_cast<SkColor>(&SkPaint::setColor)
            , py::arg("color")
            )
        .def("set_color", py::overload_cast<const SkColor4f &, SkColorSpace *>(&SkPaint::setColor)
            , py::arg("color")
            , py::arg("color_space") = nullptr
            )
        .def("set_color4f", &SkPaint::setColor4f
            , py::arg("color")
            , py::arg("color_space") = nullptr
            )
        .def("get_alphaf", &SkPaint::getAlphaf
            )
        .def("get_alpha", &SkPaint::getAlpha
            )
        .def("set_alphaf", &SkPaint::setAlphaf
            , py::arg("a")
            )
        .def("set_alpha", &SkPaint::setAlpha
            , py::arg("a")
            )
        .def("set_argb", &SkPaint::setARGB
            , py::arg("a")
            , py::arg("r")
            , py::arg("g")
            , py::arg("b")
            )
        .def("get_stroke_width", &SkPaint::getStrokeWidth
            )
        .def("set_stroke_width", &SkPaint::setStrokeWidth
            , py::arg("width")
            )
        .def("get_stroke_miter", &SkPaint::getStrokeMiter
            )
        .def("set_stroke_miter", &SkPaint::setStrokeMiter
            , py::arg("miter_limit")
            )
        ;

        py::enum_<SkPaint::Cap>(_Paint, "Cap", py::arithmetic())
            .value("K_BUTT_CAP", SkPaint::Cap::kButt_Cap)
            .value("K_ROUND_CAP", SkPaint::Cap::kRound_Cap)
            .value("K_SQUARE_CAP", SkPaint::Cap::kSquare_Cap)
            .value("K_LAST_CAP", SkPaint::Cap::kLast_Cap)
            .value("K_DEFAULT_CAP", SkPaint::Cap::kDefault_Cap)
            .export_values()
        ;
        py::enum_<SkPaint::Join>(_Paint, "Join", py::arithmetic())
            .value("K_MITER_JOIN", SkPaint::Join::kMiter_Join)
            .value("K_ROUND_JOIN", SkPaint::Join::kRound_Join)
            .value("K_BEVEL_JOIN", SkPaint::Join::kBevel_Join)
            .value("K_LAST_JOIN", SkPaint::Join::kLast_Join)
            .value("K_DEFAULT_JOIN", SkPaint::Join::kDefault_Join)
            .export_values()
        ;
        _Paint
        .def("get_stroke_cap", &SkPaint::getStrokeCap
            )
        .def("set_stroke_cap", &SkPaint::setStrokeCap
            , py::arg("cap")
            )
        .def("get_stroke_join", &SkPaint::getStrokeJoin
            )
        .def("set_stroke_join", &SkPaint::setStrokeJoin
            , py::arg("join")
            )
        .def("get_shader", &SkPaint::getShader
            )
        .def("ref_shader", &SkPaint::refShader
            )
        .def("set_shader", &SkPaint::setShader
            , py::arg("shader")
            )
        .def("get_color_filter", &SkPaint::getColorFilter
            )
        .def("ref_color_filter", &SkPaint::refColorFilter
            )
        .def("set_color_filter", &SkPaint::setColorFilter
            , py::arg("color_filter")
            )
        .def("as_blend_mode", &SkPaint::asBlendMode
            )
        .def("get_blend_mode_or", &SkPaint::getBlendMode_or
            , py::arg("default_mode")
            )
        .def("is_src_over", &SkPaint::isSrcOver
            )
        .def("set_blend_mode", &SkPaint::setBlendMode
            , py::arg("mode")
            )
        .def("get_blender", &SkPaint::getBlender
            )
        .def("ref_blender", &SkPaint::refBlender
            )
        .def("set_blender", &SkPaint::setBlender
            , py::arg("blender")
            )
        .def("get_path_effect", &SkPaint::getPathEffect
            )
        .def("ref_path_effect", &SkPaint::refPathEffect
            )
        .def("set_path_effect", &SkPaint::setPathEffect
            , py::arg("path_effect")
            )
        .def("get_mask_filter", &SkPaint::getMaskFilter
            )
        .def("ref_mask_filter", &SkPaint::refMaskFilter
            )
        .def("set_mask_filter", &SkPaint::setMaskFilter
            , py::arg("mask_filter")
            )
        .def("get_image_filter", &SkPaint::getImageFilter
            )
        .def("ref_image_filter", &SkPaint::refImageFilter
            )
        .def("set_image_filter", &SkPaint::setImageFilter
            , py::arg("image_filter")
            )
        .def("nothing_to_draw", &SkPaint::nothingToDraw
            )
        .def("can_compute_fast_bounds", &SkPaint::canComputeFastBounds
            )
        .def("compute_fast_bounds", &SkPaint::computeFastBounds
            , py::arg("orig")
            , py::arg("storage")
            )
        .def("compute_fast_stroke_bounds", &SkPaint::computeFastStrokeBounds
            , py::arg("orig")
            , py::arg("storage")
            )
        .def("do_compute_fast_bounds", &SkPaint::doComputeFastBounds
            , py::arg("orig")
            , py::arg("storage")
            , py::arg("style")
            )
    ;


}