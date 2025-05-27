#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/yoga/crunge-yoga.h>
#include <crunge/yoga/conversions.h>

#include <yoga/enums/Align.h>
#include <yoga/enums/BoxSizing.h>
#include <yoga/enums/Dimension.h>
#include <yoga/enums/Direction.h>
#include <yoga/enums/Display.h>
#include <yoga/enums/Edge.h>
#include <yoga/enums/FlexDirection.h>
#include <yoga/enums/Gutter.h>
#include <yoga/enums/Justify.h>
#include <yoga/enums/Overflow.h>
#include <yoga/enums/PhysicalEdge.h>
#include <yoga/enums/PositionType.h>
#include <yoga/enums/Unit.h>
#include <yoga/enums/Wrap.h>

namespace py = pybind11;

void init_yoga_enums_py_auto(py::module &_yoga, Registry &registry) {
    py::enum_<facebook::yoga::Align>(_yoga, "Align", py::arithmetic())
        .value("AUTO", facebook::yoga::Align::Auto)
        .value("FLEX_START", facebook::yoga::Align::FlexStart)
        .value("CENTER", facebook::yoga::Align::Center)
        .value("FLEX_END", facebook::yoga::Align::FlexEnd)
        .value("STRETCH", facebook::yoga::Align::Stretch)
        .value("BASELINE", facebook::yoga::Align::Baseline)
        .value("SPACE_BETWEEN", facebook::yoga::Align::SpaceBetween)
        .value("SPACE_AROUND", facebook::yoga::Align::SpaceAround)
        .value("SPACE_EVENLY", facebook::yoga::Align::SpaceEvenly)
        .export_values()
    ;

    py::enum_<facebook::yoga::BoxSizing>(_yoga, "BoxSizing", py::arithmetic())
        .value("BORDER_BOX", facebook::yoga::BoxSizing::BorderBox)
        .value("CONTENT_BOX", facebook::yoga::BoxSizing::ContentBox)
        .export_values()
    ;

    py::enum_<facebook::yoga::Dimension>(_yoga, "Dimension", py::arithmetic())
        .value("WIDTH", facebook::yoga::Dimension::Width)
        .value("HEIGHT", facebook::yoga::Dimension::Height)
        .export_values()
    ;

    py::enum_<facebook::yoga::Direction>(_yoga, "Direction", py::arithmetic())
        .value("INHERIT", facebook::yoga::Direction::Inherit)
        .value("LTR", facebook::yoga::Direction::LTR)
        .value("RTL", facebook::yoga::Direction::RTL)
        .export_values()
    ;

    py::enum_<facebook::yoga::Display>(_yoga, "Display", py::arithmetic())
        .value("FLEX", facebook::yoga::Display::Flex)
        .value("NONE", facebook::yoga::Display::None)
        .value("CONTENTS", facebook::yoga::Display::Contents)
        .export_values()
    ;

    py::enum_<facebook::yoga::Edge>(_yoga, "Edge", py::arithmetic())
        .value("LEFT", facebook::yoga::Edge::Left)
        .value("TOP", facebook::yoga::Edge::Top)
        .value("RIGHT", facebook::yoga::Edge::Right)
        .value("BOTTOM", facebook::yoga::Edge::Bottom)
        .value("START", facebook::yoga::Edge::Start)
        .value("END", facebook::yoga::Edge::End)
        .value("HORIZONTAL", facebook::yoga::Edge::Horizontal)
        .value("VERTICAL", facebook::yoga::Edge::Vertical)
        .value("ALL", facebook::yoga::Edge::All)
        .export_values()
    ;

    py::enum_<facebook::yoga::FlexDirection>(_yoga, "FlexDirection", py::arithmetic())
        .value("COLUMN", facebook::yoga::FlexDirection::Column)
        .value("COLUMN_REVERSE", facebook::yoga::FlexDirection::ColumnReverse)
        .value("ROW", facebook::yoga::FlexDirection::Row)
        .value("ROW_REVERSE", facebook::yoga::FlexDirection::RowReverse)
        .export_values()
    ;

    py::enum_<facebook::yoga::Gutter>(_yoga, "Gutter", py::arithmetic())
        .value("COLUMN", facebook::yoga::Gutter::Column)
        .value("ROW", facebook::yoga::Gutter::Row)
        .value("ALL", facebook::yoga::Gutter::All)
        .export_values()
    ;

    py::enum_<facebook::yoga::Justify>(_yoga, "Justify", py::arithmetic())
        .value("FLEX_START", facebook::yoga::Justify::FlexStart)
        .value("CENTER", facebook::yoga::Justify::Center)
        .value("FLEX_END", facebook::yoga::Justify::FlexEnd)
        .value("SPACE_BETWEEN", facebook::yoga::Justify::SpaceBetween)
        .value("SPACE_AROUND", facebook::yoga::Justify::SpaceAround)
        .value("SPACE_EVENLY", facebook::yoga::Justify::SpaceEvenly)
        .export_values()
    ;

    py::enum_<facebook::yoga::Overflow>(_yoga, "Overflow", py::arithmetic())
        .value("VISIBLE", facebook::yoga::Overflow::Visible)
        .value("HIDDEN", facebook::yoga::Overflow::Hidden)
        .value("SCROLL", facebook::yoga::Overflow::Scroll)
        .export_values()
    ;

    py::enum_<facebook::yoga::PhysicalEdge>(_yoga, "PhysicalEdge", py::arithmetic())
        .value("LEFT", facebook::yoga::PhysicalEdge::Left)
        .value("TOP", facebook::yoga::PhysicalEdge::Top)
        .value("RIGHT", facebook::yoga::PhysicalEdge::Right)
        .value("BOTTOM", facebook::yoga::PhysicalEdge::Bottom)
        .export_values()
    ;

    py::enum_<facebook::yoga::PositionType>(_yoga, "PositionType", py::arithmetic())
        .value("STATIC", facebook::yoga::PositionType::Static)
        .value("RELATIVE", facebook::yoga::PositionType::Relative)
        .value("ABSOLUTE", facebook::yoga::PositionType::Absolute)
        .export_values()
    ;

    py::enum_<facebook::yoga::Unit>(_yoga, "Unit", py::arithmetic())
        .value("UNDEFINED", facebook::yoga::Unit::Undefined)
        .value("POINT", facebook::yoga::Unit::Point)
        .value("PERCENT", facebook::yoga::Unit::Percent)
        .value("AUTO", facebook::yoga::Unit::Auto)
        .value("MAX_CONTENT", facebook::yoga::Unit::MaxContent)
        .value("FIT_CONTENT", facebook::yoga::Unit::FitContent)
        .value("STRETCH", facebook::yoga::Unit::Stretch)
        .export_values()
    ;

    py::enum_<facebook::yoga::Wrap>(_yoga, "Wrap", py::arithmetic())
        .value("NO_WRAP", facebook::yoga::Wrap::NoWrap)
        .value("WRAP", facebook::yoga::Wrap::Wrap)
        .value("REVERSE", facebook::yoga::Wrap::WrapReverse)
        .export_values()
    ;

}