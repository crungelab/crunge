#include <limits>
//#include <iostream>
#include <sstream>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>

//#include <crunge/box2d/crunge-box2d.h>
//#include <crunge/box2d/conversions.h>

#include <box2d/collision.h>

namespace py = pybind11;

void init_collision_py_auto(py::module &_box2d, Registry &registry) {
    py::class_<b2RayCastInput> _RayCastInput(_box2d, "RayCastInput");
    registry.on(_box2d, "RayCastInput", _RayCastInput);
        _RayCastInput
        .def_readwrite("origin", &b2RayCastInput::origin)
        .def_readwrite("translation", &b2RayCastInput::translation)
        .def_readwrite("max_fraction", &b2RayCastInput::maxFraction)
    ;

    py::class_<b2ShapeProxy> _ShapeProxy(_box2d, "ShapeProxy");
    registry.on(_box2d, "ShapeProxy", _ShapeProxy);
        _ShapeProxy
        .def_readonly("points", &b2ShapeProxy::points)
        .def_readwrite("count", &b2ShapeProxy::count)
        .def_readwrite("radius", &b2ShapeProxy::radius)
    ;

    py::class_<b2ShapeCastInput> _ShapeCastInput(_box2d, "ShapeCastInput");
    registry.on(_box2d, "ShapeCastInput", _ShapeCastInput);
        _ShapeCastInput
        .def_readwrite("proxy", &b2ShapeCastInput::proxy)
        .def_readwrite("translation", &b2ShapeCastInput::translation)
        .def_readwrite("max_fraction", &b2ShapeCastInput::maxFraction)
        .def_readwrite("can_encroach", &b2ShapeCastInput::canEncroach)
    ;

    py::class_<b2CastOutput> _CastOutput(_box2d, "CastOutput");
    registry.on(_box2d, "CastOutput", _CastOutput);
        _CastOutput
        .def_readwrite("normal", &b2CastOutput::normal)
        .def_readwrite("point", &b2CastOutput::point)
        .def_readwrite("fraction", &b2CastOutput::fraction)
        .def_readwrite("iterations", &b2CastOutput::iterations)
        .def_readwrite("hit", &b2CastOutput::hit)
    ;

    py::class_<b2MassData> _MassData(_box2d, "MassData");
    registry.on(_box2d, "MassData", _MassData);
        _MassData
        .def_readwrite("mass", &b2MassData::mass)
        .def_readwrite("center", &b2MassData::center)
        .def_readwrite("rotational_inertia", &b2MassData::rotationalInertia)
    ;

    py::class_<b2Circle> _Circle(_box2d, "Circle");
    registry.on(_box2d, "Circle", _Circle);
        _Circle
        .def_readwrite("center", &b2Circle::center)
        .def_readwrite("radius", &b2Circle::radius)
        .def(py::init([](const py::kwargs& kwargs)
        {
            b2Circle obj{};
            if (kwargs.contains("center"))
            {
                auto value = kwargs["center"].cast<struct b2Vec2>();
                obj.center = value;
            }
            if (kwargs.contains("radius"))
            {
                auto value = kwargs["radius"].cast<float>();
                obj.radius = value;
            }
            return obj;
        }))
        .def("__repr__", [](const b2Circle &self) {
            std::stringstream ss;
            ss << "Circle(";
            ss << "center=" << py::repr(py::cast(self.center)).cast<std::string>();
            ss << ", ";
            ss << "radius=" << py::repr(py::cast(self.radius)).cast<std::string>();
            ss << ")";
            return ss.str();
        })
    ;

    py::class_<b2Capsule> _Capsule(_box2d, "Capsule");
    registry.on(_box2d, "Capsule", _Capsule);
        _Capsule
        .def_readwrite("center1", &b2Capsule::center1)
        .def_readwrite("center2", &b2Capsule::center2)
        .def_readwrite("radius", &b2Capsule::radius)
    ;

    py::class_<b2Polygon> _Polygon(_box2d, "Polygon");
    registry.on(_box2d, "Polygon", _Polygon);
        _Polygon
        .def_readonly("vertices", &b2Polygon::vertices)
        .def_readonly("normals", &b2Polygon::normals)
        .def_readwrite("centroid", &b2Polygon::centroid)
        .def_readwrite("radius", &b2Polygon::radius)
        .def_readwrite("count", &b2Polygon::count)
        .def("__repr__", [](const b2Polygon &self) {
            std::stringstream ss;
            ss << "Polygon(";
            ss << "vertices=" << py::repr(py::cast(self.vertices)).cast<std::string>();
            ss << ", ";
            ss << "normals=" << py::repr(py::cast(self.normals)).cast<std::string>();
            ss << ", ";
            ss << "centroid=" << py::repr(py::cast(self.centroid)).cast<std::string>();
            ss << ", ";
            ss << "radius=" << py::repr(py::cast(self.radius)).cast<std::string>();
            ss << ", ";
            ss << "count=" << py::repr(py::cast(self.count)).cast<std::string>();
            ss << ")";
            return ss.str();
        })
    ;

    py::class_<b2Segment> _Segment(_box2d, "Segment");
    registry.on(_box2d, "Segment", _Segment);
        _Segment
        .def_readwrite("point1", &b2Segment::point1)
        .def_readwrite("point2", &b2Segment::point2)
    ;

    py::class_<b2ChainSegment> _ChainSegment(_box2d, "ChainSegment");
    registry.on(_box2d, "ChainSegment", _ChainSegment);
        _ChainSegment
        .def_readwrite("ghost1", &b2ChainSegment::ghost1)
        .def_readwrite("segment", &b2ChainSegment::segment)
        .def_readwrite("ghost2", &b2ChainSegment::ghost2)
        .def_readwrite("chain_id", &b2ChainSegment::chainId)
    ;

    _box2d
    .def("is_valid_ray", &b2IsValidRay
        , py::arg("input")
        , py::return_value_policy::automatic_reference)
    .def("make_polygon", &b2MakePolygon
        , py::arg("hull")
        , py::arg("radius")
        , py::return_value_policy::automatic_reference)
    .def("make_offset_polygon", &b2MakeOffsetPolygon
        , py::arg("hull")
        , py::arg("position")
        , py::arg("rotation")
        , py::return_value_policy::automatic_reference)
    .def("make_offset_rounded_polygon", &b2MakeOffsetRoundedPolygon
        , py::arg("hull")
        , py::arg("position")
        , py::arg("rotation")
        , py::arg("radius")
        , py::return_value_policy::automatic_reference)
    .def("make_square", &b2MakeSquare
        , py::arg("half_width")
        , py::return_value_policy::automatic_reference)
    .def("make_box", &b2MakeBox
        , py::arg("half_width")
        , py::arg("half_height")
        , py::return_value_policy::automatic_reference)
    .def("make_rounded_box", &b2MakeRoundedBox
        , py::arg("half_width")
        , py::arg("half_height")
        , py::arg("radius")
        , py::return_value_policy::automatic_reference)
    .def("make_offset_box", &b2MakeOffsetBox
        , py::arg("half_width")
        , py::arg("half_height")
        , py::arg("center")
        , py::arg("rotation")
        , py::return_value_policy::automatic_reference)
    .def("make_offset_rounded_box", &b2MakeOffsetRoundedBox
        , py::arg("half_width")
        , py::arg("half_height")
        , py::arg("center")
        , py::arg("rotation")
        , py::arg("radius")
        , py::return_value_policy::automatic_reference)
    .def("transform_polygon", &b2TransformPolygon
        , py::arg("transform")
        , py::arg("polygon")
        , py::return_value_policy::automatic_reference)
    .def("compute_circle_mass", &b2ComputeCircleMass
        , py::arg("shape")
        , py::arg("density")
        , py::return_value_policy::automatic_reference)
    .def("compute_capsule_mass", &b2ComputeCapsuleMass
        , py::arg("shape")
        , py::arg("density")
        , py::return_value_policy::automatic_reference)
    .def("compute_polygon_mass", &b2ComputePolygonMass
        , py::arg("shape")
        , py::arg("density")
        , py::return_value_policy::automatic_reference)
    .def("compute_circle_aabb", &b2ComputeCircleAABB
        , py::arg("shape")
        , py::arg("transform")
        , py::return_value_policy::automatic_reference)
    .def("compute_capsule_aabb", &b2ComputeCapsuleAABB
        , py::arg("shape")
        , py::arg("transform")
        , py::return_value_policy::automatic_reference)
    .def("compute_polygon_aabb", &b2ComputePolygonAABB
        , py::arg("shape")
        , py::arg("transform")
        , py::return_value_policy::automatic_reference)
    .def("compute_segment_aabb", &b2ComputeSegmentAABB
        , py::arg("shape")
        , py::arg("transform")
        , py::return_value_policy::automatic_reference)
    .def("point_in_circle", &b2PointInCircle
        , py::arg("shape")
        , py::arg("point")
        , py::return_value_policy::automatic_reference)
    .def("point_in_capsule", &b2PointInCapsule
        , py::arg("shape")
        , py::arg("point")
        , py::return_value_policy::automatic_reference)
    .def("point_in_polygon", &b2PointInPolygon
        , py::arg("shape")
        , py::arg("point")
        , py::return_value_policy::automatic_reference)
    .def("ray_cast_circle", &b2RayCastCircle
        , py::arg("shape")
        , py::arg("input")
        , py::return_value_policy::automatic_reference)
    .def("ray_cast_capsule", &b2RayCastCapsule
        , py::arg("shape")
        , py::arg("input")
        , py::return_value_policy::automatic_reference)
    .def("ray_cast_segment", &b2RayCastSegment
        , py::arg("shape")
        , py::arg("input")
        , py::arg("one_sided")
        , py::return_value_policy::automatic_reference)
    .def("ray_cast_polygon", &b2RayCastPolygon
        , py::arg("shape")
        , py::arg("input")
        , py::return_value_policy::automatic_reference)
    .def("shape_cast_circle", &b2ShapeCastCircle
        , py::arg("shape")
        , py::arg("input")
        , py::return_value_policy::automatic_reference)
    .def("shape_cast_capsule", &b2ShapeCastCapsule
        , py::arg("shape")
        , py::arg("input")
        , py::return_value_policy::automatic_reference)
    .def("shape_cast_segment", &b2ShapeCastSegment
        , py::arg("shape")
        , py::arg("input")
        , py::return_value_policy::automatic_reference)
    .def("shape_cast_polygon", &b2ShapeCastPolygon
        , py::arg("shape")
        , py::arg("input")
        , py::return_value_policy::automatic_reference)
    ;

    py::class_<b2Hull> _Hull(_box2d, "Hull");
    registry.on(_box2d, "Hull", _Hull);
        _Hull
        .def_readonly("points", &b2Hull::points)
        .def_readwrite("count", &b2Hull::count)
    ;

    _box2d
    .def("compute_hull", &b2ComputeHull
        , py::arg("points")
        , py::arg("count")
        , py::return_value_policy::automatic_reference)
    .def("validate_hull", &b2ValidateHull
        , py::arg("hull")
        , py::return_value_policy::automatic_reference)
    ;

    py::class_<b2SegmentDistanceResult> _SegmentDistanceResult(_box2d, "SegmentDistanceResult");
    registry.on(_box2d, "SegmentDistanceResult", _SegmentDistanceResult);
        _SegmentDistanceResult
        .def_readwrite("closest1", &b2SegmentDistanceResult::closest1)
        .def_readwrite("closest2", &b2SegmentDistanceResult::closest2)
        .def_readwrite("fraction1", &b2SegmentDistanceResult::fraction1)
        .def_readwrite("fraction2", &b2SegmentDistanceResult::fraction2)
        .def_readwrite("distance_squared", &b2SegmentDistanceResult::distanceSquared)
    ;

    _box2d
    .def("segment_distance", &b2SegmentDistance
        , py::arg("p1")
        , py::arg("q1")
        , py::arg("p2")
        , py::arg("q2")
        , py::return_value_policy::automatic_reference)
    ;

    py::class_<b2SimplexCache> _SimplexCache(_box2d, "SimplexCache");
    registry.on(_box2d, "SimplexCache", _SimplexCache);
        _SimplexCache
        .def_readwrite("count", &b2SimplexCache::count)
        .def_readonly("index_a", &b2SimplexCache::indexA)
        .def_readonly("index_b", &b2SimplexCache::indexB)
    ;

    py::class_<b2DistanceInput> _DistanceInput(_box2d, "DistanceInput");
    registry.on(_box2d, "DistanceInput", _DistanceInput);
        _DistanceInput
        .def_readwrite("proxy_a", &b2DistanceInput::proxyA)
        .def_readwrite("proxy_b", &b2DistanceInput::proxyB)
        .def_readwrite("transform_a", &b2DistanceInput::transformA)
        .def_readwrite("transform_b", &b2DistanceInput::transformB)
        .def_readwrite("use_radii", &b2DistanceInput::useRadii)
    ;

    py::class_<b2DistanceOutput> _DistanceOutput(_box2d, "DistanceOutput");
    registry.on(_box2d, "DistanceOutput", _DistanceOutput);
        _DistanceOutput
        .def_readwrite("point_a", &b2DistanceOutput::pointA)
        .def_readwrite("point_b", &b2DistanceOutput::pointB)
        .def_readwrite("normal", &b2DistanceOutput::normal)
        .def_readwrite("distance", &b2DistanceOutput::distance)
        .def_readwrite("iterations", &b2DistanceOutput::iterations)
        .def_readwrite("simplex_count", &b2DistanceOutput::simplexCount)
    ;

    py::class_<b2SimplexVertex> _SimplexVertex(_box2d, "SimplexVertex");
    registry.on(_box2d, "SimplexVertex", _SimplexVertex);
        _SimplexVertex
        .def_readwrite("w_a", &b2SimplexVertex::wA)
        .def_readwrite("w_b", &b2SimplexVertex::wB)
        .def_readwrite("w", &b2SimplexVertex::w)
        .def_readwrite("a", &b2SimplexVertex::a)
        .def_readwrite("index_a", &b2SimplexVertex::indexA)
        .def_readwrite("index_b", &b2SimplexVertex::indexB)
    ;

    py::class_<b2Simplex> _Simplex(_box2d, "Simplex");
    registry.on(_box2d, "Simplex", _Simplex);
        _Simplex
        .def_readwrite("v1", &b2Simplex::v1)
        .def_readwrite("v2", &b2Simplex::v2)
        .def_readwrite("v3", &b2Simplex::v3)
        .def_readwrite("count", &b2Simplex::count)
    ;

    _box2d
    .def("shape_distance", &b2ShapeDistance
        , py::arg("input")
        , py::arg("cache")
        , py::arg("simplexes")
        , py::arg("simplex_capacity")
        , py::return_value_policy::automatic_reference)
    ;

    py::class_<b2ShapeCastPairInput> _ShapeCastPairInput(_box2d, "ShapeCastPairInput");
    registry.on(_box2d, "ShapeCastPairInput", _ShapeCastPairInput);
        _ShapeCastPairInput
        .def_readwrite("proxy_a", &b2ShapeCastPairInput::proxyA)
        .def_readwrite("proxy_b", &b2ShapeCastPairInput::proxyB)
        .def_readwrite("transform_a", &b2ShapeCastPairInput::transformA)
        .def_readwrite("transform_b", &b2ShapeCastPairInput::transformB)
        .def_readwrite("translation_b", &b2ShapeCastPairInput::translationB)
        .def_readwrite("max_fraction", &b2ShapeCastPairInput::maxFraction)
        .def_readwrite("can_encroach", &b2ShapeCastPairInput::canEncroach)
    ;

    _box2d
    .def("shape_cast", &b2ShapeCast
        , py::arg("input")
        , py::return_value_policy::automatic_reference)
    .def("make_proxy", &b2MakeProxy
        , py::arg("points")
        , py::arg("count")
        , py::arg("radius")
        , py::return_value_policy::automatic_reference)
    .def("make_offset_proxy", &b2MakeOffsetProxy
        , py::arg("points")
        , py::arg("count")
        , py::arg("radius")
        , py::arg("position")
        , py::arg("rotation")
        , py::return_value_policy::automatic_reference)
    ;

    py::class_<b2Sweep> _Sweep(_box2d, "Sweep");
    registry.on(_box2d, "Sweep", _Sweep);
        _Sweep
        .def_readwrite("local_center", &b2Sweep::localCenter)
        .def_readwrite("c1", &b2Sweep::c1)
        .def_readwrite("c2", &b2Sweep::c2)
        .def_readwrite("q1", &b2Sweep::q1)
        .def_readwrite("q2", &b2Sweep::q2)
    ;

    _box2d
    .def("get_sweep_transform", &b2GetSweepTransform
        , py::arg("sweep")
        , py::arg("time")
        , py::return_value_policy::automatic_reference)
    ;

    py::class_<b2TOIInput> _TOIInput(_box2d, "TOIInput");
    registry.on(_box2d, "TOIInput", _TOIInput);
        _TOIInput
        .def_readwrite("proxy_a", &b2TOIInput::proxyA)
        .def_readwrite("proxy_b", &b2TOIInput::proxyB)
        .def_readwrite("sweep_a", &b2TOIInput::sweepA)
        .def_readwrite("sweep_b", &b2TOIInput::sweepB)
        .def_readwrite("max_fraction", &b2TOIInput::maxFraction)
    ;

    py::enum_<b2TOIState>(_box2d, "TOIState", py::arithmetic())
        .value("TOI_STATE_UNKNOWN", b2TOIState::b2_toiStateUnknown)
        .value("TOI_STATE_FAILED", b2TOIState::b2_toiStateFailed)
        .value("TOI_STATE_OVERLAPPED", b2TOIState::b2_toiStateOverlapped)
        .value("TOI_STATE_HIT", b2TOIState::b2_toiStateHit)
        .value("TOI_STATE_SEPARATED", b2TOIState::b2_toiStateSeparated)
        .export_values()
    ;
    py::class_<b2TOIOutput> _TOIOutput(_box2d, "TOIOutput");
    registry.on(_box2d, "TOIOutput", _TOIOutput);
        _TOIOutput
        .def_readwrite("state", &b2TOIOutput::state)
        .def_readwrite("point", &b2TOIOutput::point)
        .def_readwrite("normal", &b2TOIOutput::normal)
        .def_readwrite("fraction", &b2TOIOutput::fraction)
    ;

    _box2d
    .def("time_of_impact", &b2TimeOfImpact
        , py::arg("input")
        , py::return_value_policy::automatic_reference)
    ;

    py::class_<b2ManifoldPoint> _ManifoldPoint(_box2d, "ManifoldPoint");
    registry.on(_box2d, "ManifoldPoint", _ManifoldPoint);
        _ManifoldPoint
        .def_readwrite("point", &b2ManifoldPoint::point)
        .def_readwrite("anchor_a", &b2ManifoldPoint::anchorA)
        .def_readwrite("anchor_b", &b2ManifoldPoint::anchorB)
        .def_readwrite("separation", &b2ManifoldPoint::separation)
        .def_readwrite("normal_impulse", &b2ManifoldPoint::normalImpulse)
        .def_readwrite("tangent_impulse", &b2ManifoldPoint::tangentImpulse)
        .def_readwrite("total_normal_impulse", &b2ManifoldPoint::totalNormalImpulse)
        .def_readwrite("normal_velocity", &b2ManifoldPoint::normalVelocity)
        .def_readwrite("id", &b2ManifoldPoint::id)
        .def_readwrite("persisted", &b2ManifoldPoint::persisted)
    ;

    py::class_<b2Manifold> _Manifold(_box2d, "Manifold");
    registry.on(_box2d, "Manifold", _Manifold);
        _Manifold
        .def_readwrite("normal", &b2Manifold::normal)
        .def_readwrite("rolling_impulse", &b2Manifold::rollingImpulse)
        .def_readonly("points", &b2Manifold::points)
        .def_readwrite("point_count", &b2Manifold::pointCount)
    ;

    _box2d
    .def("collide_circles", &b2CollideCircles
        , py::arg("circle_a")
        , py::arg("xf_a")
        , py::arg("circle_b")
        , py::arg("xf_b")
        , py::return_value_policy::automatic_reference)
    .def("collide_capsule_and_circle", &b2CollideCapsuleAndCircle
        , py::arg("capsule_a")
        , py::arg("xf_a")
        , py::arg("circle_b")
        , py::arg("xf_b")
        , py::return_value_policy::automatic_reference)
    .def("collide_segment_and_circle", &b2CollideSegmentAndCircle
        , py::arg("segment_a")
        , py::arg("xf_a")
        , py::arg("circle_b")
        , py::arg("xf_b")
        , py::return_value_policy::automatic_reference)
    .def("collide_polygon_and_circle", &b2CollidePolygonAndCircle
        , py::arg("polygon_a")
        , py::arg("xf_a")
        , py::arg("circle_b")
        , py::arg("xf_b")
        , py::return_value_policy::automatic_reference)
    .def("collide_capsules", &b2CollideCapsules
        , py::arg("capsule_a")
        , py::arg("xf_a")
        , py::arg("capsule_b")
        , py::arg("xf_b")
        , py::return_value_policy::automatic_reference)
    .def("collide_segment_and_capsule", &b2CollideSegmentAndCapsule
        , py::arg("segment_a")
        , py::arg("xf_a")
        , py::arg("capsule_b")
        , py::arg("xf_b")
        , py::return_value_policy::automatic_reference)
    .def("collide_polygon_and_capsule", &b2CollidePolygonAndCapsule
        , py::arg("polygon_a")
        , py::arg("xf_a")
        , py::arg("capsule_b")
        , py::arg("xf_b")
        , py::return_value_policy::automatic_reference)
    .def("collide_polygons", &b2CollidePolygons
        , py::arg("polygon_a")
        , py::arg("xf_a")
        , py::arg("polygon_b")
        , py::arg("xf_b")
        , py::return_value_policy::automatic_reference)
    .def("collide_segment_and_polygon", &b2CollideSegmentAndPolygon
        , py::arg("segment_a")
        , py::arg("xf_a")
        , py::arg("polygon_b")
        , py::arg("xf_b")
        , py::return_value_policy::automatic_reference)
    .def("collide_chain_segment_and_circle", &b2CollideChainSegmentAndCircle
        , py::arg("segment_a")
        , py::arg("xf_a")
        , py::arg("circle_b")
        , py::arg("xf_b")
        , py::return_value_policy::automatic_reference)
    .def("collide_chain_segment_and_capsule", &b2CollideChainSegmentAndCapsule
        , py::arg("segment_a")
        , py::arg("xf_a")
        , py::arg("capsule_b")
        , py::arg("xf_b")
        , py::arg("cache")
        , py::return_value_policy::automatic_reference)
    .def("collide_chain_segment_and_polygon", &b2CollideChainSegmentAndPolygon
        , py::arg("segment_a")
        , py::arg("xf_a")
        , py::arg("polygon_b")
        , py::arg("xf_b")
        , py::arg("cache")
        , py::return_value_policy::automatic_reference)
    ;

    py::class_<b2TreeStats> _TreeStats(_box2d, "TreeStats");
    registry.on(_box2d, "TreeStats", _TreeStats);
        _TreeStats
        .def_readwrite("node_visits", &b2TreeStats::nodeVisits)
        .def_readwrite("leaf_visits", &b2TreeStats::leafVisits)
    ;

    _box2d
    .def("dynamic_tree_create", &b2DynamicTree_Create
        , py::return_value_policy::automatic_reference)
    .def("dynamic_tree_destroy", &b2DynamicTree_Destroy
        , py::arg("tree")
        , py::return_value_policy::automatic_reference)
    .def("dynamic_tree_create_proxy", &b2DynamicTree_CreateProxy
        , py::arg("tree")
        , py::arg("aabb")
        , py::arg("category_bits")
        , py::arg("user_data")
        , py::return_value_policy::automatic_reference)
    .def("dynamic_tree_destroy_proxy", &b2DynamicTree_DestroyProxy
        , py::arg("tree")
        , py::arg("proxy_id")
        , py::return_value_policy::automatic_reference)
    .def("dynamic_tree_move_proxy", &b2DynamicTree_MoveProxy
        , py::arg("tree")
        , py::arg("proxy_id")
        , py::arg("aabb")
        , py::return_value_policy::automatic_reference)
    .def("dynamic_tree_enlarge_proxy", &b2DynamicTree_EnlargeProxy
        , py::arg("tree")
        , py::arg("proxy_id")
        , py::arg("aabb")
        , py::return_value_policy::automatic_reference)
    .def("dynamic_tree_set_category_bits", &b2DynamicTree_SetCategoryBits
        , py::arg("tree")
        , py::arg("proxy_id")
        , py::arg("category_bits")
        , py::return_value_policy::automatic_reference)
    .def("dynamic_tree_get_category_bits", &b2DynamicTree_GetCategoryBits
        , py::arg("tree")
        , py::arg("proxy_id")
        , py::return_value_policy::automatic_reference)
    .def("dynamic_tree_query", &b2DynamicTree_Query
        , py::arg("tree")
        , py::arg("aabb")
        , py::arg("mask_bits")
        , py::arg("callback")
        , py::arg("context")
        , py::return_value_policy::automatic_reference)
    .def("dynamic_tree_query_all", &b2DynamicTree_QueryAll
        , py::arg("tree")
        , py::arg("aabb")
        , py::arg("callback")
        , py::arg("context")
        , py::return_value_policy::automatic_reference)
    .def("dynamic_tree_ray_cast", &b2DynamicTree_RayCast
        , py::arg("tree")
        , py::arg("input")
        , py::arg("mask_bits")
        , py::arg("callback")
        , py::arg("context")
        , py::return_value_policy::automatic_reference)
    .def("dynamic_tree_shape_cast", &b2DynamicTree_ShapeCast
        , py::arg("tree")
        , py::arg("input")
        , py::arg("mask_bits")
        , py::arg("callback")
        , py::arg("context")
        , py::return_value_policy::automatic_reference)
    .def("dynamic_tree_get_height", &b2DynamicTree_GetHeight
        , py::arg("tree")
        , py::return_value_policy::automatic_reference)
    .def("dynamic_tree_get_area_ratio", &b2DynamicTree_GetAreaRatio
        , py::arg("tree")
        , py::return_value_policy::automatic_reference)
    .def("dynamic_tree_get_root_bounds", &b2DynamicTree_GetRootBounds
        , py::arg("tree")
        , py::return_value_policy::automatic_reference)
    .def("dynamic_tree_get_proxy_count", &b2DynamicTree_GetProxyCount
        , py::arg("tree")
        , py::return_value_policy::automatic_reference)
    .def("dynamic_tree_rebuild", &b2DynamicTree_Rebuild
        , py::arg("tree")
        , py::arg("full_build")
        , py::return_value_policy::automatic_reference)
    .def("dynamic_tree_get_byte_count", &b2DynamicTree_GetByteCount
        , py::arg("tree")
        , py::return_value_policy::automatic_reference)
    .def("dynamic_tree_get_user_data", &b2DynamicTree_GetUserData
        , py::arg("tree")
        , py::arg("proxy_id")
        , py::return_value_policy::automatic_reference)
    .def("dynamic_tree_get_aabb", &b2DynamicTree_GetAABB
        , py::arg("tree")
        , py::arg("proxy_id")
        , py::return_value_policy::automatic_reference)
    .def("dynamic_tree_validate", &b2DynamicTree_Validate
        , py::arg("tree")
        , py::return_value_policy::automatic_reference)
    .def("dynamic_tree_validate_no_enlarged", &b2DynamicTree_ValidateNoEnlarged
        , py::arg("tree")
        , py::return_value_policy::automatic_reference)
    ;

    py::class_<b2PlaneResult> _PlaneResult(_box2d, "PlaneResult");
    registry.on(_box2d, "PlaneResult", _PlaneResult);
        _PlaneResult
        .def_readwrite("plane", &b2PlaneResult::plane)
        .def_readwrite("point", &b2PlaneResult::point)
        .def_readwrite("hit", &b2PlaneResult::hit)
    ;

    py::class_<b2CollisionPlane> _CollisionPlane(_box2d, "CollisionPlane");
    registry.on(_box2d, "CollisionPlane", _CollisionPlane);
        _CollisionPlane
        .def_readwrite("plane", &b2CollisionPlane::plane)
        .def_readwrite("push_limit", &b2CollisionPlane::pushLimit)
        .def_readwrite("push", &b2CollisionPlane::push)
        .def_readwrite("clip_velocity", &b2CollisionPlane::clipVelocity)
    ;

    py::class_<b2PlaneSolverResult> _PlaneSolverResult(_box2d, "PlaneSolverResult");
    registry.on(_box2d, "PlaneSolverResult", _PlaneSolverResult);
        _PlaneSolverResult
        .def_readwrite("translation", &b2PlaneSolverResult::translation)
        .def_readwrite("iteration_count", &b2PlaneSolverResult::iterationCount)
    ;

    _box2d
    .def("solve_planes", &b2SolvePlanes
        , py::arg("target_delta")
        , py::arg("planes")
        , py::arg("count")
        , py::return_value_policy::automatic_reference)
    .def("clip_vector", &b2ClipVector
        , py::arg("vector")
        , py::arg("planes")
        , py::arg("count")
        , py::return_value_policy::automatic_reference)
    ;


}