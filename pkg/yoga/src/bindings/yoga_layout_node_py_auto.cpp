#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/yoga/crunge-yoga.h>
#include <crunge/yoga/conversions.h>

#include "../LayoutNode.h"

namespace py = pybind11;

void init_yoga_layout_node_py_auto(py::module &_yoga, Registry &registry) {
    py::class_<Bounds> _Bounds(_yoga, "Bounds");
    registry.on(_yoga, "Bounds", _Bounds);
        _Bounds
        .def_readwrite("left", &Bounds::left)
        .def_readwrite("right", &Bounds::right)
        .def_readwrite("top", &Bounds::top)
        .def_readwrite("bottom", &Bounds::bottom)
        .def_readwrite("width", &Bounds::width)
        .def_readwrite("height", &Bounds::height)
    ;


    py::class_<Config> _Config(_yoga, "Config");
    registry.on(_yoga, "Config", _Config);
        _Config
        .def_static("create", &Config::create
            , py::return_value_policy::reference)
        .def_static("destroy", &Config::destroy
            , py::arg("config")
            )
        .def("set_experimental_feature_enabled", &Config::setExperimentalFeatureEnabled
            , py::arg("feature")
            , py::arg("enabled")
            )
        .def("set_point_scale_factor", &Config::setPointScaleFactor
            , py::arg("pixels_in_point")
            )
        .def("set_errata", &Config::setErrata
            , py::arg("errata")
            )
        .def("set_use_web_defaults", &Config::setUseWebDefaults
            , py::arg("use_web_defaults")
            )
        .def("is_experimental_feature_enabled", &Config::isExperimentalFeatureEnabled
            , py::arg("feature")
            )
        .def("get_errata", &Config::getErrata
            )
        .def("use_web_defaults", &Config::useWebDefaults
            )
    ;


    py::class_<Size> _Size(_yoga, "Size");
    registry.on(_yoga, "Size", _Size);
        _Size
        .def_readwrite("width", &Size::width)
        .def_readwrite("height", &Size::height)
        .def(py::init<>())
        .def(py::init<double, double>()
        , py::arg("width")
        , py::arg("height")
        )
    ;


    py::class_<LayoutNode> _LayoutNode(_yoga, "LayoutNode");
    registry.on(_yoga, "LayoutNode", _LayoutNode);
        _LayoutNode
        .def_static("create_default", &LayoutNode::createDefault
            , py::return_value_policy::reference)
        .def_static("create_with_config", &LayoutNode::createWithConfig
            , py::arg("config")
            , py::return_value_policy::reference)
        .def_static("destroy", &LayoutNode::destroy
            , py::arg("node")
            )
        .def("reset", &LayoutNode::reset
            )
        .def("copy_style", &LayoutNode::copyStyle
            , py::arg("other")
            )
        .def("set_position_type", &LayoutNode::setPositionType
            , py::arg("position_type")
            )
        .def("set_position", &LayoutNode::setPosition
            , py::arg("edge")
            , py::arg("position")
            )
        .def("set_position_percent", &LayoutNode::setPositionPercent
            , py::arg("edge")
            , py::arg("position")
            )
        .def("set_position_auto", &LayoutNode::setPositionAuto
            , py::arg("edge")
            )
        .def("set_align_content", &LayoutNode::setAlignContent
            , py::arg("align_content")
            )
        .def("set_align_items", &LayoutNode::setAlignItems
            , py::arg("align_items")
            )
        .def("set_align_self", &LayoutNode::setAlignSelf
            , py::arg("align_self")
            )
        .def("set_flex_direction", &LayoutNode::setFlexDirection
            , py::arg("flex_direction")
            )
        .def("set_flex_wrap", &LayoutNode::setFlexWrap
            , py::arg("flex_wrap")
            )
        .def("set_justify_content", &LayoutNode::setJustifyContent
            , py::arg("justify_content")
            )
        .def("set_direction", &LayoutNode::setDirection
            , py::arg("direction")
            )
        .def("set_margin", &LayoutNode::setMargin
            , py::arg("edge")
            , py::arg("margin")
            )
        .def("set_margin_percent", &LayoutNode::setMarginPercent
            , py::arg("edge")
            , py::arg("margin")
            )
        .def("set_margin_auto", &LayoutNode::setMarginAuto
            , py::arg("edge")
            )
        .def("set_overflow", &LayoutNode::setOverflow
            , py::arg("overflow")
            )
        .def("set_display", &LayoutNode::setDisplay
            , py::arg("display")
            )
        .def("set_flex", &LayoutNode::setFlex
            , py::arg("flex")
            )
        .def("set_flex_basis", &LayoutNode::setFlexBasis
            , py::arg("flex_basis")
            )
        .def("set_flex_basis_percent", &LayoutNode::setFlexBasisPercent
            , py::arg("flex_basis")
            )
        .def("set_flex_basis_auto", &LayoutNode::setFlexBasisAuto
            )
        .def("set_flex_basis_max_content", &LayoutNode::setFlexBasisMaxContent
            )
        .def("set_flex_basis_fit_content", &LayoutNode::setFlexBasisFitContent
            )
        .def("set_flex_basis_stretch", &LayoutNode::setFlexBasisStretch
            )
        .def("set_flex_grow", &LayoutNode::setFlexGrow
            , py::arg("flex_grow")
            )
        .def("set_flex_shrink", &LayoutNode::setFlexShrink
            , py::arg("flex_shrink")
            )
        .def("set_width", &LayoutNode::setWidth
            , py::arg("width")
            )
        .def("set_width_percent", &LayoutNode::setWidthPercent
            , py::arg("width")
            )
        .def("set_width_auto", &LayoutNode::setWidthAuto
            )
        .def("set_width_max_content", &LayoutNode::setWidthMaxContent
            )
        .def("set_width_fit_content", &LayoutNode::setWidthFitContent
            )
        .def("set_width_stretch", &LayoutNode::setWidthStretch
            )
        .def("set_height", &LayoutNode::setHeight
            , py::arg("height")
            )
        .def("set_height_percent", &LayoutNode::setHeightPercent
            , py::arg("height")
            )
        .def("set_height_auto", &LayoutNode::setHeightAuto
            )
        .def("set_height_max_content", &LayoutNode::setHeightMaxContent
            )
        .def("set_height_fit_content", &LayoutNode::setHeightFitContent
            )
        .def("set_height_stretch", &LayoutNode::setHeightStretch
            )
        .def("set_min_width", &LayoutNode::setMinWidth
            , py::arg("min_width")
            )
        .def("set_min_width_percent", &LayoutNode::setMinWidthPercent
            , py::arg("min_width")
            )
        .def("set_min_width_max_content", &LayoutNode::setMinWidthMaxContent
            )
        .def("set_min_width_fit_content", &LayoutNode::setMinWidthFitContent
            )
        .def("set_min_width_stretch", &LayoutNode::setMinWidthStretch
            )
        .def("set_min_height", &LayoutNode::setMinHeight
            , py::arg("min_height")
            )
        .def("set_min_height_percent", &LayoutNode::setMinHeightPercent
            , py::arg("min_height")
            )
        .def("set_min_height_max_content", &LayoutNode::setMinHeightMaxContent
            )
        .def("set_min_height_fit_content", &LayoutNode::setMinHeightFitContent
            )
        .def("set_min_height_stretch", &LayoutNode::setMinHeightStretch
            )
        .def("set_max_width", &LayoutNode::setMaxWidth
            , py::arg("max_width")
            )
        .def("set_max_width_percent", &LayoutNode::setMaxWidthPercent
            , py::arg("max_width")
            )
        .def("set_max_width_max_content", &LayoutNode::setMaxWidthMaxContent
            )
        .def("set_max_width_fit_content", &LayoutNode::setMaxWidthFitContent
            )
        .def("set_max_width_stretch", &LayoutNode::setMaxWidthStretch
            )
        .def("set_max_height", &LayoutNode::setMaxHeight
            , py::arg("max_height")
            )
        .def("set_max_height_percent", &LayoutNode::setMaxHeightPercent
            , py::arg("max_height")
            )
        .def("set_max_height_max_content", &LayoutNode::setMaxHeightMaxContent
            )
        .def("set_max_height_fit_content", &LayoutNode::setMaxHeightFitContent
            )
        .def("set_max_height_stretch", &LayoutNode::setMaxHeightStretch
            )
        .def("set_aspect_ratio", &LayoutNode::setAspectRatio
            , py::arg("aspect_ratio")
            )
        .def("set_border", &LayoutNode::setBorder
            , py::arg("edge")
            , py::arg("border")
            )
        .def("set_padding", &LayoutNode::setPadding
            , py::arg("edge")
            , py::arg("padding")
            )
        .def("set_padding_percent", &LayoutNode::setPaddingPercent
            , py::arg("edge")
            , py::arg("padding")
            )
        .def("set_gap", &LayoutNode::setGap
            , py::arg("gutter")
            , py::arg("gap_length")
            )
        .def("set_gap_percent", &LayoutNode::setGapPercent
            , py::arg("gutter")
            , py::arg("gap_length")
            )
        .def("set_box_sizing", &LayoutNode::setBoxSizing
            , py::arg("box_sizing")
            )
        .def("get_position_type", &LayoutNode::getPositionType
            )
        .def("get_position", &LayoutNode::getPosition
            , py::arg("edge")
            )
        .def("get_align_content", &LayoutNode::getAlignContent
            )
        .def("get_align_items", &LayoutNode::getAlignItems
            )
        .def("get_align_self", &LayoutNode::getAlignSelf
            )
        .def("get_flex_direction", &LayoutNode::getFlexDirection
            )
        .def("get_flex_wrap", &LayoutNode::getFlexWrap
            )
        .def("get_justify_content", &LayoutNode::getJustifyContent
            )
        .def("get_direction", &LayoutNode::getDirection
            )
        .def("get_margin", &LayoutNode::getMargin
            , py::arg("edge")
            )
        .def("get_overflow", &LayoutNode::getOverflow
            )
        .def("get_display", &LayoutNode::getDisplay
            )
        .def("get_flex_basis", &LayoutNode::getFlexBasis
            )
        .def("get_flex_grow", &LayoutNode::getFlexGrow
            )
        .def("get_flex_shrink", &LayoutNode::getFlexShrink
            )
        .def("get_width", &LayoutNode::getWidth
            )
        .def("get_height", &LayoutNode::getHeight
            )
        .def("get_min_width", &LayoutNode::getMinWidth
            )
        .def("get_min_height", &LayoutNode::getMinHeight
            )
        .def("get_max_width", &LayoutNode::getMaxWidth
            )
        .def("get_max_height", &LayoutNode::getMaxHeight
            )
        .def("get_aspect_ratio", &LayoutNode::getAspectRatio
            )
        .def("get_border", &LayoutNode::getBorder
            , py::arg("edge")
            )
        .def("get_padding", &LayoutNode::getPadding
            , py::arg("edge")
            )
        .def("get_gap", &LayoutNode::getGap
            , py::arg("gutter")
            )
        .def("get_box_sizing", &LayoutNode::getBoxSizing
            )
        .def("insert_child", &LayoutNode::insertChild
            , py::arg("child")
            , py::arg("index")
            )
        .def("add_child", &LayoutNode::addChild
            , py::arg("child")
            )
        .def("remove_child", &LayoutNode::removeChild
            , py::arg("child")
            )
        .def("get_child_count", &LayoutNode::getChildCount
            )
        .def("get_parent", &LayoutNode::getParent
            , py::return_value_policy::reference)
        .def("get_child", &LayoutNode::getChild
            , py::arg("index")
            , py::return_value_policy::reference)
        .def("set_measure_func", &LayoutNode::setMeasureFunc
            , py::arg("measure_func")
            )
        .def("unset_measure_func", &LayoutNode::unsetMeasureFunc
            )
        .def("call_measure_func", &LayoutNode::callMeasureFunc
            , py::arg("width")
            , py::arg("width_mode")
            , py::arg("height")
            , py::arg("height_mode")
            )
        .def("set_dirtied_func", &LayoutNode::setDirtiedFunc
            , py::arg("dirtied_func")
            )
        .def("unset_dirtied_func", &LayoutNode::unsetDirtiedFunc
            )
        .def("call_dirtied_func", &LayoutNode::callDirtiedFunc
            )
        .def("mark_dirty", &LayoutNode::markDirty
            )
        .def("is_dirty", &LayoutNode::isDirty
            )
        .def("mark_layout_seen", &LayoutNode::markLayoutSeen
            )
        .def("has_new_layout", &LayoutNode::hasNewLayout
            )
        .def("calculate_bounds", &LayoutNode::calculateBounds
            , py::arg("width")
            , py::arg("height")
            , py::arg("direction")
            )
        .def("get_computed_left", &LayoutNode::getComputedLeft
            )
        .def("get_computed_right", &LayoutNode::getComputedRight
            )
        .def("get_computed_top", &LayoutNode::getComputedTop
            )
        .def("get_computed_bottom", &LayoutNode::getComputedBottom
            )
        .def("get_computed_width", &LayoutNode::getComputedWidth
            )
        .def("get_computed_height", &LayoutNode::getComputedHeight
            )
        .def("get_computed_bounds", &LayoutNode::getComputedBounds
            )
        .def("get_computed_margin", &LayoutNode::getComputedMargin
            , py::arg("edge")
            )
        .def("get_computed_border", &LayoutNode::getComputedBorder
            , py::arg("edge")
            )
        .def("get_computed_padding", &LayoutNode::getComputedPadding
            , py::arg("edge")
            )
        .def("set_is_reference_baseline", &LayoutNode::setIsReferenceBaseline
            , py::arg("is_reference_baseline")
            )
        .def("is_reference_baseline", &LayoutNode::isReferenceBaseline
            )
        .def_readwrite("children", &LayoutNode::py_children)
        .def("set_always_forms_containing_block", &LayoutNode::setAlwaysFormsContainingBlock
            , py::arg("always_form_containing_block")
            )
    ;


}