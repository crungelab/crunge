#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

#include <nanort.h>
#include <iostream>

#include <cxbind/cxbind.h>
#include <crunge/nanort/conversions.h>

namespace py = pybind11;

using namespace nanort;

void init_generated(py::module &_nanort, Registry &registry) {
    py::enum_<nanort::RayType>(_nanort, "RayType", py::arithmetic())
        .value("RAY_TYPE_NONE", nanort::RayType::RAY_TYPE_NONE)
        .value("RAY_TYPE_PRIMARY", nanort::RayType::RAY_TYPE_PRIMARY)
        .value("RAY_TYPE_SECONDARY", nanort::RayType::RAY_TYPE_SECONDARY)
        .value("RAY_TYPE_DIFFUSE", nanort::RayType::RAY_TYPE_DIFFUSE)
        .value("RAY_TYPE_REFLECTION", nanort::RayType::RAY_TYPE_REFLECTION)
        .value("RAY_TYPE_REFRACTION", nanort::RayType::RAY_TYPE_REFRACTION)
        .export_values()
    ;

    py::class_<nanort::Ray<float>> Ray_float(_nanort, "Ray_float");
    registry.on(_nanort, "Ray_float", Ray_float);
    Ray_float
        .def(py::init<>())
        .def_readonly("org", &nanort::Ray<float>::org)
        .def_readonly("dir", &nanort::Ray<float>::dir)
        .def_readwrite("min_t", &nanort::Ray<float>::min_t)
        .def_readwrite("max_t", &nanort::Ray<float>::max_t)
        .def_readwrite("type", &nanort::Ray<float>::type)
    ;

    py::class_<nanort::BVHBuildStatistics> BVHBuildStatistics(_nanort, "BVHBuildStatistics");
    registry.on(_nanort, "BVHBuildStatistics", BVHBuildStatistics);
    BVHBuildStatistics
        .def_readwrite("max_tree_depth", &nanort::BVHBuildStatistics::max_tree_depth)
        .def_readwrite("num_leaf_nodes", &nanort::BVHBuildStatistics::num_leaf_nodes)
        .def_readwrite("num_branch_nodes", &nanort::BVHBuildStatistics::num_branch_nodes)
        .def_readwrite("build_secs", &nanort::BVHBuildStatistics::build_secs)
        .def(py::init<>())
    ;

    py::class_<nanort::BVHTraceOptions> BVHTraceOptions(_nanort, "BVHTraceOptions");
    registry.on(_nanort, "BVHTraceOptions", BVHTraceOptions);
    BVHTraceOptions
        .def_readonly("prim_ids_range", &nanort::BVHTraceOptions::prim_ids_range)
        .def_readwrite("skip_prim_id", &nanort::BVHTraceOptions::skip_prim_id)
        .def_readwrite("cull_back_face", &nanort::BVHTraceOptions::cull_back_face)
        .def_readonly("pad", &nanort::BVHTraceOptions::pad)
        .def(py::init<>())
    ;

    py::class_<nanort::BVHAccel<float>> BVHAccel_float(_nanort, "BVHAccel_float");
    registry.on(_nanort, "BVHAccel_float", BVHAccel_float);
    BVHAccel_float
        .def(py::init<>())
        .def("get_statistics", &nanort::BVHAccel<float>::GetStatistics
            , py::return_value_policy::automatic_reference)
        .def("debug", &nanort::BVHAccel<float>::Debug
            , py::return_value_policy::automatic_reference)
        .def("get_nodes", &nanort::BVHAccel<float>::GetNodes
            , py::return_value_policy::reference)
        .def("get_indices", &nanort::BVHAccel<float>::GetIndices
            , py::return_value_policy::reference)
        .def("bounding_box", [](nanort::BVHAccel<float>& self, std::array<float, 3>& bmin, std::array<float, 3>& bmax)
            {
                self.BoundingBox(&bmin[0], &bmax[0]);
                return std::make_tuple(bmin, bmax);
            }
            , py::arg("bmin")
            , py::arg("bmax")
            , py::return_value_policy::automatic_reference)
        .def("is_valid", &nanort::BVHAccel<float>::IsValid
            , py::return_value_policy::automatic_reference)
    ;


}