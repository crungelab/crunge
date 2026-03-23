#include <limits>
//#include <iostream>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>


#include <cxbind/cxbind.h>
#include <cxbind/callback.h>

//#include <crunge/box2d/crunge-box2d.h>
//#include <crunge/box2d/conversions.h>

#include <box2d/id.h>
#include <box2d/box2d.h>

#include "box2d_internal.h"

namespace py = pybind11;

void init_id_py_auto(py::module &_box2d, Registry &registry) {
    py::class_<b2WorldId> _World(_box2d, "World");
    registry.on(_box2d, "World", _World);
        _World
        .def_readwrite("index1", &b2WorldId::index1)
        .def_readwrite("generation", &b2WorldId::generation)
        .def(py::init(&b2CreateWorld))
        .def("draw", &World_Draw
            , py::arg("arg")
            )
        .def("destroy", &b2DestroyWorld
            )
        .def("is_valid", &b2World_IsValid
            )
        .def("step", &b2World_Step
            , py::arg("time_step")
            , py::arg("sub_step_count")
            )
        .def("get_body_events", &b2World_GetBodyEvents
            )
        .def("get_sensor_events", &b2World_GetSensorEvents
            )
        .def("get_contact_events", &b2World_GetContactEvents
            )
        .def("get_joint_events", &b2World_GetJointEvents
            )
        .def("overlap_aabb", [](b2WorldId worldId, b2AABB aabb, b2QueryFilter filter, py::function fcn)
            {
                cxbind::thunk_state _context(fcn);
                auto context = &_context;
                auto _fcn = +[](b2ShapeId shapeId, void * context) -> bool {
                    auto& ts = *static_cast<cxbind::thunk_state*>(context);
                    // ... use ts, acquire GIL, call Python, etc ...
                    py::gil_scoped_acquire gil;
                    py::object result = ts.cb(shapeId);
                    return result.cast<_Bool>();
                };
                
                return b2World_OverlapAABB(worldId, aabb, filter, _fcn, context);
            }
            , py::arg("aabb")
            , py::arg("filter")
            , py::arg("fcn")
            )
        .def("overlap_shape", [](b2WorldId worldId, const b2ShapeProxy * proxy, b2QueryFilter filter, py::function fcn)
            {
                cxbind::thunk_state _context(fcn);
                auto context = &_context;
                auto _fcn = +[](b2ShapeId shapeId, void * context) -> bool {
                    auto& ts = *static_cast<cxbind::thunk_state*>(context);
                    // ... use ts, acquire GIL, call Python, etc ...
                    py::gil_scoped_acquire gil;
                    py::object result = ts.cb(shapeId);
                    return result.cast<_Bool>();
                };
                
                return b2World_OverlapShape(worldId, proxy, filter, _fcn, context);
            }
            , py::arg("proxy")
            , py::arg("filter")
            , py::arg("fcn")
            )
        .def("cast_ray", &b2World_CastRay
            , py::arg("origin")
            , py::arg("translation")
            , py::arg("filter")
            , py::arg("fcn")
            , py::arg("context")
            )
        .def("cast_ray_closest", &b2World_CastRayClosest
            , py::arg("origin")
            , py::arg("translation")
            , py::arg("filter")
            )
        .def("cast_shape", &b2World_CastShape
            , py::arg("proxy")
            , py::arg("translation")
            , py::arg("filter")
            , py::arg("fcn")
            , py::arg("context")
            )
        .def("cast_mover", &b2World_CastMover
            , py::arg("mover")
            , py::arg("translation")
            , py::arg("filter")
            )
        .def("collide_mover", &b2World_CollideMover
            , py::arg("mover")
            , py::arg("filter")
            , py::arg("fcn")
            , py::arg("context")
            )
        .def("enable_sleeping", &b2World_EnableSleeping
            , py::arg("flag")
            )
        .def("is_sleeping_enabled", &b2World_IsSleepingEnabled
            )
        .def("enable_continuous", &b2World_EnableContinuous
            , py::arg("flag")
            )
        .def("is_continuous_enabled", &b2World_IsContinuousEnabled
            )
        .def("set_restitution_threshold", &b2World_SetRestitutionThreshold
            , py::arg("value")
            )
        .def("get_restitution_threshold", &b2World_GetRestitutionThreshold
            )
        .def("set_hit_event_threshold", &b2World_SetHitEventThreshold
            , py::arg("value")
            )
        .def("get_hit_event_threshold", &b2World_GetHitEventThreshold
            )
        .def("set_custom_filter_callback", &b2World_SetCustomFilterCallback
            , py::arg("fcn")
            , py::arg("context")
            )
        .def("set_pre_solve_callback", &b2World_SetPreSolveCallback
            , py::arg("fcn")
            , py::arg("context")
            )
        .def("set_gravity", &b2World_SetGravity
            , py::arg("gravity")
            )
        .def("get_gravity", &b2World_GetGravity
            )
        .def("explode", &b2World_Explode
            , py::arg("explosion_def")
            )
        .def("set_contact_tuning", &b2World_SetContactTuning
            , py::arg("hertz")
            , py::arg("damping_ratio")
            , py::arg("push_speed")
            )
        .def("set_maximum_linear_speed", &b2World_SetMaximumLinearSpeed
            , py::arg("maximum_linear_speed")
            )
        .def("get_maximum_linear_speed", &b2World_GetMaximumLinearSpeed
            )
        .def("enable_warm_starting", &b2World_EnableWarmStarting
            , py::arg("flag")
            )
        .def("is_warm_starting_enabled", &b2World_IsWarmStartingEnabled
            )
        .def("get_awake_body_count", &b2World_GetAwakeBodyCount
            )
        .def("get_profile", &b2World_GetProfile
            )
        .def("get_counters", &b2World_GetCounters
            )
        .def("set_user_data", &b2World_SetUserData
            , py::arg("user_data")
            )
        .def("get_user_data", &b2World_GetUserData
            )
        .def("set_friction_callback", &b2World_SetFrictionCallback
            , py::arg("callback")
            )
        .def("set_restitution_callback", &b2World_SetRestitutionCallback
            , py::arg("callback")
            )
        .def("dump_memory_stats", &b2World_DumpMemoryStats
            )
        .def("rebuild_static_tree", &b2World_RebuildStaticTree
            )
        .def("enable_speculative", &b2World_EnableSpeculative
            , py::arg("flag")
            )
        .def("create_body", &b2CreateBody
            , py::arg("def")
            )
        .def("create_distance_joint", &b2CreateDistanceJoint
            , py::arg("def")
            )
        .def("create_motor_joint", &b2CreateMotorJoint
            , py::arg("def")
            )
        .def("create_filter_joint", &b2CreateFilterJoint
            , py::arg("def")
            )
        .def("create_prismatic_joint", &b2CreatePrismaticJoint
            , py::arg("def")
            )
        .def("create_revolute_joint", &b2CreateRevoluteJoint
            , py::arg("def")
            )
        .def("create_weld_joint", &b2CreateWeldJoint
            , py::arg("def")
            )
        .def("create_wheel_joint", &b2CreateWheelJoint
            , py::arg("def")
            )
    ;

    py::class_<b2BodyId> _Body(_box2d, "Body");
    registry.on(_box2d, "Body", _Body);
        _Body
        .def_readwrite("index1", &b2BodyId::index1)
        .def_readwrite("world0", &b2BodyId::world0)
        .def_readwrite("generation", &b2BodyId::generation)
        .def("is_valid", &b2Body_IsValid
            )
        .def("get_type", &b2Body_GetType
            )
        .def("set_type", &b2Body_SetType
            , py::arg("type")
            )
        .def("set_name", &b2Body_SetName
            , py::arg("name")
            )
        .def("get_name", &b2Body_GetName
            )
        .def("get_position", &b2Body_GetPosition
            )
        .def("get_rotation", &b2Body_GetRotation
            )
        .def("get_transform", &b2Body_GetTransform
            )
        .def("set_transform", &b2Body_SetTransform
            , py::arg("position")
            , py::arg("rotation")
            )
        .def("get_local_point", &b2Body_GetLocalPoint
            , py::arg("world_point")
            )
        .def("get_world_point", &b2Body_GetWorldPoint
            , py::arg("local_point")
            )
        .def("get_local_vector", &b2Body_GetLocalVector
            , py::arg("world_vector")
            )
        .def("get_world_vector", &b2Body_GetWorldVector
            , py::arg("local_vector")
            )
        .def("get_linear_velocity", &b2Body_GetLinearVelocity
            )
        .def("get_angular_velocity", &b2Body_GetAngularVelocity
            )
        .def("set_linear_velocity", &b2Body_SetLinearVelocity
            , py::arg("linear_velocity")
            )
        .def("set_angular_velocity", &b2Body_SetAngularVelocity
            , py::arg("angular_velocity")
            )
        .def("set_target_transform", &b2Body_SetTargetTransform
            , py::arg("target")
            , py::arg("time_step")
            , py::arg("wake")
            )
        .def("get_local_point_velocity", &b2Body_GetLocalPointVelocity
            , py::arg("local_point")
            )
        .def("get_world_point_velocity", &b2Body_GetWorldPointVelocity
            , py::arg("world_point")
            )
        .def("apply_force", &b2Body_ApplyForce
            , py::arg("force")
            , py::arg("point")
            , py::arg("wake")
            )
        .def("apply_force_to_center", &b2Body_ApplyForceToCenter
            , py::arg("force")
            , py::arg("wake")
            )
        .def("apply_torque", &b2Body_ApplyTorque
            , py::arg("torque")
            , py::arg("wake")
            )
        .def("clear_forces", &b2Body_ClearForces
            )
        .def("apply_linear_impulse", &b2Body_ApplyLinearImpulse
            , py::arg("impulse")
            , py::arg("point")
            , py::arg("wake")
            )
        .def("apply_linear_impulse_to_center", &b2Body_ApplyLinearImpulseToCenter
            , py::arg("impulse")
            , py::arg("wake")
            )
        .def("apply_angular_impulse", &b2Body_ApplyAngularImpulse
            , py::arg("impulse")
            , py::arg("wake")
            )
        .def("get_mass", &b2Body_GetMass
            )
        .def("get_rotational_inertia", &b2Body_GetRotationalInertia
            )
        .def("get_local_center_of_mass", &b2Body_GetLocalCenterOfMass
            )
        .def("get_world_center_of_mass", &b2Body_GetWorldCenterOfMass
            )
        .def("set_mass_data", &b2Body_SetMassData
            , py::arg("mass_data")
            )
        .def("get_mass_data", &b2Body_GetMassData
            )
        .def("apply_mass_from_shapes", &b2Body_ApplyMassFromShapes
            )
        .def("set_linear_damping", &b2Body_SetLinearDamping
            , py::arg("linear_damping")
            )
        .def("get_linear_damping", &b2Body_GetLinearDamping
            )
        .def("set_angular_damping", &b2Body_SetAngularDamping
            , py::arg("angular_damping")
            )
        .def("get_angular_damping", &b2Body_GetAngularDamping
            )
        .def("set_gravity_scale", &b2Body_SetGravityScale
            , py::arg("gravity_scale")
            )
        .def("get_gravity_scale", &b2Body_GetGravityScale
            )
        .def("is_awake", &b2Body_IsAwake
            )
        .def("set_awake", &b2Body_SetAwake
            , py::arg("awake")
            )
        .def("wake_touching", &b2Body_WakeTouching
            )
        .def("enable_sleep", &b2Body_EnableSleep
            , py::arg("enable_sleep")
            )
        .def("is_sleep_enabled", &b2Body_IsSleepEnabled
            )
        .def("set_sleep_threshold", &b2Body_SetSleepThreshold
            , py::arg("sleep_threshold")
            )
        .def("get_sleep_threshold", &b2Body_GetSleepThreshold
            )
        .def("is_enabled", &b2Body_IsEnabled
            )
        .def("disable", &b2Body_Disable
            )
        .def("enable", &b2Body_Enable
            )
        .def("set_motion_locks", &b2Body_SetMotionLocks
            , py::arg("locks")
            )
        .def("get_motion_locks", &b2Body_GetMotionLocks
            )
        .def("set_bullet", &b2Body_SetBullet
            , py::arg("flag")
            )
        .def("is_bullet", &b2Body_IsBullet
            )
        .def("enable_contact_events", &b2Body_EnableContactEvents
            , py::arg("flag")
            )
        .def("enable_hit_events", &b2Body_EnableHitEvents
            , py::arg("flag")
            )
        .def("get_world", &b2Body_GetWorld
            )
        .def("get_shape_count", &b2Body_GetShapeCount
            )
        .def("get_shapes", &b2Body_GetShapes
            , py::arg("shape_array")
            , py::arg("capacity")
            )
        .def("get_joint_count", &b2Body_GetJointCount
            )
        .def("get_joints", &b2Body_GetJoints
            , py::arg("joint_array")
            , py::arg("capacity")
            )
        .def("get_contact_capacity", &b2Body_GetContactCapacity
            )
        .def("get_contact_data", &b2Body_GetContactData
            , py::arg("contact_data")
            , py::arg("capacity")
            )
        .def("compute_aabb", &b2Body_ComputeAABB
            )
        .def("create_circle_shape", &b2CreateCircleShape
            , py::arg("def")
            , py::arg("circle")
            )
        .def("create_segment_shape", &b2CreateSegmentShape
            , py::arg("def")
            , py::arg("segment")
            )
        .def("create_capsule_shape", &b2CreateCapsuleShape
            , py::arg("def")
            , py::arg("capsule")
            )
        .def("create_polygon_shape", &b2CreatePolygonShape
            , py::arg("def")
            , py::arg("polygon")
            )
        .def("create_chain", &b2CreateChain
            , py::arg("def")
            )
        .def_property("user_data", &Body_GetUserData, &Body_SetUserData)
        .def_property_readonly("position", &b2Body_GetPosition)
        .def_property_readonly("rotation", &b2Body_GetRotation)
        .def_property_readonly("angle", &Body_GetAngle)
    ;

    py::class_<b2ShapeId> _Shape(_box2d, "Shape");
    registry.on(_box2d, "Shape", _Shape);
        _Shape
        .def_readwrite("index1", &b2ShapeId::index1)
        .def_readwrite("world0", &b2ShapeId::world0)
        .def_readwrite("generation", &b2ShapeId::generation)
        .def("destroy", &b2DestroyShape
            , py::arg("update_body_mass")
            )
        .def("is_valid", &b2Shape_IsValid
            )
        .def("get_type", &b2Shape_GetType
            )
        .def("get_body", &b2Shape_GetBody
            )
        .def("get_world", &b2Shape_GetWorld
            )
        .def("is_sensor", &b2Shape_IsSensor
            )
        .def("set_user_data", &b2Shape_SetUserData
            , py::arg("user_data")
            )
        .def("get_user_data", &b2Shape_GetUserData
            )
        .def("set_density", &b2Shape_SetDensity
            , py::arg("density")
            , py::arg("update_body_mass")
            )
        .def("get_density", &b2Shape_GetDensity
            )
        .def("set_friction", &b2Shape_SetFriction
            , py::arg("friction")
            )
        .def("get_friction", &b2Shape_GetFriction
            )
        .def("set_restitution", &b2Shape_SetRestitution
            , py::arg("restitution")
            )
        .def("get_restitution", &b2Shape_GetRestitution
            )
        .def("set_user_material", &b2Shape_SetUserMaterial
            , py::arg("material")
            )
        .def("get_user_material", &b2Shape_GetUserMaterial
            )
        .def("set_surface_material", &b2Shape_SetSurfaceMaterial
            , py::arg("surface_material")
            )
        .def("get_surface_material", &b2Shape_GetSurfaceMaterial
            )
        .def("get_filter", &b2Shape_GetFilter
            )
        .def("set_filter", &b2Shape_SetFilter
            , py::arg("filter")
            )
        .def("enable_sensor_events", &b2Shape_EnableSensorEvents
            , py::arg("flag")
            )
        .def("are_sensor_events_enabled", &b2Shape_AreSensorEventsEnabled
            )
        .def("enable_contact_events", &b2Shape_EnableContactEvents
            , py::arg("flag")
            )
        .def("are_contact_events_enabled", &b2Shape_AreContactEventsEnabled
            )
        .def("enable_pre_solve_events", &b2Shape_EnablePreSolveEvents
            , py::arg("flag")
            )
        .def("are_pre_solve_events_enabled", &b2Shape_ArePreSolveEventsEnabled
            )
        .def("enable_hit_events", &b2Shape_EnableHitEvents
            , py::arg("flag")
            )
        .def("are_hit_events_enabled", &b2Shape_AreHitEventsEnabled
            )
        .def("test_point", &b2Shape_TestPoint
            , py::arg("point")
            )
        .def("ray_cast", &b2Shape_RayCast
            , py::arg("input")
            )
        .def("get_circle", &b2Shape_GetCircle
            )
        .def("get_segment", &b2Shape_GetSegment
            )
        .def("get_chain_segment", &b2Shape_GetChainSegment
            )
        .def("get_capsule", &b2Shape_GetCapsule
            )
        .def("get_polygon", &b2Shape_GetPolygon
            )
        .def("set_circle", &b2Shape_SetCircle
            , py::arg("circle")
            )
        .def("set_capsule", &b2Shape_SetCapsule
            , py::arg("capsule")
            )
        .def("set_segment", &b2Shape_SetSegment
            , py::arg("segment")
            )
        .def("set_polygon", &b2Shape_SetPolygon
            , py::arg("polygon")
            )
        .def("get_parent_chain", &b2Shape_GetParentChain
            )
        .def("get_contact_capacity", &b2Shape_GetContactCapacity
            )
        .def("get_contact_data", &b2Shape_GetContactData
            , py::arg("contact_data")
            , py::arg("capacity")
            )
        .def("get_sensor_capacity", &b2Shape_GetSensorCapacity
            )
        .def("get_sensor_data", &b2Shape_GetSensorData
            , py::arg("visitor_ids")
            , py::arg("capacity")
            )
        .def("get_aabb", &b2Shape_GetAABB
            )
        .def("compute_mass_data", &b2Shape_ComputeMassData
            )
        .def("get_closest_point", &b2Shape_GetClosestPoint
            , py::arg("target")
            )
        .def("apply_wind", &b2Shape_ApplyWind
            , py::arg("wind")
            , py::arg("drag")
            , py::arg("lift")
            , py::arg("wake")
            )
        .def_property_readonly("body", &b2Shape_GetBody)
        .def_property("friction", &b2Shape_GetFriction, &b2Shape_SetFriction)
        .def_property("restitution", &b2Shape_GetRestitution, &b2Shape_SetRestitution)
    ;

    py::class_<b2ChainId> _ChainId(_box2d, "ChainId");
    registry.on(_box2d, "ChainId", _ChainId);
        _ChainId
        .def_readwrite("index1", &b2ChainId::index1)
        .def_readwrite("world0", &b2ChainId::world0)
        .def_readwrite("generation", &b2ChainId::generation)
    ;

    py::class_<b2JointId> _JointId(_box2d, "JointId");
    registry.on(_box2d, "JointId", _JointId);
        _JointId
        .def_readwrite("index1", &b2JointId::index1)
        .def_readwrite("world0", &b2JointId::world0)
        .def_readwrite("generation", &b2JointId::generation)
    ;

    py::class_<b2ContactId> _ContactId(_box2d, "ContactId");
    registry.on(_box2d, "ContactId", _ContactId);
        _ContactId
        .def_readwrite("index1", &b2ContactId::index1)
        .def_readwrite("world0", &b2ContactId::world0)
        .def_readwrite("padding", &b2ContactId::padding)
        .def_readwrite("generation", &b2ContactId::generation)
    ;


}