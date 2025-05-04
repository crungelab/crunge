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
    py::class_<SkPaint> Paint(_skia, "Paint");
    registry.on(_skia, "Paint", Paint);
        Paint
        .def(py::init<>())
        .def(py::init<const SkRGBA4f<kUnpremul_SkAlphaType> &, SkColorSpace *>()
        , py::arg("color")
        , py::arg("color_space") = nullptr
        )
        .def(py::init<const SkPaint &>()
        , py::arg("paint")
        )
        .def("reset", &SkPaint::reset
            , py::return_value_policy::automatic_reference)
        .def("is_anti_alias", &SkPaint::isAntiAlias
            , py::return_value_policy::automatic_reference)
        .def("set_anti_alias", &SkPaint::setAntiAlias
            , py::arg("aa")
            , py::return_value_policy::automatic_reference)
        .def("is_dither", &SkPaint::isDither
            , py::return_value_policy::automatic_reference)
        .def("set_dither", &SkPaint::setDither
            , py::arg("dither")
            , py::return_value_policy::automatic_reference)
        ;

        py::enum_<SkPaint::Style>(Paint, "Style", py::arithmetic())
            .value("K_FILL_STYLE", SkPaint::Style::kFill_Style)
            .value("K_STROKE_STYLE", SkPaint::Style::kStroke_Style)
            .value("K_STROKE_AND_FILL_STYLE", SkPaint::Style::kStrokeAndFill_Style)
            .export_values()
        ;
        Paint
        .def("get_style", &SkPaint::getStyle
            , py::return_value_policy::automatic_reference)
        .def("set_style", &SkPaint::setStyle
            , py::arg("style")
            , py::return_value_policy::automatic_reference)
        .def("set_stroke", &SkPaint::setStroke
            , py::arg("")
            , py::return_value_policy::automatic_reference)
        .def("get_color", &SkPaint::getColor
            , py::return_value_policy::automatic_reference)
        .def("get_color4f", &SkPaint::getColor4f
            , py::return_value_policy::automatic_reference)
        .def("set_color", py::overload_cast<unsigned int>(&SkPaint::setColor)
            , py::arg("color")
            , py::return_value_policy::automatic_reference)
        .def("set_color", py::overload_cast<const SkRGBA4f<kUnpremul_SkAlphaType> &, SkColorSpace *>(&SkPaint::setColor)
            , py::arg("color")
            , py::arg("color_space") = nullptr
            , py::return_value_policy::automatic_reference)
        .def("set_color4f", &SkPaint::setColor4f
            , py::arg("color")
            , py::arg("color_space") = nullptr
            , py::return_value_policy::automatic_reference)
        .def("get_alphaf", &SkPaint::getAlphaf
            , py::return_value_policy::automatic_reference)
        .def("get_alpha", &SkPaint::getAlpha
            , py::return_value_policy::automatic_reference)
        .def("set_alphaf", &SkPaint::setAlphaf
            , py::arg("a")
            , py::return_value_policy::automatic_reference)
        .def("set_alpha", &SkPaint::setAlpha
            , py::arg("a")
            , py::return_value_policy::automatic_reference)
        .def("set_argb", &SkPaint::setARGB
            , py::arg("a")
            , py::arg("r")
            , py::arg("g")
            , py::arg("b")
            , py::return_value_policy::automatic_reference)
        .def("get_stroke_width", &SkPaint::getStrokeWidth
            , py::return_value_policy::automatic_reference)
        .def("set_stroke_width", &SkPaint::setStrokeWidth
            , py::arg("width")
            , py::return_value_policy::automatic_reference)
        .def("get_stroke_miter", &SkPaint::getStrokeMiter
            , py::return_value_policy::automatic_reference)
        .def("set_stroke_miter", &SkPaint::setStrokeMiter
            , py::arg("miter_limit")
            , py::return_value_policy::automatic_reference)
        ;

        py::enum_<SkPaint::Cap>(Paint, "Cap", py::arithmetic())
            .value("K_BUTT_CAP", SkPaint::Cap::kButt_Cap)
            .value("K_ROUND_CAP", SkPaint::Cap::kRound_Cap)
            .value("K_SQUARE_CAP", SkPaint::Cap::kSquare_Cap)
            .value("K_LAST_CAP", SkPaint::Cap::kLast_Cap)
            .value("K_DEFAULT_CAP", SkPaint::Cap::kDefault_Cap)
            .export_values()
        ;
        py::enum_<SkPaint::Join>(Paint, "Join", py::arithmetic())
            .value("K_MITER_JOIN", SkPaint::Join::kMiter_Join)
            .value("K_ROUND_JOIN", SkPaint::Join::kRound_Join)
            .value("K_BEVEL_JOIN", SkPaint::Join::kBevel_Join)
            .value("K_LAST_JOIN", SkPaint::Join::kLast_Join)
            .value("K_DEFAULT_JOIN", SkPaint::Join::kDefault_Join)
            .export_values()
        ;
        Paint
        .def("get_stroke_cap", &SkPaint::getStrokeCap
            , py::return_value_policy::automatic_reference)
        .def("set_stroke_cap", &SkPaint::setStrokeCap
            , py::arg("cap")
            , py::return_value_policy::automatic_reference)
        .def("get_stroke_join", &SkPaint::getStrokeJoin
            , py::return_value_policy::automatic_reference)
        .def("set_stroke_join", &SkPaint::setStrokeJoin
            , py::arg("join")
            , py::return_value_policy::automatic_reference)
        .def("get_shader", &SkPaint::getShader
            , py::return_value_policy::automatic_reference)
        .def("ref_shader", &SkPaint::refShader
            , py::return_value_policy::automatic_reference)
        .def("set_shader", &SkPaint::setShader
            , py::arg("shader")
            , py::return_value_policy::automatic_reference)
        .def("get_color_filter", &SkPaint::getColorFilter
            , py::return_value_policy::automatic_reference)
        .def("ref_color_filter", &SkPaint::refColorFilter
            , py::return_value_policy::automatic_reference)
        .def("set_color_filter", &SkPaint::setColorFilter
            , py::arg("color_filter")
            , py::return_value_policy::automatic_reference)
        .def("as_blend_mode", &SkPaint::asBlendMode
            , py::return_value_policy::automatic_reference)
        .def("get_blend_mode_or", &SkPaint::getBlendMode_or
            , py::arg("default_mode")
            , py::return_value_policy::automatic_reference)
        .def("is_src_over", &SkPaint::isSrcOver
            , py::return_value_policy::automatic_reference)
        .def("set_blend_mode", &SkPaint::setBlendMode
            , py::arg("mode")
            , py::return_value_policy::automatic_reference)
        .def("get_blender", &SkPaint::getBlender
            , py::return_value_policy::automatic_reference)
        .def("ref_blender", &SkPaint::refBlender
            , py::return_value_policy::automatic_reference)
        .def("set_blender", &SkPaint::setBlender
            , py::arg("blender")
            , py::return_value_policy::automatic_reference)
        .def("get_path_effect", &SkPaint::getPathEffect
            , py::return_value_policy::automatic_reference)
        .def("ref_path_effect", &SkPaint::refPathEffect
            , py::return_value_policy::automatic_reference)
        .def("set_path_effect", &SkPaint::setPathEffect
            , py::arg("path_effect")
            , py::return_value_policy::automatic_reference)
        .def("get_mask_filter", &SkPaint::getMaskFilter
            , py::return_value_policy::automatic_reference)
        .def("ref_mask_filter", &SkPaint::refMaskFilter
            , py::return_value_policy::automatic_reference)
        .def("set_mask_filter", &SkPaint::setMaskFilter
            , py::arg("mask_filter")
            , py::return_value_policy::automatic_reference)
        .def("get_image_filter", &SkPaint::getImageFilter
            , py::return_value_policy::automatic_reference)
        .def("ref_image_filter", &SkPaint::refImageFilter
            , py::return_value_policy::automatic_reference)
        .def("set_image_filter", &SkPaint::setImageFilter
            , py::arg("image_filter")
            , py::return_value_policy::automatic_reference)
        .def("nothing_to_draw", &SkPaint::nothingToDraw
            , py::return_value_policy::automatic_reference)
        .def("can_compute_fast_bounds", &SkPaint::canComputeFastBounds
            , py::return_value_policy::automatic_reference)
        .def("compute_fast_bounds", &SkPaint::computeFastBounds
            , py::arg("orig")
            , py::arg("storage")
            , py::return_value_policy::reference)
        .def("compute_fast_stroke_bounds", &SkPaint::computeFastStrokeBounds
            , py::arg("orig")
            , py::arg("storage")
            , py::return_value_policy::reference)
        .def("do_compute_fast_bounds", &SkPaint::doComputeFastBounds
            , py::arg("orig")
            , py::arg("storage")
            , py::arg("style")
            , py::return_value_policy::reference)
    ;


}