#include <limits>
//#include <iostream>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>


#include <cxbind/cxbind.h>
#include <cxbind/callback.h>

#include <crunge/box2d/crunge-box2d.h>
#include <crunge/box2d/conversions.h>

#include <box2d/box2d.h>

namespace py = pybind11;

void init_box2d_py_auto(py::module &_box2d, Registry &registry) {
    _box2d
    .def("create_world", &b2CreateWorld
        , py::arg("def")
        )
    .def("destroy_world", &b2DestroyWorld
        , py::arg("world_id")
        )
    .def("world_is_valid", &b2World_IsValid
        , py::arg("id")
        )
    .def("world_step", &b2World_Step
        , py::arg("world_id")
        , py::arg("time_step")
        , py::arg("sub_step_count")
        )
    .def("world_get_bounds", &b2World_GetBounds
        , py::arg("world_id")
        )
    .def("world_get_body_events", &b2World_GetBodyEvents
        , py::arg("world_id")
        )
    .def("world_get_sensor_events", &b2World_GetSensorEvents
        , py::arg("world_id")
        )
    .def("world_get_contact_events", &b2World_GetContactEvents
        , py::arg("world_id")
        )
    .def("world_get_joint_events", &b2World_GetJointEvents
        , py::arg("world_id")
        )
    .def("world_overlap_aabb", [](b2WorldId worldId, b2Pos origin, b2AABB aabb, b2QueryFilter filter, py::function fcn)
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
            
            return b2World_OverlapAABB(worldId, origin, aabb, filter, _fcn, context);
        }
        , py::arg("world_id")
        , py::arg("origin")
        , py::arg("aabb")
        , py::arg("filter")
        , py::arg("fcn")
        )
    .def("world_overlap_shape", [](b2WorldId worldId, b2Pos origin, const b2ShapeProxy * proxy, b2QueryFilter filter, py::function fcn)
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
            
            return b2World_OverlapShape(worldId, origin, proxy, filter, _fcn, context);
        }
        , py::arg("world_id")
        , py::arg("origin")
        , py::arg("proxy")
        , py::arg("filter")
        , py::arg("fcn")
        )
    .def("world_cast_ray", &b2World_CastRay
        , py::arg("world_id")
        , py::arg("origin")
        , py::arg("translation")
        , py::arg("filter")
        , py::arg("fcn")
        , py::arg("context")
        )
    .def("world_cast_ray_closest", &b2World_CastRayClosest
        , py::arg("world_id")
        , py::arg("origin")
        , py::arg("translation")
        , py::arg("filter")
        )
    .def("world_cast_shape", &b2World_CastShape
        , py::arg("world_id")
        , py::arg("origin")
        , py::arg("proxy")
        , py::arg("translation")
        , py::arg("filter")
        , py::arg("fcn")
        , py::arg("context")
        )
    .def("world_cast_mover", &b2World_CastMover
        , py::arg("world_id")
        , py::arg("origin")
        , py::arg("mover")
        , py::arg("translation")
        , py::arg("filter")
        )
    .def("world_collide_mover", &b2World_CollideMover
        , py::arg("world_id")
        , py::arg("origin")
        , py::arg("mover")
        , py::arg("filter")
        , py::arg("fcn")
        , py::arg("context")
        )
    .def("world_enable_sleeping", &b2World_EnableSleeping
        , py::arg("world_id")
        , py::arg("flag")
        )
    .def("world_is_sleeping_enabled", &b2World_IsSleepingEnabled
        , py::arg("world_id")
        )
    .def("world_enable_continuous", &b2World_EnableContinuous
        , py::arg("world_id")
        , py::arg("flag")
        )
    .def("world_is_continuous_enabled", &b2World_IsContinuousEnabled
        , py::arg("world_id")
        )
    .def("world_set_restitution_threshold", &b2World_SetRestitutionThreshold
        , py::arg("world_id")
        , py::arg("value")
        )
    .def("world_get_restitution_threshold", &b2World_GetRestitutionThreshold
        , py::arg("world_id")
        )
    .def("world_set_hit_event_threshold", &b2World_SetHitEventThreshold
        , py::arg("world_id")
        , py::arg("value")
        )
    .def("world_get_hit_event_threshold", &b2World_GetHitEventThreshold
        , py::arg("world_id")
        )
    .def("world_set_custom_filter_callback", &b2World_SetCustomFilterCallback
        , py::arg("world_id")
        , py::arg("fcn")
        , py::arg("context")
        )
    .def("world_set_pre_solve_callback", &b2World_SetPreSolveCallback
        , py::arg("world_id")
        , py::arg("pre_solve_fcn")
        , py::arg("pre_continuous_fcn")
        , py::arg("context")
        )
    .def("world_set_gravity", &b2World_SetGravity
        , py::arg("world_id")
        , py::arg("gravity")
        )
    .def("world_get_gravity", &b2World_GetGravity
        , py::arg("world_id")
        )
    .def("world_explode", &b2World_Explode
        , py::arg("world_id")
        , py::arg("explosion_def")
        )
    .def("world_set_contact_tuning", &b2World_SetContactTuning
        , py::arg("world_id")
        , py::arg("hertz")
        , py::arg("damping_ratio")
        , py::arg("push_speed")
        )
    .def("world_set_contact_recycle_distance", &b2World_SetContactRecycleDistance
        , py::arg("world_id")
        , py::arg("recycle_distance")
        )
    .def("world_get_contact_recycle_distance", &b2World_GetContactRecycleDistance
        , py::arg("world_id")
        )
    .def("world_set_maximum_linear_speed", &b2World_SetMaximumLinearSpeed
        , py::arg("world_id")
        , py::arg("maximum_linear_speed")
        )
    .def("world_get_maximum_linear_speed", &b2World_GetMaximumLinearSpeed
        , py::arg("world_id")
        )
    .def("world_enable_warm_starting", &b2World_EnableWarmStarting
        , py::arg("world_id")
        , py::arg("flag")
        )
    .def("world_is_warm_starting_enabled", &b2World_IsWarmStartingEnabled
        , py::arg("world_id")
        )
    .def("world_get_awake_body_count", &b2World_GetAwakeBodyCount
        , py::arg("world_id")
        )
    .def("world_get_profile", &b2World_GetProfile
        , py::arg("world_id")
        )
    .def("world_get_counters", &b2World_GetCounters
        , py::arg("world_id")
        )
    .def("world_get_max_capacity", &b2World_GetMaxCapacity
        , py::arg("world_id")
        )
    .def("world_set_user_data", &b2World_SetUserData
        , py::arg("world_id")
        , py::arg("user_data")
        )
    .def("world_get_user_data", &b2World_GetUserData
        , py::arg("world_id")
        , py::return_value_policy::reference)
    .def("world_set_friction_callback", &b2World_SetFrictionCallback
        , py::arg("world_id")
        , py::arg("callback")
        )
    .def("world_set_restitution_callback", &b2World_SetRestitutionCallback
        , py::arg("world_id")
        , py::arg("callback")
        )
    .def("world_set_worker_count", &b2World_SetWorkerCount
        , py::arg("world_id")
        , py::arg("count")
        )
    .def("world_get_worker_count", &b2World_GetWorkerCount
        , py::arg("world_id")
        )
    .def("world_dump_memory_stats", &b2World_DumpMemoryStats
        , py::arg("world_id")
        )
    .def("world_rebuild_static_tree", &b2World_RebuildStaticTree
        , py::arg("world_id")
        )
    .def("world_enable_speculative", &b2World_EnableSpeculative
        , py::arg("world_id")
        , py::arg("flag")
        )
    .def("world_get_state_hash", &b2World_GetStateHash
        , py::arg("world_id")
        )
    .def("create_recording", [](int byteCapacity)
        {
            return py::capsule(b2CreateRecording(byteCapacity), "b2Recording");
        }
        , py::arg("byte_capacity")
        )
    .def("destroy_recording", [](py::capsule recording)
        {
            return b2DestroyRecording(static_cast<b2Recording *>(recording.get_pointer()));
        }
        , py::arg("recording")
        )
    .def("recording_get_data", [](py::capsule recording)
        {
            return b2Recording_GetData(static_cast<const b2Recording *>(recording.get_pointer()));
        }
        , py::arg("recording")
        , py::return_value_policy::reference)
    .def("recording_get_size", [](py::capsule recording)
        {
            return b2Recording_GetSize(static_cast<const b2Recording *>(recording.get_pointer()));
        }
        , py::arg("recording")
        )
    .def("world_start_recording", [](b2WorldId worldId, py::capsule recording)
        {
            return b2World_StartRecording(worldId, static_cast<b2Recording *>(recording.get_pointer()));
        }
        , py::arg("world_id")
        , py::arg("recording")
        )
    .def("world_stop_recording", &b2World_StopRecording
        , py::arg("world_id")
        )
    .def("save_recording_to_file", [](py::capsule recording, const char * path)
        {
            return b2SaveRecordingToFile(static_cast<const b2Recording *>(recording.get_pointer()), path);
        }
        , py::arg("recording")
        , py::arg("path")
        )
    .def("load_recording_from_file", [](const char * path)
        {
            return py::capsule(b2LoadRecordingFromFile(path), "b2Recording");
        }
        , py::arg("path")
        )
    .def("world_snapshot", &b2World_Snapshot
        , py::arg("world_id")
        , py::arg("image")
        , py::arg("capacity")
        )
    .def("world_restore", &b2World_Restore
        , py::arg("world_id")
        , py::arg("image")
        , py::arg("size")
        )
    .def("create_world_from_snapshot", &b2CreateWorldFromSnapshot
        , py::arg("image")
        , py::arg("size")
        , py::arg("worker_count")
        )
    .def("create_body", &b2CreateBody
        , py::arg("world_id")
        , py::arg("def")
        )
    .def("body_is_valid", &b2Body_IsValid
        , py::arg("id")
        )
    .def("body_get_type", &b2Body_GetType
        , py::arg("body_id")
        )
    .def("body_set_type", &b2Body_SetType
        , py::arg("body_id")
        , py::arg("type")
        )
    .def("body_set_name", &b2Body_SetName
        , py::arg("body_id")
        , py::arg("name")
        )
    .def("body_get_name", &b2Body_GetName
        , py::arg("body_id")
        , py::return_value_policy::reference)
    .def("body_get_position", &b2Body_GetPosition
        , py::arg("body_id")
        )
    .def("body_get_rotation", &b2Body_GetRotation
        , py::arg("body_id")
        )
    .def("body_get_transform", &b2Body_GetTransform
        , py::arg("body_id")
        )
    .def("body_set_transform", &b2Body_SetTransform
        , py::arg("body_id")
        , py::arg("position")
        , py::arg("rotation")
        )
    .def("body_get_local_point", &b2Body_GetLocalPoint
        , py::arg("body_id")
        , py::arg("world_point")
        )
    .def("body_get_world_point", &b2Body_GetWorldPoint
        , py::arg("body_id")
        , py::arg("local_point")
        )
    .def("body_get_local_vector", &b2Body_GetLocalVector
        , py::arg("body_id")
        , py::arg("world_vector")
        )
    .def("body_get_world_vector", &b2Body_GetWorldVector
        , py::arg("body_id")
        , py::arg("local_vector")
        )
    .def("body_get_linear_velocity", &b2Body_GetLinearVelocity
        , py::arg("body_id")
        )
    .def("body_get_angular_velocity", &b2Body_GetAngularVelocity
        , py::arg("body_id")
        )
    .def("body_set_linear_velocity", &b2Body_SetLinearVelocity
        , py::arg("body_id")
        , py::arg("linear_velocity")
        )
    .def("body_set_angular_velocity", &b2Body_SetAngularVelocity
        , py::arg("body_id")
        , py::arg("angular_velocity")
        )
    .def("body_set_target_transform", &b2Body_SetTargetTransform
        , py::arg("body_id")
        , py::arg("target")
        , py::arg("time_step")
        , py::arg("wake")
        )
    .def("body_get_local_point_velocity", &b2Body_GetLocalPointVelocity
        , py::arg("body_id")
        , py::arg("local_point")
        )
    .def("body_get_world_point_velocity", &b2Body_GetWorldPointVelocity
        , py::arg("body_id")
        , py::arg("world_point")
        )
    .def("body_apply_force", &b2Body_ApplyForce
        , py::arg("body_id")
        , py::arg("force")
        , py::arg("point")
        , py::arg("wake")
        )
    .def("body_apply_force_to_center", &b2Body_ApplyForceToCenter
        , py::arg("body_id")
        , py::arg("force")
        , py::arg("wake")
        )
    .def("body_apply_torque", &b2Body_ApplyTorque
        , py::arg("body_id")
        , py::arg("torque")
        , py::arg("wake")
        )
    .def("body_clear_forces", &b2Body_ClearForces
        , py::arg("body_id")
        )
    .def("body_apply_linear_impulse", &b2Body_ApplyLinearImpulse
        , py::arg("body_id")
        , py::arg("impulse")
        , py::arg("point")
        , py::arg("wake")
        )
    .def("body_apply_linear_impulse_to_center", &b2Body_ApplyLinearImpulseToCenter
        , py::arg("body_id")
        , py::arg("impulse")
        , py::arg("wake")
        )
    .def("body_apply_angular_impulse", &b2Body_ApplyAngularImpulse
        , py::arg("body_id")
        , py::arg("impulse")
        , py::arg("wake")
        )
    .def("body_get_mass", &b2Body_GetMass
        , py::arg("body_id")
        )
    .def("body_get_rotational_inertia", &b2Body_GetRotationalInertia
        , py::arg("body_id")
        )
    .def("body_get_local_center", &b2Body_GetLocalCenter
        , py::arg("body_id")
        )
    .def("body_get_world_center", &b2Body_GetWorldCenter
        , py::arg("body_id")
        )
    .def("body_set_mass_data", &b2Body_SetMassData
        , py::arg("body_id")
        , py::arg("mass_data")
        )
    .def("body_get_mass_data", &b2Body_GetMassData
        , py::arg("body_id")
        )
    .def("body_apply_mass_from_shapes", &b2Body_ApplyMassFromShapes
        , py::arg("body_id")
        )
    .def("body_set_linear_damping", &b2Body_SetLinearDamping
        , py::arg("body_id")
        , py::arg("linear_damping")
        )
    .def("body_get_linear_damping", &b2Body_GetLinearDamping
        , py::arg("body_id")
        )
    .def("body_set_angular_damping", &b2Body_SetAngularDamping
        , py::arg("body_id")
        , py::arg("angular_damping")
        )
    .def("body_get_angular_damping", &b2Body_GetAngularDamping
        , py::arg("body_id")
        )
    .def("body_set_gravity_scale", &b2Body_SetGravityScale
        , py::arg("body_id")
        , py::arg("gravity_scale")
        )
    .def("body_get_gravity_scale", &b2Body_GetGravityScale
        , py::arg("body_id")
        )
    .def("body_is_awake", &b2Body_IsAwake
        , py::arg("body_id")
        )
    .def("body_set_awake", &b2Body_SetAwake
        , py::arg("body_id")
        , py::arg("awake")
        )
    .def("body_wake_touching", &b2Body_WakeTouching
        , py::arg("body_id")
        )
    .def("body_enable_sleep", &b2Body_EnableSleep
        , py::arg("body_id")
        , py::arg("enable_sleep")
        )
    .def("body_is_sleep_enabled", &b2Body_IsSleepEnabled
        , py::arg("body_id")
        )
    .def("body_set_sleep_threshold", &b2Body_SetSleepThreshold
        , py::arg("body_id")
        , py::arg("sleep_threshold")
        )
    .def("body_get_sleep_threshold", &b2Body_GetSleepThreshold
        , py::arg("body_id")
        )
    .def("body_set_safety_factor", &b2Body_SetSafetyFactor
        , py::arg("body_id")
        , py::arg("safety_factor")
        )
    .def("body_get_safety_factor", &b2Body_GetSafetyFactor
        , py::arg("body_id")
        )
    .def("body_is_enabled", &b2Body_IsEnabled
        , py::arg("body_id")
        )
    .def("body_disable", &b2Body_Disable
        , py::arg("body_id")
        )
    .def("body_enable", &b2Body_Enable
        , py::arg("body_id")
        )
    .def("body_set_motion_locks", &b2Body_SetMotionLocks
        , py::arg("body_id")
        , py::arg("locks")
        )
    .def("body_get_motion_locks", &b2Body_GetMotionLocks
        , py::arg("body_id")
        )
    .def("body_set_bullet", &b2Body_SetBullet
        , py::arg("body_id")
        , py::arg("flag")
        )
    .def("body_is_bullet", &b2Body_IsBullet
        , py::arg("body_id")
        )
    .def("body_enable_contact_recycling", &b2Body_EnableContactRecycling
        , py::arg("body_id")
        , py::arg("flag")
        )
    .def("body_is_contact_recycling_enabled", &b2Body_IsContactRecyclingEnabled
        , py::arg("body_id")
        )
    .def("body_enable_contact_events", &b2Body_EnableContactEvents
        , py::arg("body_id")
        , py::arg("flag")
        )
    .def("body_enable_hit_events", &b2Body_EnableHitEvents
        , py::arg("body_id")
        , py::arg("flag")
        )
    .def("body_get_world", &b2Body_GetWorld
        , py::arg("body_id")
        )
    .def("body_get_shape_count", &b2Body_GetShapeCount
        , py::arg("body_id")
        )
    .def("body_get_shapes", &b2Body_GetShapes
        , py::arg("body_id")
        , py::arg("shape_array")
        , py::arg("capacity")
        )
    .def("body_get_joint_count", &b2Body_GetJointCount
        , py::arg("body_id")
        )
    .def("body_get_joints", &b2Body_GetJoints
        , py::arg("body_id")
        , py::arg("joint_array")
        , py::arg("capacity")
        )
    .def("body_get_contact_capacity", &b2Body_GetContactCapacity
        , py::arg("body_id")
        )
    .def("body_get_contact_data", &b2Body_GetContactData
        , py::arg("body_id")
        , py::arg("contact_data")
        , py::arg("capacity")
        )
    .def("body_compute_aabb", &b2Body_ComputeAABB
        , py::arg("body_id")
        )
    .def("create_circle_shape", &b2CreateCircleShape
        , py::arg("body_id")
        , py::arg("def")
        , py::arg("circle")
        )
    .def("create_segment_shape", &b2CreateSegmentShape
        , py::arg("body_id")
        , py::arg("def")
        , py::arg("segment")
        )
    .def("create_chain_segment_shape", &b2CreateChainSegmentShape
        , py::arg("body_id")
        , py::arg("def")
        , py::arg("chain_segment")
        )
    .def("create_capsule_shape", &b2CreateCapsuleShape
        , py::arg("body_id")
        , py::arg("def")
        , py::arg("capsule")
        )
    .def("create_polygon_shape", &b2CreatePolygonShape
        , py::arg("body_id")
        , py::arg("def")
        , py::arg("polygon")
        )
    .def("shape_is_valid", &b2Shape_IsValid
        , py::arg("id")
        )
    .def("shape_get_type", &b2Shape_GetType
        , py::arg("shape_id")
        )
    .def("shape_get_body", &b2Shape_GetBody
        , py::arg("shape_id")
        )
    .def("shape_get_world", &b2Shape_GetWorld
        , py::arg("shape_id")
        )
    .def("shape_is_sensor", &b2Shape_IsSensor
        , py::arg("shape_id")
        )
    .def("shape_set_density", &b2Shape_SetDensity
        , py::arg("shape_id")
        , py::arg("density")
        , py::arg("update_body_mass")
        )
    .def("shape_get_density", &b2Shape_GetDensity
        , py::arg("shape_id")
        )
    .def("shape_set_friction", &b2Shape_SetFriction
        , py::arg("shape_id")
        , py::arg("friction")
        )
    .def("shape_get_friction", &b2Shape_GetFriction
        , py::arg("shape_id")
        )
    .def("shape_set_restitution", &b2Shape_SetRestitution
        , py::arg("shape_id")
        , py::arg("restitution")
        )
    .def("shape_get_restitution", &b2Shape_GetRestitution
        , py::arg("shape_id")
        )
    .def("shape_set_user_material", &b2Shape_SetUserMaterial
        , py::arg("shape_id")
        , py::arg("material")
        )
    .def("shape_get_user_material", &b2Shape_GetUserMaterial
        , py::arg("shape_id")
        )
    .def("shape_set_surface_material", &b2Shape_SetSurfaceMaterial
        , py::arg("shape_id")
        , py::arg("surface_material")
        )
    .def("shape_get_surface_material", &b2Shape_GetSurfaceMaterial
        , py::arg("shape_id")
        )
    .def("shape_get_filter", &b2Shape_GetFilter
        , py::arg("shape_id")
        )
    .def("shape_set_filter", &b2Shape_SetFilter
        , py::arg("shape_id")
        , py::arg("filter")
        )
    .def("shape_enable_sensor_events", &b2Shape_EnableSensorEvents
        , py::arg("shape_id")
        , py::arg("flag")
        )
    .def("shape_are_sensor_events_enabled", &b2Shape_AreSensorEventsEnabled
        , py::arg("shape_id")
        )
    .def("shape_enable_contact_events", &b2Shape_EnableContactEvents
        , py::arg("shape_id")
        , py::arg("flag")
        )
    .def("shape_are_contact_events_enabled", &b2Shape_AreContactEventsEnabled
        , py::arg("shape_id")
        )
    .def("shape_enable_pre_solve_events", &b2Shape_EnablePreSolveEvents
        , py::arg("shape_id")
        , py::arg("flag")
        )
    .def("shape_are_pre_solve_events_enabled", &b2Shape_ArePreSolveEventsEnabled
        , py::arg("shape_id")
        )
    .def("shape_enable_hit_events", &b2Shape_EnableHitEvents
        , py::arg("shape_id")
        , py::arg("flag")
        )
    .def("shape_are_hit_events_enabled", &b2Shape_AreHitEventsEnabled
        , py::arg("shape_id")
        )
    .def("shape_test_point", &b2Shape_TestPoint
        , py::arg("shape_id")
        , py::arg("point")
        )
    .def("shape_ray_cast", &b2Shape_RayCast
        , py::arg("shape_id")
        , py::arg("origin")
        , py::arg("translation")
        )
    .def("shape_get_circle", &b2Shape_GetCircle
        , py::arg("shape_id")
        )
    .def("shape_get_segment", &b2Shape_GetSegment
        , py::arg("shape_id")
        )
    .def("shape_get_chain_segment", &b2Shape_GetChainSegment
        , py::arg("shape_id")
        )
    .def("shape_get_capsule", &b2Shape_GetCapsule
        , py::arg("shape_id")
        )
    .def("shape_get_polygon", &b2Shape_GetPolygon
        , py::arg("shape_id")
        )
    .def("shape_set_circle", &b2Shape_SetCircle
        , py::arg("shape_id")
        , py::arg("circle")
        )
    .def("shape_set_capsule", &b2Shape_SetCapsule
        , py::arg("shape_id")
        , py::arg("capsule")
        )
    .def("shape_set_segment", &b2Shape_SetSegment
        , py::arg("shape_id")
        , py::arg("segment")
        )
    .def("shape_set_polygon", &b2Shape_SetPolygon
        , py::arg("shape_id")
        , py::arg("polygon")
        )
    .def("shape_set_chain_segment", &b2Shape_SetChainSegment
        , py::arg("shape_id")
        , py::arg("chain_segment")
        )
    .def("shape_get_parent_chain", &b2Shape_GetParentChain
        , py::arg("shape_id")
        )
    .def("shape_get_contact_capacity", &b2Shape_GetContactCapacity
        , py::arg("shape_id")
        )
    .def("shape_get_contact_data", &b2Shape_GetContactData
        , py::arg("shape_id")
        , py::arg("contact_data")
        , py::arg("capacity")
        )
    .def("shape_get_sensor_capacity", &b2Shape_GetSensorCapacity
        , py::arg("shape_id")
        )
    .def("shape_get_sensor_data", &b2Shape_GetSensorData
        , py::arg("shape_id")
        , py::arg("visitor_ids")
        , py::arg("capacity")
        )
    .def("shape_get_aabb", &b2Shape_GetAABB
        , py::arg("shape_id")
        )
    .def("shape_compute_mass_data", &b2Shape_ComputeMassData
        , py::arg("shape_id")
        )
    .def("shape_get_closest_point", &b2Shape_GetClosestPoint
        , py::arg("shape_id")
        , py::arg("target")
        )
    .def("shape_apply_wind", &b2Shape_ApplyWind
        , py::arg("shape_id")
        , py::arg("wind")
        , py::arg("drag")
        , py::arg("lift")
        , py::arg("wake")
        )
    .def("create_chain", &b2CreateChain
        , py::arg("body_id")
        , py::arg("def")
        )
    .def("destroy_chain", &b2DestroyChain
        , py::arg("chain_id")
        )
    .def("chain_get_world", &b2Chain_GetWorld
        , py::arg("chain_id")
        )
    .def("chain_get_segment_count", &b2Chain_GetSegmentCount
        , py::arg("chain_id")
        )
    .def("chain_get_segments", &b2Chain_GetSegments
        , py::arg("chain_id")
        , py::arg("segment_array")
        , py::arg("capacity")
        )
    .def("chain_get_surface_material_count", &b2Chain_GetSurfaceMaterialCount
        , py::arg("chain_id")
        )
    .def("chain_set_surface_material", &b2Chain_SetSurfaceMaterial
        , py::arg("chain_id")
        , py::arg("material")
        , py::arg("material_index")
        )
    .def("chain_get_surface_material", &b2Chain_GetSurfaceMaterial
        , py::arg("chain_id")
        , py::arg("material_index")
        )
    .def("chain_is_valid", &b2Chain_IsValid
        , py::arg("id")
        )
    .def("destroy_joint", &b2DestroyJoint
        , py::arg("joint_id")
        )
    .def("joint_is_valid", &b2Joint_IsValid
        , py::arg("id")
        )
    .def("joint_get_type", &b2Joint_GetType
        , py::arg("joint_id")
        )
    .def("joint_get_body_a", &b2Joint_GetBodyA
        , py::arg("joint_id")
        )
    .def("joint_get_body_b", &b2Joint_GetBodyB
        , py::arg("joint_id")
        )
    .def("joint_get_world", &b2Joint_GetWorld
        , py::arg("joint_id")
        )
    .def("joint_set_local_frame_a", &b2Joint_SetLocalFrameA
        , py::arg("joint_id")
        , py::arg("local_frame")
        )
    .def("joint_get_local_frame_a", &b2Joint_GetLocalFrameA
        , py::arg("joint_id")
        )
    .def("joint_set_local_frame_b", &b2Joint_SetLocalFrameB
        , py::arg("joint_id")
        , py::arg("local_frame")
        )
    .def("joint_get_local_frame_b", &b2Joint_GetLocalFrameB
        , py::arg("joint_id")
        )
    .def("joint_set_collide_connected", &b2Joint_SetCollideConnected
        , py::arg("joint_id")
        , py::arg("should_collide")
        )
    .def("joint_get_collide_connected", &b2Joint_GetCollideConnected
        , py::arg("joint_id")
        )
    .def("joint_set_user_data", &b2Joint_SetUserData
        , py::arg("joint_id")
        , py::arg("user_data")
        )
    .def("joint_get_user_data", &b2Joint_GetUserData
        , py::arg("joint_id")
        , py::return_value_policy::reference)
    .def("joint_wake_bodies", &b2Joint_WakeBodies
        , py::arg("joint_id")
        )
    .def("joint_get_constraint_force", &b2Joint_GetConstraintForce
        , py::arg("joint_id")
        )
    .def("joint_get_constraint_torque", &b2Joint_GetConstraintTorque
        , py::arg("joint_id")
        )
    .def("joint_get_linear_separation", &b2Joint_GetLinearSeparation
        , py::arg("joint_id")
        )
    .def("joint_get_angular_separation", &b2Joint_GetAngularSeparation
        , py::arg("joint_id")
        )
    .def("joint_set_constraint_tuning", &b2Joint_SetConstraintTuning
        , py::arg("joint_id")
        , py::arg("hertz")
        , py::arg("damping_ratio")
        )
    .def("joint_get_constraint_tuning", [](b2JointId jointId, float * hertz, float * dampingRatio)
        {
            b2Joint_GetConstraintTuning(jointId, hertz, dampingRatio);
            return std::make_tuple(hertz, dampingRatio);
        }
        , py::arg("joint_id")
        , py::arg("hertz")
        , py::arg("damping_ratio")
        )
    .def("joint_set_force_threshold", &b2Joint_SetForceThreshold
        , py::arg("joint_id")
        , py::arg("threshold")
        )
    .def("joint_get_force_threshold", &b2Joint_GetForceThreshold
        , py::arg("joint_id")
        )
    .def("joint_set_torque_threshold", &b2Joint_SetTorqueThreshold
        , py::arg("joint_id")
        , py::arg("threshold")
        )
    .def("joint_get_torque_threshold", &b2Joint_GetTorqueThreshold
        , py::arg("joint_id")
        )
    .def("create_distance_joint", &b2CreateDistanceJoint
        , py::arg("world_id")
        , py::arg("def")
        )
    .def("distance_joint_set_length", &b2DistanceJoint_SetLength
        , py::arg("joint_id")
        , py::arg("length")
        )
    .def("distance_joint_get_length", &b2DistanceJoint_GetLength
        , py::arg("joint_id")
        )
    .def("distance_joint_enable_spring", &b2DistanceJoint_EnableSpring
        , py::arg("joint_id")
        , py::arg("enable_spring")
        )
    .def("distance_joint_is_spring_enabled", &b2DistanceJoint_IsSpringEnabled
        , py::arg("joint_id")
        )
    .def("distance_joint_set_spring_force_range", &b2DistanceJoint_SetSpringForceRange
        , py::arg("joint_id")
        , py::arg("lower_force")
        , py::arg("upper_force")
        )
    .def("distance_joint_get_spring_force_range", [](b2JointId jointId, float * lowerForce, float * upperForce)
        {
            b2DistanceJoint_GetSpringForceRange(jointId, lowerForce, upperForce);
            return std::make_tuple(lowerForce, upperForce);
        }
        , py::arg("joint_id")
        , py::arg("lower_force")
        , py::arg("upper_force")
        )
    .def("distance_joint_set_spring_hertz", &b2DistanceJoint_SetSpringHertz
        , py::arg("joint_id")
        , py::arg("hertz")
        )
    .def("distance_joint_set_spring_damping_ratio", &b2DistanceJoint_SetSpringDampingRatio
        , py::arg("joint_id")
        , py::arg("damping_ratio")
        )
    .def("distance_joint_get_spring_hertz", &b2DistanceJoint_GetSpringHertz
        , py::arg("joint_id")
        )
    .def("distance_joint_get_spring_damping_ratio", &b2DistanceJoint_GetSpringDampingRatio
        , py::arg("joint_id")
        )
    .def("distance_joint_enable_limit", &b2DistanceJoint_EnableLimit
        , py::arg("joint_id")
        , py::arg("enable_limit")
        )
    .def("distance_joint_is_limit_enabled", &b2DistanceJoint_IsLimitEnabled
        , py::arg("joint_id")
        )
    .def("distance_joint_set_length_range", &b2DistanceJoint_SetLengthRange
        , py::arg("joint_id")
        , py::arg("min_length")
        , py::arg("max_length")
        )
    .def("distance_joint_get_min_length", &b2DistanceJoint_GetMinLength
        , py::arg("joint_id")
        )
    .def("distance_joint_get_max_length", &b2DistanceJoint_GetMaxLength
        , py::arg("joint_id")
        )
    .def("distance_joint_get_current_length", &b2DistanceJoint_GetCurrentLength
        , py::arg("joint_id")
        )
    .def("distance_joint_enable_motor", &b2DistanceJoint_EnableMotor
        , py::arg("joint_id")
        , py::arg("enable_motor")
        )
    .def("distance_joint_is_motor_enabled", &b2DistanceJoint_IsMotorEnabled
        , py::arg("joint_id")
        )
    .def("distance_joint_set_motor_speed", &b2DistanceJoint_SetMotorSpeed
        , py::arg("joint_id")
        , py::arg("motor_speed")
        )
    .def("distance_joint_get_motor_speed", &b2DistanceJoint_GetMotorSpeed
        , py::arg("joint_id")
        )
    .def("distance_joint_set_max_motor_force", &b2DistanceJoint_SetMaxMotorForce
        , py::arg("joint_id")
        , py::arg("force")
        )
    .def("distance_joint_get_max_motor_force", &b2DistanceJoint_GetMaxMotorForce
        , py::arg("joint_id")
        )
    .def("distance_joint_get_motor_force", &b2DistanceJoint_GetMotorForce
        , py::arg("joint_id")
        )
    .def("create_filter_joint", &b2CreateFilterJoint
        , py::arg("world_id")
        , py::arg("def")
        )
    .def("create_motor_joint", &b2CreateMotorJoint
        , py::arg("world_id")
        , py::arg("def")
        )
    .def("motor_joint_set_linear_velocity", &b2MotorJoint_SetLinearVelocity
        , py::arg("joint_id")
        , py::arg("velocity")
        )
    .def("motor_joint_get_linear_velocity", &b2MotorJoint_GetLinearVelocity
        , py::arg("joint_id")
        )
    .def("motor_joint_set_angular_velocity", &b2MotorJoint_SetAngularVelocity
        , py::arg("joint_id")
        , py::arg("velocity")
        )
    .def("motor_joint_get_angular_velocity", &b2MotorJoint_GetAngularVelocity
        , py::arg("joint_id")
        )
    .def("motor_joint_set_max_velocity_force", &b2MotorJoint_SetMaxVelocityForce
        , py::arg("joint_id")
        , py::arg("max_force")
        )
    .def("motor_joint_get_max_velocity_force", &b2MotorJoint_GetMaxVelocityForce
        , py::arg("joint_id")
        )
    .def("motor_joint_set_max_velocity_torque", &b2MotorJoint_SetMaxVelocityTorque
        , py::arg("joint_id")
        , py::arg("max_torque")
        )
    .def("motor_joint_get_max_velocity_torque", &b2MotorJoint_GetMaxVelocityTorque
        , py::arg("joint_id")
        )
    .def("motor_joint_set_linear_hertz", &b2MotorJoint_SetLinearHertz
        , py::arg("joint_id")
        , py::arg("hertz")
        )
    .def("motor_joint_get_linear_hertz", &b2MotorJoint_GetLinearHertz
        , py::arg("joint_id")
        )
    .def("motor_joint_set_linear_damping_ratio", &b2MotorJoint_SetLinearDampingRatio
        , py::arg("joint_id")
        , py::arg("damping")
        )
    .def("motor_joint_get_linear_damping_ratio", &b2MotorJoint_GetLinearDampingRatio
        , py::arg("joint_id")
        )
    .def("motor_joint_set_angular_hertz", &b2MotorJoint_SetAngularHertz
        , py::arg("joint_id")
        , py::arg("hertz")
        )
    .def("motor_joint_get_angular_hertz", &b2MotorJoint_GetAngularHertz
        , py::arg("joint_id")
        )
    .def("motor_joint_set_angular_damping_ratio", &b2MotorJoint_SetAngularDampingRatio
        , py::arg("joint_id")
        , py::arg("damping")
        )
    .def("motor_joint_get_angular_damping_ratio", &b2MotorJoint_GetAngularDampingRatio
        , py::arg("joint_id")
        )
    .def("motor_joint_set_max_spring_force", &b2MotorJoint_SetMaxSpringForce
        , py::arg("joint_id")
        , py::arg("max_force")
        )
    .def("motor_joint_get_max_spring_force", &b2MotorJoint_GetMaxSpringForce
        , py::arg("joint_id")
        )
    .def("motor_joint_set_max_spring_torque", &b2MotorJoint_SetMaxSpringTorque
        , py::arg("joint_id")
        , py::arg("max_torque")
        )
    .def("motor_joint_get_max_spring_torque", &b2MotorJoint_GetMaxSpringTorque
        , py::arg("joint_id")
        )
    .def("create_mover_joint", &b2CreateMoverJoint
        , py::arg("world_id")
        , py::arg("def")
        )
    .def("mover_joint_set_linear_velocity", &b2MoverJoint_SetLinearVelocity
        , py::arg("joint_id")
        , py::arg("velocity")
        )
    .def("mover_joint_get_linear_velocity", &b2MoverJoint_GetLinearVelocity
        , py::arg("joint_id")
        )
    .def("mover_joint_set_max_velocity_force", &b2MoverJoint_SetMaxVelocityForce
        , py::arg("joint_id")
        , py::arg("max_force")
        )
    .def("mover_joint_get_max_velocity_force", &b2MoverJoint_GetMaxVelocityForce
        , py::arg("joint_id")
        )
    .def("create_pogo_joint", &b2CreatePogoJoint
        , py::arg("world_id")
        , py::arg("def")
        )
    .def("pogo_joint_set_rest_length", &b2PogoJoint_SetRestLength
        , py::arg("joint_id")
        , py::arg("length")
        )
    .def("pogo_joint_get_rest_length", &b2PogoJoint_GetRestLength
        , py::arg("joint_id")
        )
    .def("pogo_joint_set_spring_hertz", &b2PogoJoint_SetSpringHertz
        , py::arg("joint_id")
        , py::arg("hertz")
        )
    .def("pogo_joint_get_spring_hertz", &b2PogoJoint_GetSpringHertz
        , py::arg("joint_id")
        )
    .def("pogo_joint_set_spring_damping_ratio", &b2PogoJoint_SetSpringDampingRatio
        , py::arg("joint_id")
        , py::arg("damping_ratio")
        )
    .def("pogo_joint_get_spring_damping_ratio", &b2PogoJoint_GetSpringDampingRatio
        , py::arg("joint_id")
        )
    .def("pogo_joint_get_length", &b2PogoJoint_GetLength
        , py::arg("joint_id")
        )
    .def("pogo_joint_get_velocity", &b2PogoJoint_GetVelocity
        , py::arg("joint_id")
        )
    .def("pogo_joint_get_impulse", &b2PogoJoint_GetImpulse
        , py::arg("joint_id")
        )
    .def("create_prismatic_joint", &b2CreatePrismaticJoint
        , py::arg("world_id")
        , py::arg("def")
        )
    .def("prismatic_joint_enable_spring", &b2PrismaticJoint_EnableSpring
        , py::arg("joint_id")
        , py::arg("enable_spring")
        )
    .def("prismatic_joint_is_spring_enabled", &b2PrismaticJoint_IsSpringEnabled
        , py::arg("joint_id")
        )
    .def("prismatic_joint_set_spring_hertz", &b2PrismaticJoint_SetSpringHertz
        , py::arg("joint_id")
        , py::arg("hertz")
        )
    .def("prismatic_joint_get_spring_hertz", &b2PrismaticJoint_GetSpringHertz
        , py::arg("joint_id")
        )
    .def("prismatic_joint_set_spring_damping_ratio", &b2PrismaticJoint_SetSpringDampingRatio
        , py::arg("joint_id")
        , py::arg("damping_ratio")
        )
    .def("prismatic_joint_get_spring_damping_ratio", &b2PrismaticJoint_GetSpringDampingRatio
        , py::arg("joint_id")
        )
    .def("prismatic_joint_set_target_translation", &b2PrismaticJoint_SetTargetTranslation
        , py::arg("joint_id")
        , py::arg("translation")
        )
    .def("prismatic_joint_get_target_translation", &b2PrismaticJoint_GetTargetTranslation
        , py::arg("joint_id")
        )
    .def("prismatic_joint_enable_limit", &b2PrismaticJoint_EnableLimit
        , py::arg("joint_id")
        , py::arg("enable_limit")
        )
    .def("prismatic_joint_is_limit_enabled", &b2PrismaticJoint_IsLimitEnabled
        , py::arg("joint_id")
        )
    .def("prismatic_joint_get_lower_limit", &b2PrismaticJoint_GetLowerLimit
        , py::arg("joint_id")
        )
    .def("prismatic_joint_get_upper_limit", &b2PrismaticJoint_GetUpperLimit
        , py::arg("joint_id")
        )
    .def("prismatic_joint_set_limits", &b2PrismaticJoint_SetLimits
        , py::arg("joint_id")
        , py::arg("lower")
        , py::arg("upper")
        )
    .def("prismatic_joint_enable_motor", &b2PrismaticJoint_EnableMotor
        , py::arg("joint_id")
        , py::arg("enable_motor")
        )
    .def("prismatic_joint_is_motor_enabled", &b2PrismaticJoint_IsMotorEnabled
        , py::arg("joint_id")
        )
    .def("prismatic_joint_set_motor_speed", &b2PrismaticJoint_SetMotorSpeed
        , py::arg("joint_id")
        , py::arg("motor_speed")
        )
    .def("prismatic_joint_get_motor_speed", &b2PrismaticJoint_GetMotorSpeed
        , py::arg("joint_id")
        )
    .def("prismatic_joint_set_max_motor_force", &b2PrismaticJoint_SetMaxMotorForce
        , py::arg("joint_id")
        , py::arg("force")
        )
    .def("prismatic_joint_get_max_motor_force", &b2PrismaticJoint_GetMaxMotorForce
        , py::arg("joint_id")
        )
    .def("prismatic_joint_get_motor_force", &b2PrismaticJoint_GetMotorForce
        , py::arg("joint_id")
        )
    .def("prismatic_joint_get_translation", &b2PrismaticJoint_GetTranslation
        , py::arg("joint_id")
        )
    .def("prismatic_joint_get_speed", &b2PrismaticJoint_GetSpeed
        , py::arg("joint_id")
        )
    .def("create_revolute_joint", &b2CreateRevoluteJoint
        , py::arg("world_id")
        , py::arg("def")
        )
    .def("revolute_joint_enable_spring", &b2RevoluteJoint_EnableSpring
        , py::arg("joint_id")
        , py::arg("enable_spring")
        )
    .def("revolute_joint_is_spring_enabled", &b2RevoluteJoint_IsSpringEnabled
        , py::arg("joint_id")
        )
    .def("revolute_joint_set_spring_hertz", &b2RevoluteJoint_SetSpringHertz
        , py::arg("joint_id")
        , py::arg("hertz")
        )
    .def("revolute_joint_get_spring_hertz", &b2RevoluteJoint_GetSpringHertz
        , py::arg("joint_id")
        )
    .def("revolute_joint_set_spring_damping_ratio", &b2RevoluteJoint_SetSpringDampingRatio
        , py::arg("joint_id")
        , py::arg("damping_ratio")
        )
    .def("revolute_joint_get_spring_damping_ratio", &b2RevoluteJoint_GetSpringDampingRatio
        , py::arg("joint_id")
        )
    .def("revolute_joint_set_target_angle", &b2RevoluteJoint_SetTargetAngle
        , py::arg("joint_id")
        , py::arg("angle")
        )
    .def("revolute_joint_get_target_angle", &b2RevoluteJoint_GetTargetAngle
        , py::arg("joint_id")
        )
    .def("revolute_joint_get_angle", &b2RevoluteJoint_GetAngle
        , py::arg("joint_id")
        )
    .def("revolute_joint_enable_limit", &b2RevoluteJoint_EnableLimit
        , py::arg("joint_id")
        , py::arg("enable_limit")
        )
    .def("revolute_joint_is_limit_enabled", &b2RevoluteJoint_IsLimitEnabled
        , py::arg("joint_id")
        )
    .def("revolute_joint_get_lower_limit", &b2RevoluteJoint_GetLowerLimit
        , py::arg("joint_id")
        )
    .def("revolute_joint_get_upper_limit", &b2RevoluteJoint_GetUpperLimit
        , py::arg("joint_id")
        )
    .def("revolute_joint_set_limits", &b2RevoluteJoint_SetLimits
        , py::arg("joint_id")
        , py::arg("lower")
        , py::arg("upper")
        )
    .def("revolute_joint_enable_motor", &b2RevoluteJoint_EnableMotor
        , py::arg("joint_id")
        , py::arg("enable_motor")
        )
    .def("revolute_joint_is_motor_enabled", &b2RevoluteJoint_IsMotorEnabled
        , py::arg("joint_id")
        )
    .def("revolute_joint_set_motor_speed", &b2RevoluteJoint_SetMotorSpeed
        , py::arg("joint_id")
        , py::arg("motor_speed")
        )
    .def("revolute_joint_get_motor_speed", &b2RevoluteJoint_GetMotorSpeed
        , py::arg("joint_id")
        )
    .def("revolute_joint_get_motor_torque", &b2RevoluteJoint_GetMotorTorque
        , py::arg("joint_id")
        )
    .def("revolute_joint_set_max_motor_torque", &b2RevoluteJoint_SetMaxMotorTorque
        , py::arg("joint_id")
        , py::arg("torque")
        )
    .def("revolute_joint_get_max_motor_torque", &b2RevoluteJoint_GetMaxMotorTorque
        , py::arg("joint_id")
        )
    .def("create_weld_joint", &b2CreateWeldJoint
        , py::arg("world_id")
        , py::arg("def")
        )
    .def("weld_joint_set_linear_hertz", &b2WeldJoint_SetLinearHertz
        , py::arg("joint_id")
        , py::arg("hertz")
        )
    .def("weld_joint_get_linear_hertz", &b2WeldJoint_GetLinearHertz
        , py::arg("joint_id")
        )
    .def("weld_joint_set_linear_damping_ratio", &b2WeldJoint_SetLinearDampingRatio
        , py::arg("joint_id")
        , py::arg("damping_ratio")
        )
    .def("weld_joint_get_linear_damping_ratio", &b2WeldJoint_GetLinearDampingRatio
        , py::arg("joint_id")
        )
    .def("weld_joint_set_angular_hertz", &b2WeldJoint_SetAngularHertz
        , py::arg("joint_id")
        , py::arg("hertz")
        )
    .def("weld_joint_get_angular_hertz", &b2WeldJoint_GetAngularHertz
        , py::arg("joint_id")
        )
    .def("weld_joint_set_angular_damping_ratio", &b2WeldJoint_SetAngularDampingRatio
        , py::arg("joint_id")
        , py::arg("damping_ratio")
        )
    .def("weld_joint_get_angular_damping_ratio", &b2WeldJoint_GetAngularDampingRatio
        , py::arg("joint_id")
        )
    .def("create_wheel_joint", &b2CreateWheelJoint
        , py::arg("world_id")
        , py::arg("def")
        )
    .def("wheel_joint_enable_spring", &b2WheelJoint_EnableSpring
        , py::arg("joint_id")
        , py::arg("enable_spring")
        )
    .def("wheel_joint_is_spring_enabled", &b2WheelJoint_IsSpringEnabled
        , py::arg("joint_id")
        )
    .def("wheel_joint_set_spring_hertz", &b2WheelJoint_SetSpringHertz
        , py::arg("joint_id")
        , py::arg("hertz")
        )
    .def("wheel_joint_get_spring_hertz", &b2WheelJoint_GetSpringHertz
        , py::arg("joint_id")
        )
    .def("wheel_joint_set_spring_damping_ratio", &b2WheelJoint_SetSpringDampingRatio
        , py::arg("joint_id")
        , py::arg("damping_ratio")
        )
    .def("wheel_joint_get_spring_damping_ratio", &b2WheelJoint_GetSpringDampingRatio
        , py::arg("joint_id")
        )
    .def("wheel_joint_enable_limit", &b2WheelJoint_EnableLimit
        , py::arg("joint_id")
        , py::arg("enable_limit")
        )
    .def("wheel_joint_is_limit_enabled", &b2WheelJoint_IsLimitEnabled
        , py::arg("joint_id")
        )
    .def("wheel_joint_get_lower_limit", &b2WheelJoint_GetLowerLimit
        , py::arg("joint_id")
        )
    .def("wheel_joint_get_upper_limit", &b2WheelJoint_GetUpperLimit
        , py::arg("joint_id")
        )
    .def("wheel_joint_set_limits", &b2WheelJoint_SetLimits
        , py::arg("joint_id")
        , py::arg("lower")
        , py::arg("upper")
        )
    .def("wheel_joint_enable_motor", &b2WheelJoint_EnableMotor
        , py::arg("joint_id")
        , py::arg("enable_motor")
        )
    .def("wheel_joint_is_motor_enabled", &b2WheelJoint_IsMotorEnabled
        , py::arg("joint_id")
        )
    .def("wheel_joint_set_motor_speed", &b2WheelJoint_SetMotorSpeed
        , py::arg("joint_id")
        , py::arg("motor_speed")
        )
    .def("wheel_joint_get_motor_speed", &b2WheelJoint_GetMotorSpeed
        , py::arg("joint_id")
        )
    .def("wheel_joint_set_max_motor_torque", &b2WheelJoint_SetMaxMotorTorque
        , py::arg("joint_id")
        , py::arg("torque")
        )
    .def("wheel_joint_get_max_motor_torque", &b2WheelJoint_GetMaxMotorTorque
        , py::arg("joint_id")
        )
    .def("wheel_joint_get_motor_torque", &b2WheelJoint_GetMotorTorque
        , py::arg("joint_id")
        )
    .def("contact_is_valid", &b2Contact_IsValid
        , py::arg("id")
        )
    .def("contact_get_data", &b2Contact_GetData
        , py::arg("contact_id")
        )
    .def("validate_replay", &b2ValidateReplay
        , py::arg("data")
        , py::arg("size")
        , py::arg("worker_count")
        )
    ;

    py::class_<b2RecPlayerInfo> _RecPlayerInfo(_box2d, "RecPlayerInfo");
    registry.on(_box2d, "RecPlayerInfo", _RecPlayerInfo);
        _RecPlayerInfo
        .def_readwrite("frame_count", &b2RecPlayerInfo::frameCount)
        .def_readwrite("worker_count", &b2RecPlayerInfo::workerCount)
        .def_readwrite("time_step", &b2RecPlayerInfo::timeStep)
        .def_readwrite("sub_step_count", &b2RecPlayerInfo::subStepCount)
        .def_readwrite("length_scale", &b2RecPlayerInfo::lengthScale)
        .def_readwrite("bounds", &b2RecPlayerInfo::bounds)
    ;

    _box2d
    .def("rec_player_create", [](const void * data, int size, int workerCount)
        {
            return py::capsule(b2RecPlayer_Create(data, size, workerCount), "b2RecPlayer");
        }
        , py::arg("data")
        , py::arg("size")
        , py::arg("worker_count")
        )
    .def("rec_player_step_frame", [](py::capsule player)
        {
            return b2RecPlayer_StepFrame(static_cast<b2RecPlayer *>(player.get_pointer()));
        }
        , py::arg("player")
        )
    .def("rec_player_get_world_id", [](py::capsule player)
        {
            return b2RecPlayer_GetWorldId(static_cast<const b2RecPlayer *>(player.get_pointer()));
        }
        , py::arg("player")
        )
    .def("rec_player_restart", [](py::capsule player)
        {
            return b2RecPlayer_Restart(static_cast<b2RecPlayer *>(player.get_pointer()));
        }
        , py::arg("player")
        )
    .def("rec_player_seek_frame", [](py::capsule player, int targetFrame)
        {
            return b2RecPlayer_SeekFrame(static_cast<b2RecPlayer *>(player.get_pointer()), targetFrame);
        }
        , py::arg("player")
        , py::arg("target_frame")
        )
    .def("rec_player_get_frame", [](py::capsule player)
        {
            return b2RecPlayer_GetFrame(static_cast<const b2RecPlayer *>(player.get_pointer()));
        }
        , py::arg("player")
        )
    .def("rec_player_get_info", [](py::capsule player)
        {
            return b2RecPlayer_GetInfo(static_cast<const b2RecPlayer *>(player.get_pointer()));
        }
        , py::arg("player")
        )
    .def("rec_player_is_at_end", [](py::capsule player)
        {
            return b2RecPlayer_IsAtEnd(static_cast<const b2RecPlayer *>(player.get_pointer()));
        }
        , py::arg("player")
        )
    .def("rec_player_has_diverged", [](py::capsule player)
        {
            return b2RecPlayer_HasDiverged(static_cast<const b2RecPlayer *>(player.get_pointer()));
        }
        , py::arg("player")
        )
    .def("rec_player_get_diverge_frame", [](py::capsule player)
        {
            return b2RecPlayer_GetDivergeFrame(static_cast<const b2RecPlayer *>(player.get_pointer()));
        }
        , py::arg("player")
        )
    .def("rec_player_set_keyframe_policy", [](py::capsule player, size_t budgetBytes, int minIntervalFrames)
        {
            return b2RecPlayer_SetKeyframePolicy(static_cast<b2RecPlayer *>(player.get_pointer()), budgetBytes, minIntervalFrames);
        }
        , py::arg("player")
        , py::arg("budget_bytes")
        , py::arg("min_interval_frames")
        )
    .def("rec_player_get_keyframe_budget", [](py::capsule player)
        {
            return b2RecPlayer_GetKeyframeBudget(static_cast<const b2RecPlayer *>(player.get_pointer()));
        }
        , py::arg("player")
        )
    .def("rec_player_get_keyframe_min_interval", [](py::capsule player)
        {
            return b2RecPlayer_GetKeyframeMinInterval(static_cast<const b2RecPlayer *>(player.get_pointer()));
        }
        , py::arg("player")
        )
    .def("rec_player_get_keyframe_interval", [](py::capsule player)
        {
            return b2RecPlayer_GetKeyframeInterval(static_cast<const b2RecPlayer *>(player.get_pointer()));
        }
        , py::arg("player")
        )
    .def("rec_player_get_keyframe_bytes", [](py::capsule player)
        {
            return b2RecPlayer_GetKeyframeBytes(static_cast<const b2RecPlayer *>(player.get_pointer()));
        }
        , py::arg("player")
        )
    .def("rec_player_destroy", [](py::capsule player)
        {
            return b2RecPlayer_Destroy(static_cast<b2RecPlayer *>(player.get_pointer()));
        }
        , py::arg("player")
        )
    .def("rec_player_draw_frame_queries", [](py::capsule player, b2DebugDraw * draw, int queryIndex)
        {
            return b2RecPlayer_DrawFrameQueries(static_cast<b2RecPlayer *>(player.get_pointer()), draw, queryIndex);
        }
        , py::arg("player")
        , py::arg("draw")
        , py::arg("query_index")
        )
    ;

    py::enum_<b2RecQueryType>(_box2d, "RecQueryType", py::arithmetic())
        .value("REC_QUERY_OVERLAP_AABB", b2RecQueryType::b2_recQueryOverlapAABB)
        .value("REC_QUERY_OVERLAP_SHAPE", b2RecQueryType::b2_recQueryOverlapShape)
        .value("REC_QUERY_CAST_RAY", b2RecQueryType::b2_recQueryCastRay)
        .value("REC_QUERY_CAST_SHAPE", b2RecQueryType::b2_recQueryCastShape)
        .value("REC_QUERY_COLLIDE_MOVER", b2RecQueryType::b2_recQueryCollideMover)
        .value("REC_QUERY_CAST_RAY_CLOSEST", b2RecQueryType::b2_recQueryCastRayClosest)
        .value("REC_QUERY_CAST_MOVER", b2RecQueryType::b2_recQueryCastMover)
        .value("REC_QUERY_SHAPE_TEST_POINT", b2RecQueryType::b2_recQueryShapeTestPoint)
        .value("REC_QUERY_SHAPE_RAY_CAST", b2RecQueryType::b2_recQueryShapeRayCast)
        .export_values()
    ;
    py::class_<b2RecQueryInfo> _RecQueryInfo(_box2d, "RecQueryInfo");
    registry.on(_box2d, "RecQueryInfo", _RecQueryInfo);
        _RecQueryInfo
        .def_readwrite("type", &b2RecQueryInfo::type)
        .def_readwrite("filter", &b2RecQueryInfo::filter)
        .def_readwrite("aabb", &b2RecQueryInfo::aabb)
        .def_readwrite("origin", &b2RecQueryInfo::origin)
        .def_readwrite("translation", &b2RecQueryInfo::translation)
        .def_readwrite("shape", &b2RecQueryInfo::shape)
        .def_readwrite("hit_count", &b2RecQueryInfo::hitCount)
    ;

    py::class_<b2RecQueryHit> _RecQueryHit(_box2d, "RecQueryHit");
    registry.on(_box2d, "RecQueryHit", _RecQueryHit);
        _RecQueryHit
        .def_readwrite("shape", &b2RecQueryHit::shape)
        .def_readwrite("point", &b2RecQueryHit::point)
        .def_readwrite("normal", &b2RecQueryHit::normal)
        .def_readwrite("fraction", &b2RecQueryHit::fraction)
    ;

    _box2d
    .def("rec_player_get_frame_query_count", [](py::capsule player)
        {
            return b2RecPlayer_GetFrameQueryCount(static_cast<const b2RecPlayer *>(player.get_pointer()));
        }
        , py::arg("player")
        )
    .def("rec_player_get_frame_query", [](py::capsule player, int index)
        {
            return b2RecPlayer_GetFrameQuery(static_cast<const b2RecPlayer *>(player.get_pointer()), index);
        }
        , py::arg("player")
        , py::arg("index")
        )
    .def("rec_player_get_frame_query_hit", [](py::capsule player, int queryIndex, int hitIndex)
        {
            return b2RecPlayer_GetFrameQueryHit(static_cast<const b2RecPlayer *>(player.get_pointer()), queryIndex, hitIndex);
        }
        , py::arg("player")
        , py::arg("query_index")
        , py::arg("hit_index")
        )
    .def("rec_player_get_body_count", [](py::capsule player)
        {
            return b2RecPlayer_GetBodyCount(static_cast<const b2RecPlayer *>(player.get_pointer()));
        }
        , py::arg("player")
        )
    .def("rec_player_get_body_id", [](py::capsule player, int index)
        {
            return b2RecPlayer_GetBodyId(static_cast<const b2RecPlayer *>(player.get_pointer()), index);
        }
        , py::arg("player")
        , py::arg("index")
        )
    ;


}