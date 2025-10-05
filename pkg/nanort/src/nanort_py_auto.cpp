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

void init_nanort_py_auto(py::module &_nanort, Registry &registry) {
    py::enum_<nanort::RayType>(_nanort, "RayType", py::arithmetic())
        .value("RAY_TYPE_NONE", nanort::RayType::RAY_TYPE_NONE)
        .value("RAY_TYPE_PRIMARY", nanort::RayType::RAY_TYPE_PRIMARY)
        .value("RAY_TYPE_SECONDARY", nanort::RayType::RAY_TYPE_SECONDARY)
        .value("RAY_TYPE_DIFFUSE", nanort::RayType::RAY_TYPE_DIFFUSE)
        .value("RAY_TYPE_REFLECTION", nanort::RayType::RAY_TYPE_REFLECTION)
        .value("RAY_TYPE_REFRACTION", nanort::RayType::RAY_TYPE_REFRACTION)
        .export_values()
    ;
    py::class_<nanort::Ray<double>> _Ray(_nanort, "Ray");
    registry.on(_nanort, "Ray", _Ray);
        _Ray
        .def(py::init<>())
        .def_readonly("org", &nanort::Ray<double>::org)
        .def_readonly("dir", &nanort::Ray<double>::dir)
        .def_readwrite("min_t", &nanort::Ray<double>::min_t)
        .def_readwrite("max_t", &nanort::Ray<double>::max_t)
        .def_readwrite("type", &nanort::Ray<double>::type)
    ;

    py::class_<nanort::BVHBuildOptions<double>> _BVHBuildOptions(_nanort, "BVHBuildOptions");
    registry.on(_nanort, "BVHBuildOptions", _BVHBuildOptions);
        _BVHBuildOptions
        .def_readwrite("cost_t_aabb", &nanort::BVHBuildOptions<double>::cost_t_aabb)
        .def_readwrite("min_leaf_primitives", &nanort::BVHBuildOptions<double>::min_leaf_primitives)
        .def_readwrite("max_tree_depth", &nanort::BVHBuildOptions<double>::max_tree_depth)
        .def_readwrite("bin_size", &nanort::BVHBuildOptions<double>::bin_size)
        .def_readwrite("shallow_depth", &nanort::BVHBuildOptions<double>::shallow_depth)
        .def_readwrite("min_primitives_for_parallel_build", &nanort::BVHBuildOptions<double>::min_primitives_for_parallel_build)
        .def_readwrite("cache_bbox", &nanort::BVHBuildOptions<double>::cache_bbox)
        .def_readonly("pad", &nanort::BVHBuildOptions<double>::pad)
        .def(py::init<>())
    ;

    py::class_<nanort::BVHBuildStatistics> _BVHBuildStatistics(_nanort, "BVHBuildStatistics");
    registry.on(_nanort, "BVHBuildStatistics", _BVHBuildStatistics);
        _BVHBuildStatistics
        .def_readwrite("max_tree_depth", &nanort::BVHBuildStatistics::max_tree_depth)
        .def_readwrite("num_leaf_nodes", &nanort::BVHBuildStatistics::num_leaf_nodes)
        .def_readwrite("num_branch_nodes", &nanort::BVHBuildStatistics::num_branch_nodes)
        .def_readwrite("build_secs", &nanort::BVHBuildStatistics::build_secs)
        .def(py::init<>())
    ;

    py::class_<nanort::BVHTraceOptions> _BVHTraceOptions(_nanort, "BVHTraceOptions");
    registry.on(_nanort, "BVHTraceOptions", _BVHTraceOptions);
        _BVHTraceOptions
        .def_readonly("prim_ids_range", &nanort::BVHTraceOptions::prim_ids_range)
        .def_readwrite("skip_prim_id", &nanort::BVHTraceOptions::skip_prim_id)
        .def_readwrite("cull_back_face", &nanort::BVHTraceOptions::cull_back_face)
        .def_readonly("pad", &nanort::BVHTraceOptions::pad)
        .def(py::init<>())
    ;

    py::class_<nanort::BVHAccel<double>> _BVHAccel(_nanort, "BVHAccel");
    registry.on(_nanort, "BVHAccel", _BVHAccel);
        _BVHAccel
        .def(py::init<>())
        .def("get_statistics", &nanort::BVHAccel<double>::GetStatistics
            , py::return_value_policy::automatic_reference)
        .def("debug", &nanort::BVHAccel<double>::Debug
            , py::return_value_policy::automatic_reference)
        .def("get_nodes", &nanort::BVHAccel<double>::GetNodes
            , py::return_value_policy::reference)
        .def("get_indices", &nanort::BVHAccel<double>::GetIndices
            , py::return_value_policy::reference)
        .def("bounding_box", [](nanort::BVHAccel<double>& self, std::array<double, 3>& bmin, std::array<double, 3>& bmax)
            {
                self.BoundingBox(&bmin[0], &bmax[0]);
                return std::make_tuple(bmin, bmax);
            }
            , py::arg("bmin")
            , py::arg("bmax")
            , py::return_value_policy::automatic_reference)
        .def("is_valid", &nanort::BVHAccel<double>::IsValid
            , py::return_value_policy::automatic_reference)
    ;

    py::class_<nanort::TriangleSAHPred<double>> _TriangleSAHPred(_nanort, "TriangleSAHPred");
    registry.on(_nanort, "TriangleSAHPred", _TriangleSAHPred);
        _TriangleSAHPred
        .def(py::init<const double *, const unsigned int *, unsigned long>()
        , py::arg("vertices")
        , py::arg("faces")
        , py::arg("vertex_stride_bytes")
        )
        .def("set", &nanort::TriangleSAHPred<double>::Set
            , py::arg("axis")
            , py::arg("pos")
            , py::return_value_policy::automatic_reference)
    ;

    py::class_<nanort::TriangleMesh<double>> _TriangleMesh(_nanort, "TriangleMesh");
    registry.on(_nanort, "TriangleMesh", _TriangleMesh);
        _TriangleMesh
        .def(py::init<const double *, const unsigned int *, const unsigned long>()
        , py::arg("vertices")
        , py::arg("faces")
        , py::arg("vertex_stride_bytes")
        )
        .def("bounding_box", &nanort::TriangleMesh<double>::BoundingBox
            , py::arg("bmin")
            , py::arg("bmax")
            , py::arg("prim_index")
            , py::return_value_policy::automatic_reference)
        .def("bounding_box_and_center", &nanort::TriangleMesh<double>::BoundingBoxAndCenter
            , py::arg("bmin")
            , py::arg("bmax")
            , py::arg("center")
            , py::arg("prim_index")
            , py::return_value_policy::automatic_reference)
        .def_readwrite("vertices", &nanort::TriangleMesh<double>::vertices_)
        .def_readwrite("faces", &nanort::TriangleMesh<double>::faces_)
        .def_readonly("vertex_stride_bytes", &nanort::TriangleMesh<double>::vertex_stride_bytes_)
        .def("get_vertices", &nanort::TriangleMesh<double>::GetVertices
            , py::return_value_policy::automatic_reference)
        .def("get_faces", &nanort::TriangleMesh<double>::GetFaces
            , py::return_value_policy::automatic_reference)
        .def("get_vertex_stride_bytes", &nanort::TriangleMesh<double>::GetVertexStrideBytes
            , py::return_value_policy::automatic_reference)
    ;


}