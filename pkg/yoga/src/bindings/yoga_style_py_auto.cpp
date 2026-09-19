#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/yoga/crunge-yoga.h>
#include <crunge/yoga/conversions.h>

#include <yoga/style/Style.h>

namespace py = pybind11;

void init_yoga_style_py_auto(py::module &_yoga, Registry &registry) {
    py::class_<facebook::yoga::StyleLength> _StyleLength(_yoga, "StyleLength");
    registry.on(_yoga, "StyleLength", _StyleLength);
        _StyleLength
        .def(py::init<>())
        .def_static("points", &facebook::yoga::StyleLength::points
            , py::arg("value")
            )
        .def_static("percent", &facebook::yoga::StyleLength::percent
            , py::arg("value")
            )
        .def_static("of_auto", &facebook::yoga::StyleLength::ofAuto
            )
        .def_static("undefined", &facebook::yoga::StyleLength::undefined
            )
        .def("is_auto", &facebook::yoga::StyleLength::isAuto
            )
        .def("is_undefined", &facebook::yoga::StyleLength::isUndefined
            )
        .def("is_points", &facebook::yoga::StyleLength::isPoints
            )
        .def("is_percent", &facebook::yoga::StyleLength::isPercent
            )
        .def("is_defined", &facebook::yoga::StyleLength::isDefined
            )
        .def("value", &facebook::yoga::StyleLength::value
            )
        .def("resolve", &facebook::yoga::StyleLength::resolve
            , py::arg("reference_length")
            )
        .def("inexact_equals", &facebook::yoga::StyleLength::inexactEquals
            , py::arg("other")
            )
    ;


    py::class_<facebook::yoga::StyleSizeLength> _StyleSizeLength(_yoga, "StyleSizeLength");
    registry.on(_yoga, "StyleSizeLength", _StyleSizeLength);
        _StyleSizeLength
        .def(py::init<>())
        .def_static("points", &facebook::yoga::StyleSizeLength::points
            , py::arg("value")
            )
        .def_static("percent", &facebook::yoga::StyleSizeLength::percent
            , py::arg("value")
            )
        .def_static("of_auto", &facebook::yoga::StyleSizeLength::ofAuto
            )
        .def_static("of_max_content", &facebook::yoga::StyleSizeLength::ofMaxContent
            )
        .def_static("of_fit_content", &facebook::yoga::StyleSizeLength::ofFitContent
            )
        .def_static("of_stretch", &facebook::yoga::StyleSizeLength::ofStretch
            )
        .def_static("undefined", &facebook::yoga::StyleSizeLength::undefined
            )
        .def("is_auto", &facebook::yoga::StyleSizeLength::isAuto
            )
        .def("is_max_content", &facebook::yoga::StyleSizeLength::isMaxContent
            )
        .def("is_fit_content", &facebook::yoga::StyleSizeLength::isFitContent
            )
        .def("is_stretch", &facebook::yoga::StyleSizeLength::isStretch
            )
        .def("is_undefined", &facebook::yoga::StyleSizeLength::isUndefined
            )
        .def("is_defined", &facebook::yoga::StyleSizeLength::isDefined
            )
        .def("is_points", &facebook::yoga::StyleSizeLength::isPoints
            )
        .def("is_percent", &facebook::yoga::StyleSizeLength::isPercent
            )
        .def("value", &facebook::yoga::StyleSizeLength::value
            )
        .def("resolve", &facebook::yoga::StyleSizeLength::resolve
            , py::arg("reference_length")
            )
        .def("inexact_equals", &facebook::yoga::StyleSizeLength::inexactEquals
            , py::arg("other")
            )
    ;


    py::class_<facebook::yoga::Style> _Style(_yoga, "Style");
    registry.on(_yoga, "Style", _Style);
        _Style
        .def("direction", &facebook::yoga::Style::direction
            )
        .def("set_direction", &facebook::yoga::Style::setDirection
            , py::arg("value")
            )
        .def("flex_direction", &facebook::yoga::Style::flexDirection
            )
        .def("set_flex_direction", &facebook::yoga::Style::setFlexDirection
            , py::arg("value")
            )
        .def("justify_content", &facebook::yoga::Style::justifyContent
            )
        .def("set_justify_content", &facebook::yoga::Style::setJustifyContent
            , py::arg("value")
            )
        .def("align_content", &facebook::yoga::Style::alignContent
            )
        .def("set_align_content", &facebook::yoga::Style::setAlignContent
            , py::arg("value")
            )
        .def("align_items", &facebook::yoga::Style::alignItems
            )
        .def("set_align_items", &facebook::yoga::Style::setAlignItems
            , py::arg("value")
            )
        .def("align_self", &facebook::yoga::Style::alignSelf
            )
        .def("set_align_self", &facebook::yoga::Style::setAlignSelf
            , py::arg("value")
            )
        .def("position_type", &facebook::yoga::Style::positionType
            )
        .def("set_position_type", &facebook::yoga::Style::setPositionType
            , py::arg("value")
            )
        .def("flex_wrap", &facebook::yoga::Style::flexWrap
            )
        .def("set_flex_wrap", &facebook::yoga::Style::setFlexWrap
            , py::arg("value")
            )
        .def("overflow", &facebook::yoga::Style::overflow
            )
        .def("set_overflow", &facebook::yoga::Style::setOverflow
            , py::arg("value")
            )
        .def("display", &facebook::yoga::Style::display
            )
        .def("set_display", &facebook::yoga::Style::setDisplay
            , py::arg("value")
            )
        .def("flex", &facebook::yoga::Style::flex
            )
        .def("set_flex", &facebook::yoga::Style::setFlex
            , py::arg("value")
            )
        .def("flex_grow", &facebook::yoga::Style::flexGrow
            )
        .def("set_flex_grow", &facebook::yoga::Style::setFlexGrow
            , py::arg("value")
            )
        .def("flex_shrink", &facebook::yoga::Style::flexShrink
            )
        .def("set_flex_shrink", &facebook::yoga::Style::setFlexShrink
            , py::arg("value")
            )
        .def("flex_basis", &facebook::yoga::Style::flexBasis
            )
        .def("set_flex_basis", &facebook::yoga::Style::setFlexBasis
            , py::arg("value")
            )
        .def("margin", &facebook::yoga::Style::margin
            , py::arg("edge")
            )
        .def("set_margin", &facebook::yoga::Style::setMargin
            , py::arg("edge")
            , py::arg("value")
            )
        .def("position", &facebook::yoga::Style::position
            , py::arg("edge")
            )
        .def("set_position", &facebook::yoga::Style::setPosition
            , py::arg("edge")
            , py::arg("value")
            )
        .def("padding", &facebook::yoga::Style::padding
            , py::arg("edge")
            )
        .def("set_padding", &facebook::yoga::Style::setPadding
            , py::arg("edge")
            , py::arg("value")
            )
        .def("border", &facebook::yoga::Style::border
            , py::arg("edge")
            )
        .def("set_border", &facebook::yoga::Style::setBorder
            , py::arg("edge")
            , py::arg("value")
            )
        .def("gap", &facebook::yoga::Style::gap
            , py::arg("gutter")
            )
        .def("set_gap", &facebook::yoga::Style::setGap
            , py::arg("gutter")
            , py::arg("value")
            )
        .def("dimension", &facebook::yoga::Style::dimension
            , py::arg("axis")
            )
        .def("set_dimension", &facebook::yoga::Style::setDimension
            , py::arg("axis")
            , py::arg("value")
            )
        .def("min_dimension", &facebook::yoga::Style::minDimension
            , py::arg("axis")
            )
        .def("set_min_dimension", &facebook::yoga::Style::setMinDimension
            , py::arg("axis")
            , py::arg("value")
            )
        .def("resolved_min_dimension", &facebook::yoga::Style::resolvedMinDimension
            , py::arg("direction")
            , py::arg("axis")
            , py::arg("reference_length")
            , py::arg("owner_width")
            )
        .def("max_dimension", &facebook::yoga::Style::maxDimension
            , py::arg("axis")
            )
        .def("set_max_dimension", &facebook::yoga::Style::setMaxDimension
            , py::arg("axis")
            , py::arg("value")
            )
        .def("resolved_max_dimension", &facebook::yoga::Style::resolvedMaxDimension
            , py::arg("direction")
            , py::arg("axis")
            , py::arg("reference_length")
            , py::arg("owner_width")
            )
        .def("aspect_ratio", &facebook::yoga::Style::aspectRatio
            )
        .def("set_aspect_ratio", &facebook::yoga::Style::setAspectRatio
            , py::arg("value")
            )
        .def("box_sizing", &facebook::yoga::Style::boxSizing
            )
        .def("set_box_sizing", &facebook::yoga::Style::setBoxSizing
            , py::arg("value")
            )
        .def("horizontal_insets_defined", &facebook::yoga::Style::horizontalInsetsDefined
            )
        .def("vertical_insets_defined", &facebook::yoga::Style::verticalInsetsDefined
            )
        .def("is_flex_start_position_defined", &facebook::yoga::Style::isFlexStartPositionDefined
            , py::arg("axis")
            , py::arg("direction")
            )
        .def("is_flex_start_position_auto", &facebook::yoga::Style::isFlexStartPositionAuto
            , py::arg("axis")
            , py::arg("direction")
            )
        .def("is_inline_start_position_defined", &facebook::yoga::Style::isInlineStartPositionDefined
            , py::arg("axis")
            , py::arg("direction")
            )
        .def("is_inline_start_position_auto", &facebook::yoga::Style::isInlineStartPositionAuto
            , py::arg("axis")
            , py::arg("direction")
            )
        .def("is_flex_end_position_defined", &facebook::yoga::Style::isFlexEndPositionDefined
            , py::arg("axis")
            , py::arg("direction")
            )
        .def("is_flex_end_position_auto", &facebook::yoga::Style::isFlexEndPositionAuto
            , py::arg("axis")
            , py::arg("direction")
            )
        .def("is_inline_end_position_defined", &facebook::yoga::Style::isInlineEndPositionDefined
            , py::arg("axis")
            , py::arg("direction")
            )
        .def("is_inline_end_position_auto", &facebook::yoga::Style::isInlineEndPositionAuto
            , py::arg("axis")
            , py::arg("direction")
            )
        .def("compute_flex_start_position", &facebook::yoga::Style::computeFlexStartPosition
            , py::arg("axis")
            , py::arg("direction")
            , py::arg("axis_size")
            )
        .def("compute_inline_start_position", &facebook::yoga::Style::computeInlineStartPosition
            , py::arg("axis")
            , py::arg("direction")
            , py::arg("axis_size")
            )
        .def("compute_flex_end_position", &facebook::yoga::Style::computeFlexEndPosition
            , py::arg("axis")
            , py::arg("direction")
            , py::arg("axis_size")
            )
        .def("compute_inline_end_position", &facebook::yoga::Style::computeInlineEndPosition
            , py::arg("axis")
            , py::arg("direction")
            , py::arg("axis_size")
            )
        .def("compute_flex_start_margin", &facebook::yoga::Style::computeFlexStartMargin
            , py::arg("axis")
            , py::arg("direction")
            , py::arg("width_size")
            )
        .def("compute_inline_start_margin", &facebook::yoga::Style::computeInlineStartMargin
            , py::arg("axis")
            , py::arg("direction")
            , py::arg("width_size")
            )
        .def("compute_flex_end_margin", &facebook::yoga::Style::computeFlexEndMargin
            , py::arg("axis")
            , py::arg("direction")
            , py::arg("width_size")
            )
        .def("compute_inline_end_margin", &facebook::yoga::Style::computeInlineEndMargin
            , py::arg("axis")
            , py::arg("direction")
            , py::arg("width_size")
            )
        .def("compute_flex_start_border", &facebook::yoga::Style::computeFlexStartBorder
            , py::arg("axis")
            , py::arg("direction")
            )
        .def("compute_inline_start_border", &facebook::yoga::Style::computeInlineStartBorder
            , py::arg("axis")
            , py::arg("direction")
            )
        .def("compute_flex_end_border", &facebook::yoga::Style::computeFlexEndBorder
            , py::arg("axis")
            , py::arg("direction")
            )
        .def("compute_inline_end_border", &facebook::yoga::Style::computeInlineEndBorder
            , py::arg("axis")
            , py::arg("direction")
            )
        .def("compute_flex_start_padding", &facebook::yoga::Style::computeFlexStartPadding
            , py::arg("axis")
            , py::arg("direction")
            , py::arg("width_size")
            )
        .def("compute_inline_start_padding", &facebook::yoga::Style::computeInlineStartPadding
            , py::arg("axis")
            , py::arg("direction")
            , py::arg("width_size")
            )
        .def("compute_flex_end_padding", &facebook::yoga::Style::computeFlexEndPadding
            , py::arg("axis")
            , py::arg("direction")
            , py::arg("width_size")
            )
        .def("compute_inline_end_padding", &facebook::yoga::Style::computeInlineEndPadding
            , py::arg("axis")
            , py::arg("direction")
            , py::arg("width_size")
            )
        .def("compute_inline_start_padding_and_border", &facebook::yoga::Style::computeInlineStartPaddingAndBorder
            , py::arg("axis")
            , py::arg("direction")
            , py::arg("width_size")
            )
        .def("compute_flex_start_padding_and_border", &facebook::yoga::Style::computeFlexStartPaddingAndBorder
            , py::arg("axis")
            , py::arg("direction")
            , py::arg("width_size")
            )
        .def("compute_inline_end_padding_and_border", &facebook::yoga::Style::computeInlineEndPaddingAndBorder
            , py::arg("axis")
            , py::arg("direction")
            , py::arg("width_size")
            )
        .def("compute_flex_end_padding_and_border", &facebook::yoga::Style::computeFlexEndPaddingAndBorder
            , py::arg("axis")
            , py::arg("direction")
            , py::arg("width_size")
            )
        .def("compute_padding_and_border_for_dimension", &facebook::yoga::Style::computePaddingAndBorderForDimension
            , py::arg("direction")
            , py::arg("dimension")
            , py::arg("width_size")
            )
        .def("compute_border_for_axis", &facebook::yoga::Style::computeBorderForAxis
            , py::arg("axis")
            )
        .def("compute_margin_for_axis", &facebook::yoga::Style::computeMarginForAxis
            , py::arg("axis")
            , py::arg("width_size")
            )
        .def("compute_gap_for_axis", &facebook::yoga::Style::computeGapForAxis
            , py::arg("axis")
            , py::arg("owner_size")
            )
        .def("flex_start_margin_is_auto", &facebook::yoga::Style::flexStartMarginIsAuto
            , py::arg("axis")
            , py::arg("direction")
            )
        .def("flex_end_margin_is_auto", &facebook::yoga::Style::flexEndMarginIsAuto
            , py::arg("axis")
            , py::arg("direction")
            )
        .def(py::init<>())
    ;


}