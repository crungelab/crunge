#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/yoga/crunge-yoga.h>
#include <crunge/yoga/conversions.h>

#include <yoga/node/Node.h>

namespace py = pybind11;

void init_yoga_node_py_auto(py::module &_yoga, Registry &registry) {
    py::class_<facebook::yoga::LayoutResults> LayoutResults(_yoga, "LayoutResults");
    registry.on(_yoga, "LayoutResults", LayoutResults);
        LayoutResults
        .def_readwrite("computed_flex_basis_generation", &facebook::yoga::LayoutResults::computedFlexBasisGeneration)
        .def_readwrite("computed_flex_basis", &facebook::yoga::LayoutResults::computedFlexBasis)
        .def_readwrite("generation_count", &facebook::yoga::LayoutResults::generationCount)
        .def_readwrite("config_version", &facebook::yoga::LayoutResults::configVersion)
        .def_readwrite("last_owner_direction", &facebook::yoga::LayoutResults::lastOwnerDirection)
        .def_readwrite("next_cached_measurements_index", &facebook::yoga::LayoutResults::nextCachedMeasurementsIndex)
        .def_readwrite("cached_measurements", &facebook::yoga::LayoutResults::cachedMeasurements)
        .def_readwrite("cached_layout", &facebook::yoga::LayoutResults::cachedLayout)
        .def("direction", &facebook::yoga::LayoutResults::direction
            , py::return_value_policy::automatic_reference)
        .def("set_direction", &facebook::yoga::LayoutResults::setDirection
            , py::arg("direction")
            , py::return_value_policy::automatic_reference)
        .def("had_overflow", &facebook::yoga::LayoutResults::hadOverflow
            , py::return_value_policy::automatic_reference)
        .def("set_had_overflow", &facebook::yoga::LayoutResults::setHadOverflow
            , py::arg("had_overflow")
            , py::return_value_policy::automatic_reference)
        .def("dimension", &facebook::yoga::LayoutResults::dimension
            , py::arg("axis")
            , py::return_value_policy::automatic_reference)
        .def("set_dimension", &facebook::yoga::LayoutResults::setDimension
            , py::arg("axis")
            , py::arg("dimension")
            , py::return_value_policy::automatic_reference)
        .def("measured_dimension", &facebook::yoga::LayoutResults::measuredDimension
            , py::arg("axis")
            , py::return_value_policy::automatic_reference)
        .def("raw_dimension", &facebook::yoga::LayoutResults::rawDimension
            , py::arg("axis")
            , py::return_value_policy::automatic_reference)
        .def("set_measured_dimension", &facebook::yoga::LayoutResults::setMeasuredDimension
            , py::arg("axis")
            , py::arg("dimension")
            , py::return_value_policy::automatic_reference)
        .def("set_raw_dimension", &facebook::yoga::LayoutResults::setRawDimension
            , py::arg("axis")
            , py::arg("dimension")
            , py::return_value_policy::automatic_reference)
        .def("position", &facebook::yoga::LayoutResults::position
            , py::arg("physical_edge")
            , py::return_value_policy::automatic_reference)
        .def("set_position", &facebook::yoga::LayoutResults::setPosition
            , py::arg("physical_edge")
            , py::arg("dimension")
            , py::return_value_policy::automatic_reference)
        .def("margin", &facebook::yoga::LayoutResults::margin
            , py::arg("physical_edge")
            , py::return_value_policy::automatic_reference)
        .def("set_margin", &facebook::yoga::LayoutResults::setMargin
            , py::arg("physical_edge")
            , py::arg("dimension")
            , py::return_value_policy::automatic_reference)
        .def("border", &facebook::yoga::LayoutResults::border
            , py::arg("physical_edge")
            , py::return_value_policy::automatic_reference)
        .def("set_border", &facebook::yoga::LayoutResults::setBorder
            , py::arg("physical_edge")
            , py::arg("dimension")
            , py::return_value_policy::automatic_reference)
        .def("padding", &facebook::yoga::LayoutResults::padding
            , py::arg("physical_edge")
            , py::return_value_policy::automatic_reference)
        .def("set_padding", &facebook::yoga::LayoutResults::setPadding
            , py::arg("physical_edge")
            , py::arg("dimension")
            , py::return_value_policy::automatic_reference)
    ;


    py::class_<YGNode> YGNode(_yoga, "YGNode");
    registry.on(_yoga, "YGNode", YGNode);
    py::class_<facebook::yoga::Node> Node(_yoga, "Node");
    registry.on(_yoga, "Node", Node);
        Node
        .def(py::init<>())
        .def(py::init<const facebook::yoga::Config *>()
        , py::arg("config")
        )
        .def(py::init<const facebook::yoga::Node &>()
        , py::arg("node")
        )
        .def("get_context", &facebook::yoga::Node::getContext
            , py::return_value_policy::automatic_reference)
        .def("always_forms_containing_block", &facebook::yoga::Node::alwaysFormsContainingBlock
            , py::return_value_policy::automatic_reference)
        .def("get_has_new_layout", &facebook::yoga::Node::getHasNewLayout
            , py::return_value_policy::automatic_reference)
        .def("get_node_type", &facebook::yoga::Node::getNodeType
            , py::return_value_policy::automatic_reference)
        .def("has_measure_func", &facebook::yoga::Node::hasMeasureFunc
            , py::return_value_policy::automatic_reference)
        .def("measure", &facebook::yoga::Node::measure
            , py::arg("available_width")
            , py::arg("width_mode")
            , py::arg("available_height")
            , py::arg("height_mode")
            , py::return_value_policy::automatic_reference)
        .def("has_baseline_func", &facebook::yoga::Node::hasBaselineFunc
            , py::return_value_policy::automatic_reference)
        .def("baseline", &facebook::yoga::Node::baseline
            , py::arg("width")
            , py::arg("height")
            , py::return_value_policy::automatic_reference)
        .def("dimension_with_margin", &facebook::yoga::Node::dimensionWithMargin
            , py::arg("axis")
            , py::arg("width_size")
            , py::return_value_policy::automatic_reference)
        .def("is_layout_dimension_defined", &facebook::yoga::Node::isLayoutDimensionDefined
            , py::arg("axis")
            , py::return_value_policy::automatic_reference)
        .def("has_errata", &facebook::yoga::Node::hasErrata
            , py::arg("errata")
            , py::return_value_policy::automatic_reference)
        .def("get_layout", py::overload_cast<>(&facebook::yoga::Node::getLayout)
            , py::return_value_policy::reference)
        .def("get_layout", py::overload_cast<>(&facebook::yoga::Node::getLayout, py::const_)
            , py::return_value_policy::reference)
        .def("get_line_index", &facebook::yoga::Node::getLineIndex
            , py::return_value_policy::automatic_reference)
        .def("is_reference_baseline", &facebook::yoga::Node::isReferenceBaseline
            , py::return_value_policy::automatic_reference)
        .def("get_owner", &facebook::yoga::Node::getOwner
            , py::return_value_policy::automatic_reference)
        .def("get_children", &facebook::yoga::Node::getChildren
            , py::return_value_policy::reference)
        .def("get_child", &facebook::yoga::Node::getChild
            , py::arg("index")
            , py::return_value_policy::automatic_reference)
        .def("get_child_count", &facebook::yoga::Node::getChildCount
            , py::return_value_policy::automatic_reference)
        .def("get_layout_children", &facebook::yoga::Node::getLayoutChildren
            , py::return_value_policy::automatic_reference)
        .def("get_layout_child_count", &facebook::yoga::Node::getLayoutChildCount
            , py::return_value_policy::automatic_reference)
        .def("get_config", &facebook::yoga::Node::getConfig
            , py::return_value_policy::automatic_reference)
        .def("is_dirty", &facebook::yoga::Node::isDirty
            , py::return_value_policy::automatic_reference)
        .def("get_processed_dimension", &facebook::yoga::Node::getProcessedDimension
            , py::arg("dimension")
            , py::return_value_policy::automatic_reference)
        .def("get_resolved_dimension", &facebook::yoga::Node::getResolvedDimension
            , py::arg("direction")
            , py::arg("dimension")
            , py::arg("reference_length")
            , py::arg("owner_width")
            , py::return_value_policy::automatic_reference)
        .def("set_context", &facebook::yoga::Node::setContext
            , py::arg("context")
            , py::return_value_policy::automatic_reference)
        .def("set_always_forms_containing_block", &facebook::yoga::Node::setAlwaysFormsContainingBlock
            , py::arg("always_forms_containing_block")
            , py::return_value_policy::automatic_reference)
        .def("set_has_new_layout", &facebook::yoga::Node::setHasNewLayout
            , py::arg("has_new_layout")
            , py::return_value_policy::automatic_reference)
        .def("set_node_type", &facebook::yoga::Node::setNodeType
            , py::arg("node_type")
            , py::return_value_policy::automatic_reference)
        .def("set_measure_func", &facebook::yoga::Node::setMeasureFunc
            , py::arg("measure_func")
            , py::return_value_policy::automatic_reference)
        .def("set_baseline_func", &facebook::yoga::Node::setBaselineFunc
            , py::arg("base_line_func")
            , py::return_value_policy::automatic_reference)
        .def("set_dirtied_func", &facebook::yoga::Node::setDirtiedFunc
            , py::arg("dirtied_func")
            , py::return_value_policy::automatic_reference)
        .def("set_style", &facebook::yoga::Node::setStyle
            , py::arg("style")
            , py::return_value_policy::automatic_reference)
        .def("set_layout", &facebook::yoga::Node::setLayout
            , py::arg("layout")
            , py::return_value_policy::automatic_reference)
        .def("set_line_index", &facebook::yoga::Node::setLineIndex
            , py::arg("line_index")
            , py::return_value_policy::automatic_reference)
        .def("set_is_reference_baseline", &facebook::yoga::Node::setIsReferenceBaseline
            , py::arg("is_reference_baseline")
            , py::return_value_policy::automatic_reference)
        .def("set_owner", &facebook::yoga::Node::setOwner
            , py::arg("owner")
            , py::return_value_policy::automatic_reference)
        .def("set_children", &facebook::yoga::Node::setChildren
            , py::arg("children")
            , py::return_value_policy::automatic_reference)
        .def("set_config", &facebook::yoga::Node::setConfig
            , py::arg("config")
            , py::return_value_policy::automatic_reference)
        .def("set_dirty", &facebook::yoga::Node::setDirty
            , py::arg("is_dirty")
            , py::return_value_policy::automatic_reference)
        .def("set_layout_last_owner_direction", &facebook::yoga::Node::setLayoutLastOwnerDirection
            , py::arg("direction")
            , py::return_value_policy::automatic_reference)
        .def("set_layout_computed_flex_basis", &facebook::yoga::Node::setLayoutComputedFlexBasis
            , py::arg("computed_flex_basis")
            , py::return_value_policy::automatic_reference)
        .def("set_layout_computed_flex_basis_generation", &facebook::yoga::Node::setLayoutComputedFlexBasisGeneration
            , py::arg("computed_flex_basis_generation")
            , py::return_value_policy::automatic_reference)
        .def("set_layout_measured_dimension", &facebook::yoga::Node::setLayoutMeasuredDimension
            , py::arg("measured_dimension")
            , py::arg("dimension")
            , py::return_value_policy::automatic_reference)
        .def("set_layout_had_overflow", &facebook::yoga::Node::setLayoutHadOverflow
            , py::arg("had_overflow")
            , py::return_value_policy::automatic_reference)
        .def("set_layout_dimension", &facebook::yoga::Node::setLayoutDimension
            , py::arg("length_value")
            , py::arg("dimension")
            , py::return_value_policy::automatic_reference)
        .def("set_layout_direction", &facebook::yoga::Node::setLayoutDirection
            , py::arg("direction")
            , py::return_value_policy::automatic_reference)
        .def("set_layout_margin", &facebook::yoga::Node::setLayoutMargin
            , py::arg("margin")
            , py::arg("edge")
            , py::return_value_policy::automatic_reference)
        .def("set_layout_border", &facebook::yoga::Node::setLayoutBorder
            , py::arg("border")
            , py::arg("edge")
            , py::return_value_policy::automatic_reference)
        .def("set_layout_padding", &facebook::yoga::Node::setLayoutPadding
            , py::arg("padding")
            , py::arg("edge")
            , py::return_value_policy::automatic_reference)
        .def("set_layout_position", &facebook::yoga::Node::setLayoutPosition
            , py::arg("position")
            , py::arg("edge")
            , py::return_value_policy::automatic_reference)
        .def("set_position", &facebook::yoga::Node::setPosition
            , py::arg("direction")
            , py::arg("owner_width")
            , py::arg("owner_height")
            , py::return_value_policy::automatic_reference)
        .def("process_flex_basis", &facebook::yoga::Node::processFlexBasis
            , py::return_value_policy::automatic_reference)
        .def("resolve_flex_basis", &facebook::yoga::Node::resolveFlexBasis
            , py::arg("direction")
            , py::arg("flex_direction")
            , py::arg("reference_length")
            , py::arg("owner_width")
            , py::return_value_policy::automatic_reference)
        .def("process_dimensions", &facebook::yoga::Node::processDimensions
            , py::return_value_policy::automatic_reference)
        .def("resolve_direction", &facebook::yoga::Node::resolveDirection
            , py::arg("owner_direction")
            , py::return_value_policy::automatic_reference)
        .def("clear_children", &facebook::yoga::Node::clearChildren
            , py::return_value_policy::automatic_reference)
        .def("replace_child", py::overload_cast<facebook::yoga::Node *, facebook::yoga::Node *>(&facebook::yoga::Node::replaceChild)
            , py::arg("old_child")
            , py::arg("new_child")
            , py::return_value_policy::automatic_reference)
        .def("replace_child", py::overload_cast<facebook::yoga::Node *, unsigned long>(&facebook::yoga::Node::replaceChild)
            , py::arg("child")
            , py::arg("index")
            , py::return_value_policy::automatic_reference)
        .def("insert_child", &facebook::yoga::Node::insertChild
            , py::arg("child")
            , py::arg("index")
            , py::return_value_policy::automatic_reference)
        .def("remove_child", py::overload_cast<facebook::yoga::Node *>(&facebook::yoga::Node::removeChild)
            , py::arg("child")
            , py::return_value_policy::automatic_reference)
        .def("remove_child", py::overload_cast<unsigned long>(&facebook::yoga::Node::removeChild)
            , py::arg("index")
            , py::return_value_policy::automatic_reference)
        .def("clone_children_if_needed", &facebook::yoga::Node::cloneChildrenIfNeeded
            , py::return_value_policy::automatic_reference)
        .def("mark_dirty_and_propagate", &facebook::yoga::Node::markDirtyAndPropagate
            , py::return_value_policy::automatic_reference)
        .def("resolve_flex_grow", &facebook::yoga::Node::resolveFlexGrow
            , py::return_value_policy::automatic_reference)
        .def("resolve_flex_shrink", &facebook::yoga::Node::resolveFlexShrink
            , py::return_value_policy::automatic_reference)
        .def("is_node_flexible", &facebook::yoga::Node::isNodeFlexible
            , py::return_value_policy::automatic_reference)
        .def("reset", &facebook::yoga::Node::reset
            , py::return_value_policy::automatic_reference)
    ;


}