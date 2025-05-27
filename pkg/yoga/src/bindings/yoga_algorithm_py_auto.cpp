#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/yoga/crunge-yoga.h>
#include <crunge/yoga/conversions.h>

#include <yoga/algorithm/CalculateLayout.h>

namespace py = pybind11;

void init_yoga_algorithm_py_auto(py::module &_yoga, Registry &registry) {
    _yoga
    .def("calculate_layout", &facebook::yoga::calculateLayout
        , py::arg("node")
        , py::arg("owner_width")
        , py::arg("owner_height")
        , py::arg("owner_direction")
        , py::return_value_policy::automatic_reference)
    .def("calculate_layout_internal", [](facebook::yoga::Node * node, float availableWidth, float availableHeight, facebook::yoga::Direction ownerDirection, facebook::yoga::SizingMode widthSizingMode, facebook::yoga::SizingMode heightSizingMode, float ownerWidth, float ownerHeight, bool performLayout, facebook::yoga::LayoutPassReason reason, facebook::yoga::LayoutData & layoutMarkerData, unsigned int depth, unsigned int generationCount)
        {
            auto ret = facebook::yoga::calculateLayoutInternal(node, availableWidth, availableHeight, ownerDirection, widthSizingMode, heightSizingMode, ownerWidth, ownerHeight, performLayout, reason, layoutMarkerData, depth, generationCount);
            return std::make_tuple(ret, layoutMarkerData);
        }
        , py::arg("node")
        , py::arg("available_width")
        , py::arg("available_height")
        , py::arg("owner_direction")
        , py::arg("width_sizing_mode")
        , py::arg("height_sizing_mode")
        , py::arg("owner_width")
        , py::arg("owner_height")
        , py::arg("perform_layout")
        , py::arg("reason")
        , py::arg("layout_marker_data")
        , py::arg("depth")
        , py::arg("generation_count")
        , py::return_value_policy::automatic_reference)
    ;


}