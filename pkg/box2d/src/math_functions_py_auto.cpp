#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

//#include <iostream>

#include <cxbind/cxbind.h>

//#include <crunge/tmx/crunge-tmx.h>
//#include <crunge/tmx/conversions.h>

//#include <tmxlite/Map.hpp>
//#include <tmxlite/ImageLayer.hpp>

#include <box2d/math_functions.h>

namespace py = pybind11;

void init_math_functions_py_auto(py::module &_box2d, Registry &registry) {
    py::class_<b2Vec2> _Vec2(_box2d, "Vec2");
    registry.on(_box2d, "Vec2", _Vec2);
        _Vec2
        .def_readwrite("x", &b2Vec2::x)
        .def_readwrite("y", &b2Vec2::y)
        .def(py::init([](float x, float y)
        {
            b2Vec2 obj{};
            obj.x = x;
            obj.y = y;
            return obj;
        }))
    ;

    py::class_<b2CosSin> _CosSin(_box2d, "CosSin");
    registry.on(_box2d, "CosSin", _CosSin);
        _CosSin
        .def_readwrite("cosine", &b2CosSin::cosine)
        .def_readwrite("sine", &b2CosSin::sine)
    ;

    py::class_<b2Rot> _Rot(_box2d, "Rot");
    registry.on(_box2d, "Rot", _Rot);
        _Rot
        .def_readwrite("c", &b2Rot::c)
        .def_readwrite("s", &b2Rot::s)
    ;

    py::class_<b2Transform> _Transform(_box2d, "Transform");
    registry.on(_box2d, "Transform", _Transform);
        _Transform
        .def_readwrite("p", &b2Transform::p)
        .def_readwrite("q", &b2Transform::q)
    ;

    py::class_<b2Mat22> _Mat22(_box2d, "Mat22");
    registry.on(_box2d, "Mat22", _Mat22);
        _Mat22
        .def_readwrite("cx", &b2Mat22::cx)
        .def_readwrite("cy", &b2Mat22::cy)
    ;

    py::class_<b2AABB> _AABB(_box2d, "AABB");
    registry.on(_box2d, "AABB", _AABB);
        _AABB
        .def_readwrite("lower_bound", &b2AABB::lowerBound)
        .def_readwrite("upper_bound", &b2AABB::upperBound)
    ;

    py::class_<b2Plane> _Plane(_box2d, "Plane");
    registry.on(_box2d, "Plane", _Plane);
        _Plane
        .def_readwrite("normal", &b2Plane::normal)
        .def_readwrite("offset", &b2Plane::offset)
    ;

    _box2d
    .def("is_valid_float", &b2IsValidFloat
        , py::arg("a")
        , py::return_value_policy::automatic_reference)
    .def("is_valid_vec2", &b2IsValidVec2
        , py::arg("v")
        , py::return_value_policy::automatic_reference)
    .def("is_valid_rotation", &b2IsValidRotation
        , py::arg("q")
        , py::return_value_policy::automatic_reference)
    .def("is_valid_transform", &b2IsValidTransform
        , py::arg("t")
        , py::return_value_policy::automatic_reference)
    .def("is_valid_aabb", &b2IsValidAABB
        , py::arg("aabb")
        , py::return_value_policy::automatic_reference)
    .def("is_valid_plane", &b2IsValidPlane
        , py::arg("a")
        , py::return_value_policy::automatic_reference)
    .def("min_int", &b2MinInt
        , py::arg("a")
        , py::arg("b")
        , py::return_value_policy::automatic_reference)
    .def("max_int", &b2MaxInt
        , py::arg("a")
        , py::arg("b")
        , py::return_value_policy::automatic_reference)
    .def("abs_int", &b2AbsInt
        , py::arg("a")
        , py::return_value_policy::automatic_reference)
    .def("clamp_int", &b2ClampInt
        , py::arg("a")
        , py::arg("lower")
        , py::arg("upper")
        , py::return_value_policy::automatic_reference)
    .def("min_float", &b2MinFloat
        , py::arg("a")
        , py::arg("b")
        , py::return_value_policy::automatic_reference)
    .def("max_float", &b2MaxFloat
        , py::arg("a")
        , py::arg("b")
        , py::return_value_policy::automatic_reference)
    .def("abs_float", &b2AbsFloat
        , py::arg("a")
        , py::return_value_policy::automatic_reference)
    .def("clamp_float", &b2ClampFloat
        , py::arg("a")
        , py::arg("lower")
        , py::arg("upper")
        , py::return_value_policy::automatic_reference)
    .def("atan2", &b2Atan2
        , py::arg("y")
        , py::arg("x")
        , py::return_value_policy::automatic_reference)
    .def("compute_cos_sin", &b2ComputeCosSin
        , py::arg("radians")
        , py::return_value_policy::automatic_reference)
    .def("dot", &b2Dot
        , py::arg("a")
        , py::arg("b")
        , py::return_value_policy::automatic_reference)
    .def("cross", &b2Cross
        , py::arg("a")
        , py::arg("b")
        , py::return_value_policy::automatic_reference)
    .def("cross_vs", &b2CrossVS
        , py::arg("v")
        , py::arg("s")
        , py::return_value_policy::automatic_reference)
    .def("cross_sv", &b2CrossSV
        , py::arg("s")
        , py::arg("v")
        , py::return_value_policy::automatic_reference)
    .def("left_perp", &b2LeftPerp
        , py::arg("v")
        , py::return_value_policy::automatic_reference)
    .def("right_perp", &b2RightPerp
        , py::arg("v")
        , py::return_value_policy::automatic_reference)
    .def("add", &b2Add
        , py::arg("a")
        , py::arg("b")
        , py::return_value_policy::automatic_reference)
    .def("sub", &b2Sub
        , py::arg("a")
        , py::arg("b")
        , py::return_value_policy::automatic_reference)
    .def("neg", &b2Neg
        , py::arg("a")
        , py::return_value_policy::automatic_reference)
    .def("lerp", &b2Lerp
        , py::arg("a")
        , py::arg("b")
        , py::arg("t")
        , py::return_value_policy::automatic_reference)
    .def("mul", &b2Mul
        , py::arg("a")
        , py::arg("b")
        , py::return_value_policy::automatic_reference)
    .def("mul_sv", &b2MulSV
        , py::arg("s")
        , py::arg("v")
        , py::return_value_policy::automatic_reference)
    .def("mul_add", &b2MulAdd
        , py::arg("a")
        , py::arg("s")
        , py::arg("b")
        , py::return_value_policy::automatic_reference)
    .def("mul_sub", &b2MulSub
        , py::arg("a")
        , py::arg("s")
        , py::arg("b")
        , py::return_value_policy::automatic_reference)
    .def("abs", &b2Abs
        , py::arg("a")
        , py::return_value_policy::automatic_reference)
    .def("min", &b2Min
        , py::arg("a")
        , py::arg("b")
        , py::return_value_policy::automatic_reference)
    .def("max", &b2Max
        , py::arg("a")
        , py::arg("b")
        , py::return_value_policy::automatic_reference)
    .def("clamp", &b2Clamp
        , py::arg("v")
        , py::arg("a")
        , py::arg("b")
        , py::return_value_policy::automatic_reference)
    .def("length", &b2Length
        , py::arg("v")
        , py::return_value_policy::automatic_reference)
    .def("distance", &b2Distance
        , py::arg("a")
        , py::arg("b")
        , py::return_value_policy::automatic_reference)
    .def("normalize", &b2Normalize
        , py::arg("v")
        , py::return_value_policy::automatic_reference)
    .def("is_normalized", &b2IsNormalized
        , py::arg("a")
        , py::return_value_policy::automatic_reference)
    .def("get_length_and_normalize", [](float * length, b2Vec2 v)
        {
            auto ret = b2GetLengthAndNormalize(length, v);
            return std::make_tuple(ret, length);
        }
        , py::arg("length")
        , py::arg("v")
        , py::return_value_policy::automatic_reference)
    .def("normalize_rot", &b2NormalizeRot
        , py::arg("q")
        , py::return_value_policy::automatic_reference)
    .def("integrate_rotation", &b2IntegrateRotation
        , py::arg("q1")
        , py::arg("delta_angle")
        , py::return_value_policy::automatic_reference)
    .def("length_squared", &b2LengthSquared
        , py::arg("v")
        , py::return_value_policy::automatic_reference)
    .def("distance_squared", &b2DistanceSquared
        , py::arg("a")
        , py::arg("b")
        , py::return_value_policy::automatic_reference)
    .def("make_rot", &b2MakeRot
        , py::arg("radians")
        , py::return_value_policy::automatic_reference)
    .def("make_rot_from_unit_vector", &b2MakeRotFromUnitVector
        , py::arg("unit_vector")
        , py::return_value_policy::automatic_reference)
    .def("compute_rotation_between_unit_vectors", &b2ComputeRotationBetweenUnitVectors
        , py::arg("v1")
        , py::arg("v2")
        , py::return_value_policy::automatic_reference)
    .def("is_normalized_rot", &b2IsNormalizedRot
        , py::arg("q")
        , py::return_value_policy::automatic_reference)
    .def("invert_rot", &b2InvertRot
        , py::arg("a")
        , py::return_value_policy::automatic_reference)
    .def("n_lerp", &b2NLerp
        , py::arg("q1")
        , py::arg("q2")
        , py::arg("t")
        , py::return_value_policy::automatic_reference)
    .def("compute_angular_velocity", &b2ComputeAngularVelocity
        , py::arg("q1")
        , py::arg("q2")
        , py::arg("inv_h")
        , py::return_value_policy::automatic_reference)
    .def("rot_get_angle", &b2Rot_GetAngle
        , py::arg("q")
        , py::return_value_policy::automatic_reference)
    .def("rot_get_x_axis", &b2Rot_GetXAxis
        , py::arg("q")
        , py::return_value_policy::automatic_reference)
    .def("rot_get_y_axis", &b2Rot_GetYAxis
        , py::arg("q")
        , py::return_value_policy::automatic_reference)
    .def("mul_rot", &b2MulRot
        , py::arg("q")
        , py::arg("r")
        , py::return_value_policy::automatic_reference)
    .def("inv_mul_rot", &b2InvMulRot
        , py::arg("a")
        , py::arg("b")
        , py::return_value_policy::automatic_reference)
    .def("relative_angle", &b2RelativeAngle
        , py::arg("a")
        , py::arg("b")
        , py::return_value_policy::automatic_reference)
    .def("unwind_angle", &b2UnwindAngle
        , py::arg("radians")
        , py::return_value_policy::automatic_reference)
    .def("rotate_vector", &b2RotateVector
        , py::arg("q")
        , py::arg("v")
        , py::return_value_policy::automatic_reference)
    .def("inv_rotate_vector", &b2InvRotateVector
        , py::arg("q")
        , py::arg("v")
        , py::return_value_policy::automatic_reference)
    .def("transform_point", &b2TransformPoint
        , py::arg("t")
        , py::arg("p")
        , py::return_value_policy::automatic_reference)
    .def("inv_transform_point", &b2InvTransformPoint
        , py::arg("t")
        , py::arg("p")
        , py::return_value_policy::automatic_reference)
    .def("mul_transforms", &b2MulTransforms
        , py::arg("a")
        , py::arg("b")
        , py::return_value_policy::automatic_reference)
    .def("inv_mul_transforms", &b2InvMulTransforms
        , py::arg("a")
        , py::arg("b")
        , py::return_value_policy::automatic_reference)
    .def("mul_mv", &b2MulMV
        , py::arg("a")
        , py::arg("v")
        , py::return_value_policy::automatic_reference)
    .def("get_inverse22", &b2GetInverse22
        , py::arg("a")
        , py::return_value_policy::automatic_reference)
    .def("solve22", &b2Solve22
        , py::arg("a")
        , py::arg("b")
        , py::return_value_policy::automatic_reference)
    .def("aabb_contains", &b2AABB_Contains
        , py::arg("a")
        , py::arg("b")
        , py::return_value_policy::automatic_reference)
    .def("aabb_center", &b2AABB_Center
        , py::arg("a")
        , py::return_value_policy::automatic_reference)
    .def("aabb_extents", &b2AABB_Extents
        , py::arg("a")
        , py::return_value_policy::automatic_reference)
    .def("aabb_union", &b2AABB_Union
        , py::arg("a")
        , py::arg("b")
        , py::return_value_policy::automatic_reference)
    .def("aabb_overlaps", &b2AABB_Overlaps
        , py::arg("a")
        , py::arg("b")
        , py::return_value_policy::automatic_reference)
    .def("make_aabb", &b2MakeAABB
        , py::arg("points")
        , py::arg("count")
        , py::arg("radius")
        , py::return_value_policy::automatic_reference)
    .def("plane_separation", &b2PlaneSeparation
        , py::arg("plane")
        , py::arg("point")
        , py::return_value_policy::automatic_reference)
    .def("spring_damper", &b2SpringDamper
        , py::arg("hertz")
        , py::arg("damping_ratio")
        , py::arg("position")
        , py::arg("velocity")
        , py::arg("time_step")
        , py::return_value_policy::automatic_reference)
    .def("set_length_units_per_meter", &b2SetLengthUnitsPerMeter
        , py::arg("length_units")
        , py::return_value_policy::automatic_reference)
    .def("get_length_units_per_meter", &b2GetLengthUnitsPerMeter
        , py::return_value_policy::automatic_reference)
    ;


}