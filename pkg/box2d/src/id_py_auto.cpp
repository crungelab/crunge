#include <limits>
//#include <iostream>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>


#include <cxbind/cxbind.h>

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
        .def("draw", &World_Draw)
        .def("destroy", &b2DestroyWorld)
        .def("is_valid", &b2World_IsValid)
        .def("step", &b2World_Step)
        .def("get_body_events", &b2World_GetBodyEvents)
        .def("get_sensor_events", &b2World_GetSensorEvents)
        .def("get_contact_events", &b2World_GetContactEvents)
        .def("get_joint_events", &b2World_GetJointEvents)
        .def("overlap_aabb", &b2World_OverlapAABB)
        .def("overlap_shape", &b2World_OverlapShape)
        .def("cast_ray", &b2World_CastRay)
        .def("cast_ray_closest", &b2World_CastRayClosest)
        .def("cast_shape", &b2World_CastShape)
        .def("cast_mover", &b2World_CastMover)
        .def("collide_mover", &b2World_CollideMover)
        .def("enable_sleeping", &b2World_EnableSleeping)
        .def("is_sleeping_enabled", &b2World_IsSleepingEnabled)
        .def("enable_continuous", &b2World_EnableContinuous)
        .def("is_continuous_enabled", &b2World_IsContinuousEnabled)
        .def("set_restitution_threshold", &b2World_SetRestitutionThreshold)
        .def("get_restitution_threshold", &b2World_GetRestitutionThreshold)
        .def("set_hit_event_threshold", &b2World_SetHitEventThreshold)
        .def("get_hit_event_threshold", &b2World_GetHitEventThreshold)
        .def("set_custom_filter_callback", &b2World_SetCustomFilterCallback)
        .def("set_pre_solve_callback", &b2World_SetPreSolveCallback)
        .def("set_gravity", &b2World_SetGravity)
        .def("get_gravity", &b2World_GetGravity)
        .def("explode", &b2World_Explode)
        .def("set_contact_tuning", &b2World_SetContactTuning)
        .def("set_maximum_linear_speed", &b2World_SetMaximumLinearSpeed)
        .def("get_maximum_linear_speed", &b2World_GetMaximumLinearSpeed)
        .def("enable_warm_starting", &b2World_EnableWarmStarting)
        .def("is_warm_starting_enabled", &b2World_IsWarmStartingEnabled)
        .def("get_awake_body_count", &b2World_GetAwakeBodyCount)
        .def("get_profile", &b2World_GetProfile)
        .def("get_counters", &b2World_GetCounters)
        .def("set_user_data", &b2World_SetUserData)
        .def("get_user_data", &b2World_GetUserData)
        .def("set_friction_callback", &b2World_SetFrictionCallback)
        .def("set_restitution_callback", &b2World_SetRestitutionCallback)
        .def("dump_memory_stats", &b2World_DumpMemoryStats)
        .def("rebuild_static_tree", &b2World_RebuildStaticTree)
        .def("enable_speculative", &b2World_EnableSpeculative)
        .def("create_body", &b2CreateBody)
        .def("create_distance_joint", &b2CreateDistanceJoint)
        .def("create_motor_joint", &b2CreateMotorJoint)
        .def("create_filter_joint", &b2CreateFilterJoint)
        .def("create_prismatic_joint", &b2CreatePrismaticJoint)
        .def("create_revolute_joint", &b2CreateRevoluteJoint)
        .def("create_weld_joint", &b2CreateWeldJoint)
        .def("create_wheel_joint", &b2CreateWheelJoint)
    ;

    py::class_<b2BodyId> _Body(_box2d, "Body");
    registry.on(_box2d, "Body", _Body);
        _Body
        .def_readwrite("index1", &b2BodyId::index1)
        .def_readwrite("world0", &b2BodyId::world0)
        .def_readwrite("generation", &b2BodyId::generation)
        .def("is_valid", &b2Body_IsValid)
        .def("get_type", &b2Body_GetType)
        .def("set_type", &b2Body_SetType)
        .def("set_name", &b2Body_SetName)
        .def("get_name", &b2Body_GetName)
        .def("get_position", &b2Body_GetPosition)
        .def("get_rotation", &b2Body_GetRotation)
        .def("get_transform", &b2Body_GetTransform)
        .def("set_transform", &b2Body_SetTransform)
        .def("get_local_point", &b2Body_GetLocalPoint)
        .def("get_world_point", &b2Body_GetWorldPoint)
        .def("get_local_vector", &b2Body_GetLocalVector)
        .def("get_world_vector", &b2Body_GetWorldVector)
        .def("get_linear_velocity", &b2Body_GetLinearVelocity)
        .def("get_angular_velocity", &b2Body_GetAngularVelocity)
        .def("set_linear_velocity", &b2Body_SetLinearVelocity)
        .def("set_angular_velocity", &b2Body_SetAngularVelocity)
        .def("set_target_transform", &b2Body_SetTargetTransform)
        .def("get_local_point_velocity", &b2Body_GetLocalPointVelocity)
        .def("get_world_point_velocity", &b2Body_GetWorldPointVelocity)
        .def("apply_force", &b2Body_ApplyForce)
        .def("apply_force_to_center", &b2Body_ApplyForceToCenter)
        .def("apply_torque", &b2Body_ApplyTorque)
        .def("clear_forces", &b2Body_ClearForces)
        .def("apply_linear_impulse", &b2Body_ApplyLinearImpulse)
        .def("apply_linear_impulse_to_center", &b2Body_ApplyLinearImpulseToCenter)
        .def("apply_angular_impulse", &b2Body_ApplyAngularImpulse)
        .def("get_mass", &b2Body_GetMass)
        .def("get_rotational_inertia", &b2Body_GetRotationalInertia)
        .def("get_local_center_of_mass", &b2Body_GetLocalCenterOfMass)
        .def("get_world_center_of_mass", &b2Body_GetWorldCenterOfMass)
        .def("set_mass_data", &b2Body_SetMassData)
        .def("get_mass_data", &b2Body_GetMassData)
        .def("apply_mass_from_shapes", &b2Body_ApplyMassFromShapes)
        .def("set_linear_damping", &b2Body_SetLinearDamping)
        .def("get_linear_damping", &b2Body_GetLinearDamping)
        .def("set_angular_damping", &b2Body_SetAngularDamping)
        .def("get_angular_damping", &b2Body_GetAngularDamping)
        .def("set_gravity_scale", &b2Body_SetGravityScale)
        .def("get_gravity_scale", &b2Body_GetGravityScale)
        .def("is_awake", &b2Body_IsAwake)
        .def("set_awake", &b2Body_SetAwake)
        .def("wake_touching", &b2Body_WakeTouching)
        .def("enable_sleep", &b2Body_EnableSleep)
        .def("is_sleep_enabled", &b2Body_IsSleepEnabled)
        .def("set_sleep_threshold", &b2Body_SetSleepThreshold)
        .def("get_sleep_threshold", &b2Body_GetSleepThreshold)
        .def("is_enabled", &b2Body_IsEnabled)
        .def("disable", &b2Body_Disable)
        .def("enable", &b2Body_Enable)
        .def("set_motion_locks", &b2Body_SetMotionLocks)
        .def("get_motion_locks", &b2Body_GetMotionLocks)
        .def("set_bullet", &b2Body_SetBullet)
        .def("is_bullet", &b2Body_IsBullet)
        .def("enable_contact_events", &b2Body_EnableContactEvents)
        .def("enable_hit_events", &b2Body_EnableHitEvents)
        .def("get_world", &b2Body_GetWorld)
        .def("get_shape_count", &b2Body_GetShapeCount)
        .def("get_shapes", &b2Body_GetShapes)
        .def("get_joint_count", &b2Body_GetJointCount)
        .def("get_joints", &b2Body_GetJoints)
        .def("get_contact_capacity", &b2Body_GetContactCapacity)
        .def("get_contact_data", &b2Body_GetContactData)
        .def("compute_aabb", &b2Body_ComputeAABB)
        .def("create_circle_shape", &b2CreateCircleShape)
        .def("create_segment_shape", &b2CreateSegmentShape)
        .def("create_capsule_shape", &b2CreateCapsuleShape)
        .def("create_polygon_shape", &b2CreatePolygonShape)
        .def("create_chain", &b2CreateChain)
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
        .def("destroy", &b2DestroyShape)
        .def("is_valid", &b2Shape_IsValid)
        .def("get_type", &b2Shape_GetType)
        .def("get_body", &b2Shape_GetBody)
        .def("get_world", &b2Shape_GetWorld)
        .def("is_sensor", &b2Shape_IsSensor)
        .def("set_user_data", &b2Shape_SetUserData)
        .def("get_user_data", &b2Shape_GetUserData)
        .def("set_density", &b2Shape_SetDensity)
        .def("get_density", &b2Shape_GetDensity)
        .def("set_friction", &b2Shape_SetFriction)
        .def("get_friction", &b2Shape_GetFriction)
        .def("set_restitution", &b2Shape_SetRestitution)
        .def("get_restitution", &b2Shape_GetRestitution)
        .def("set_user_material", &b2Shape_SetUserMaterial)
        .def("get_user_material", &b2Shape_GetUserMaterial)
        .def("set_surface_material", &b2Shape_SetSurfaceMaterial)
        .def("get_surface_material", &b2Shape_GetSurfaceMaterial)
        .def("get_filter", &b2Shape_GetFilter)
        .def("set_filter", &b2Shape_SetFilter)
        .def("enable_sensor_events", &b2Shape_EnableSensorEvents)
        .def("are_sensor_events_enabled", &b2Shape_AreSensorEventsEnabled)
        .def("enable_contact_events", &b2Shape_EnableContactEvents)
        .def("are_contact_events_enabled", &b2Shape_AreContactEventsEnabled)
        .def("enable_pre_solve_events", &b2Shape_EnablePreSolveEvents)
        .def("are_pre_solve_events_enabled", &b2Shape_ArePreSolveEventsEnabled)
        .def("enable_hit_events", &b2Shape_EnableHitEvents)
        .def("are_hit_events_enabled", &b2Shape_AreHitEventsEnabled)
        .def("test_point", &b2Shape_TestPoint)
        .def("ray_cast", &b2Shape_RayCast)
        .def("get_circle", &b2Shape_GetCircle)
        .def("get_segment", &b2Shape_GetSegment)
        .def("get_chain_segment", &b2Shape_GetChainSegment)
        .def("get_capsule", &b2Shape_GetCapsule)
        .def("get_polygon", &b2Shape_GetPolygon)
        .def("set_circle", &b2Shape_SetCircle)
        .def("set_capsule", &b2Shape_SetCapsule)
        .def("set_segment", &b2Shape_SetSegment)
        .def("set_polygon", &b2Shape_SetPolygon)
        .def("get_parent_chain", &b2Shape_GetParentChain)
        .def("get_contact_capacity", &b2Shape_GetContactCapacity)
        .def("get_contact_data", &b2Shape_GetContactData)
        .def("get_sensor_capacity", &b2Shape_GetSensorCapacity)
        .def("get_sensor_data", &b2Shape_GetSensorData)
        .def("get_aabb", &b2Shape_GetAABB)
        .def("compute_mass_data", &b2Shape_ComputeMassData)
        .def("get_closest_point", &b2Shape_GetClosestPoint)
        .def("apply_wind", &b2Shape_ApplyWind)
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