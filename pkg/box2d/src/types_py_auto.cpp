#include <limits>
//#include <iostream>
#include <sstream>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>


#include <cxbind/cxbind.h>

//#include <crunge/box2d/crunge-box2d.h>
//#include <crunge/box2d/conversions.h>

#include <box2d/types.h>

namespace py = pybind11;

void init_types_py_auto(py::module &_box2d, Registry &registry) {
    py::class_<b2RayResult> _RayResult(_box2d, "RayResult");
    registry.on(_box2d, "RayResult", _RayResult);
        _RayResult
        .def_readwrite("shape_id", &b2RayResult::shapeId)
        .def_readwrite("point", &b2RayResult::point)
        .def_readwrite("normal", &b2RayResult::normal)
        .def_readwrite("fraction", &b2RayResult::fraction)
        .def_readwrite("node_visits", &b2RayResult::nodeVisits)
        .def_readwrite("leaf_visits", &b2RayResult::leafVisits)
        .def_readwrite("hit", &b2RayResult::hit)
    ;

    py::class_<b2WorldDef> _WorldDef(_box2d, "WorldDef");
    registry.on(_box2d, "WorldDef", _WorldDef);
        _WorldDef
        .def_readwrite("gravity", &b2WorldDef::gravity)
        .def_readwrite("restitution_threshold", &b2WorldDef::restitutionThreshold)
        .def_readwrite("hit_event_threshold", &b2WorldDef::hitEventThreshold)
        .def_readwrite("contact_hertz", &b2WorldDef::contactHertz)
        .def_readwrite("contact_damping_ratio", &b2WorldDef::contactDampingRatio)
        .def_readwrite("contact_speed", &b2WorldDef::contactSpeed)
        .def_readwrite("maximum_linear_speed", &b2WorldDef::maximumLinearSpeed)
        .def_readwrite("enable_sleep", &b2WorldDef::enableSleep)
        .def_readwrite("enable_continuous", &b2WorldDef::enableContinuous)
        .def_readwrite("enable_contact_softening", &b2WorldDef::enableContactSoftening)
        .def_readwrite("worker_count", &b2WorldDef::workerCount)
        .def_readwrite("user_task_context", &b2WorldDef::userTaskContext)
        .def_readwrite("user_data", &b2WorldDef::userData)
        .def_readwrite("internal_value", &b2WorldDef::internalValue)
        .def(py::init([](const py::kwargs& kwargs)
        {
            b2WorldDef obj = b2DefaultWorldDef();
            if (kwargs.contains("gravity"))
            {
                auto value = kwargs["gravity"].cast<struct b2Vec2>();
                obj.gravity = value;
            }
            if (kwargs.contains("restitution_threshold"))
            {
                auto value = kwargs["restitution_threshold"].cast<float>();
                obj.restitutionThreshold = value;
            }
            if (kwargs.contains("hit_event_threshold"))
            {
                auto value = kwargs["hit_event_threshold"].cast<float>();
                obj.hitEventThreshold = value;
            }
            if (kwargs.contains("contact_hertz"))
            {
                auto value = kwargs["contact_hertz"].cast<float>();
                obj.contactHertz = value;
            }
            if (kwargs.contains("contact_damping_ratio"))
            {
                auto value = kwargs["contact_damping_ratio"].cast<float>();
                obj.contactDampingRatio = value;
            }
            if (kwargs.contains("contact_speed"))
            {
                auto value = kwargs["contact_speed"].cast<float>();
                obj.contactSpeed = value;
            }
            if (kwargs.contains("maximum_linear_speed"))
            {
                auto value = kwargs["maximum_linear_speed"].cast<float>();
                obj.maximumLinearSpeed = value;
            }
            if (kwargs.contains("enable_sleep"))
            {
                auto value = kwargs["enable_sleep"].cast<_Bool>();
                obj.enableSleep = value;
            }
            if (kwargs.contains("enable_continuous"))
            {
                auto value = kwargs["enable_continuous"].cast<_Bool>();
                obj.enableContinuous = value;
            }
            if (kwargs.contains("enable_contact_softening"))
            {
                auto value = kwargs["enable_contact_softening"].cast<_Bool>();
                obj.enableContactSoftening = value;
            }
            if (kwargs.contains("worker_count"))
            {
                auto value = kwargs["worker_count"].cast<int>();
                obj.workerCount = value;
            }
            if (kwargs.contains("user_task_context"))
            {
                auto value = kwargs["user_task_context"].cast<void *>();
                obj.userTaskContext = value;
            }
            if (kwargs.contains("user_data"))
            {
                auto value = kwargs["user_data"].cast<void *>();
                obj.userData = value;
            }
            if (kwargs.contains("internal_value"))
            {
                auto value = kwargs["internal_value"].cast<int>();
                obj.internalValue = value;
            }
            return obj;
        }))
        .def("__repr__", [](const b2WorldDef &self) {
            std::stringstream ss;
            ss << "WorldDef(";
            ss << "gravity=" << py::repr(py::cast(self.gravity)).cast<std::string>();
            ss << ", ";
            ss << "restitutionThreshold=" << py::repr(py::cast(self.restitutionThreshold)).cast<std::string>();
            ss << ", ";
            ss << "hitEventThreshold=" << py::repr(py::cast(self.hitEventThreshold)).cast<std::string>();
            ss << ", ";
            ss << "contactHertz=" << py::repr(py::cast(self.contactHertz)).cast<std::string>();
            ss << ", ";
            ss << "contactDampingRatio=" << py::repr(py::cast(self.contactDampingRatio)).cast<std::string>();
            ss << ", ";
            ss << "contactSpeed=" << py::repr(py::cast(self.contactSpeed)).cast<std::string>();
            ss << ", ";
            ss << "maximumLinearSpeed=" << py::repr(py::cast(self.maximumLinearSpeed)).cast<std::string>();
            ss << ", ";
            ss << "enableSleep=" << py::repr(py::cast(self.enableSleep)).cast<std::string>();
            ss << ", ";
            ss << "enableContinuous=" << py::repr(py::cast(self.enableContinuous)).cast<std::string>();
            ss << ", ";
            ss << "enableContactSoftening=" << py::repr(py::cast(self.enableContactSoftening)).cast<std::string>();
            ss << ", ";
            ss << "workerCount=" << py::repr(py::cast(self.workerCount)).cast<std::string>();
            ss << ", ";
            ss << "userTaskContext=" << py::repr(py::cast(self.userTaskContext)).cast<std::string>();
            ss << ", ";
            ss << "userData=" << py::repr(py::cast(self.userData)).cast<std::string>();
            ss << ", ";
            ss << "internalValue=" << py::repr(py::cast(self.internalValue)).cast<std::string>();
            ss << ")";
            return ss.str();
        })
    ;

    _box2d
    .def("default_world_def", &b2DefaultWorldDef
        , py::return_value_policy::automatic_reference)
    ;

    py::enum_<b2BodyType>(_box2d, "BodyType", py::arithmetic())
        .value("STATIC_BODY", b2BodyType::b2_staticBody)
        .value("KINEMATIC_BODY", b2BodyType::b2_kinematicBody)
        .value("DYNAMIC_BODY", b2BodyType::b2_dynamicBody)
        .value("BODY_TYPE_COUNT", b2BodyType::b2_bodyTypeCount)
        .export_values()
    ;
    py::class_<b2MotionLocks> _MotionLocks(_box2d, "MotionLocks");
    registry.on(_box2d, "MotionLocks", _MotionLocks);
        _MotionLocks
        .def_readwrite("linear_x", &b2MotionLocks::linearX)
        .def_readwrite("linear_y", &b2MotionLocks::linearY)
        .def_readwrite("angular_z", &b2MotionLocks::angularZ)
    ;

    py::class_<b2BodyDef> _BodyDef(_box2d, "BodyDef");
    registry.on(_box2d, "BodyDef", _BodyDef);
        _BodyDef
        .def_readwrite("type", &b2BodyDef::type)
        .def_readwrite("position", &b2BodyDef::position)
        .def_readwrite("rotation", &b2BodyDef::rotation)
        .def_readwrite("linear_velocity", &b2BodyDef::linearVelocity)
        .def_readwrite("angular_velocity", &b2BodyDef::angularVelocity)
        .def_readwrite("linear_damping", &b2BodyDef::linearDamping)
        .def_readwrite("angular_damping", &b2BodyDef::angularDamping)
        .def_readwrite("gravity_scale", &b2BodyDef::gravityScale)
        .def_readwrite("sleep_threshold", &b2BodyDef::sleepThreshold)
        .def_property("name",
            [](const b2BodyDef& self){ return self.name; },
            [](b2BodyDef& self, const char* source){ self.name = strdup(source); }
        )
        .def_readwrite("user_data", &b2BodyDef::userData)
        .def_readwrite("motion_locks", &b2BodyDef::motionLocks)
        .def_readwrite("enable_sleep", &b2BodyDef::enableSleep)
        .def_readwrite("is_awake", &b2BodyDef::isAwake)
        .def_readwrite("is_bullet", &b2BodyDef::isBullet)
        .def_readwrite("is_enabled", &b2BodyDef::isEnabled)
        .def_readwrite("allow_fast_rotation", &b2BodyDef::allowFastRotation)
        .def_readwrite("internal_value", &b2BodyDef::internalValue)
        .def(py::init([](const py::kwargs& kwargs)
        {
            b2BodyDef obj = b2DefaultBodyDef();
            if (kwargs.contains("type"))
            {
                auto value = kwargs["type"].cast<enum b2BodyType>();
                obj.type = value;
            }
            if (kwargs.contains("position"))
            {
                auto value = kwargs["position"].cast<struct b2Vec2>();
                obj.position = value;
            }
            if (kwargs.contains("rotation"))
            {
                auto value = kwargs["rotation"].cast<struct b2Rot>();
                obj.rotation = value;
            }
            if (kwargs.contains("linear_velocity"))
            {
                auto value = kwargs["linear_velocity"].cast<struct b2Vec2>();
                obj.linearVelocity = value;
            }
            if (kwargs.contains("angular_velocity"))
            {
                auto value = kwargs["angular_velocity"].cast<float>();
                obj.angularVelocity = value;
            }
            if (kwargs.contains("linear_damping"))
            {
                auto value = kwargs["linear_damping"].cast<float>();
                obj.linearDamping = value;
            }
            if (kwargs.contains("angular_damping"))
            {
                auto value = kwargs["angular_damping"].cast<float>();
                obj.angularDamping = value;
            }
            if (kwargs.contains("gravity_scale"))
            {
                auto value = kwargs["gravity_scale"].cast<float>();
                obj.gravityScale = value;
            }
            if (kwargs.contains("sleep_threshold"))
            {
                auto value = kwargs["sleep_threshold"].cast<float>();
                obj.sleepThreshold = value;
            }
            if (kwargs.contains("name"))
            {
                auto _value = kwargs["name"].cast<std::string>();
                char* value = (char*)malloc(_value.size());
                strcpy(value, _value.c_str());
                obj.name = value;
            }
            if (kwargs.contains("user_data"))
            {
                auto value = kwargs["user_data"].cast<void *>();
                obj.userData = value;
            }
            if (kwargs.contains("motion_locks"))
            {
                auto value = kwargs["motion_locks"].cast<struct b2MotionLocks>();
                obj.motionLocks = value;
            }
            if (kwargs.contains("enable_sleep"))
            {
                auto value = kwargs["enable_sleep"].cast<_Bool>();
                obj.enableSleep = value;
            }
            if (kwargs.contains("is_awake"))
            {
                auto value = kwargs["is_awake"].cast<_Bool>();
                obj.isAwake = value;
            }
            if (kwargs.contains("is_bullet"))
            {
                auto value = kwargs["is_bullet"].cast<_Bool>();
                obj.isBullet = value;
            }
            if (kwargs.contains("is_enabled"))
            {
                auto value = kwargs["is_enabled"].cast<_Bool>();
                obj.isEnabled = value;
            }
            if (kwargs.contains("allow_fast_rotation"))
            {
                auto value = kwargs["allow_fast_rotation"].cast<_Bool>();
                obj.allowFastRotation = value;
            }
            if (kwargs.contains("internal_value"))
            {
                auto value = kwargs["internal_value"].cast<int>();
                obj.internalValue = value;
            }
            return obj;
        }))
        .def("__repr__", [](const b2BodyDef &self) {
            std::stringstream ss;
            ss << "BodyDef(";
            ss << "type=" << py::repr(py::cast(self.type)).cast<std::string>();
            ss << ", ";
            ss << "position=" << py::repr(py::cast(self.position)).cast<std::string>();
            ss << ", ";
            ss << "rotation=" << py::repr(py::cast(self.rotation)).cast<std::string>();
            ss << ", ";
            ss << "linearVelocity=" << py::repr(py::cast(self.linearVelocity)).cast<std::string>();
            ss << ", ";
            ss << "angularVelocity=" << py::repr(py::cast(self.angularVelocity)).cast<std::string>();
            ss << ", ";
            ss << "linearDamping=" << py::repr(py::cast(self.linearDamping)).cast<std::string>();
            ss << ", ";
            ss << "angularDamping=" << py::repr(py::cast(self.angularDamping)).cast<std::string>();
            ss << ", ";
            ss << "gravityScale=" << py::repr(py::cast(self.gravityScale)).cast<std::string>();
            ss << ", ";
            ss << "sleepThreshold=" << py::repr(py::cast(self.sleepThreshold)).cast<std::string>();
            ss << ", ";
            ss << "name=" << py::repr(py::cast(self.name)).cast<std::string>();
            ss << ", ";
            ss << "userData=" << py::repr(py::cast(self.userData)).cast<std::string>();
            ss << ", ";
            ss << "motionLocks=" << py::repr(py::cast(self.motionLocks)).cast<std::string>();
            ss << ", ";
            ss << "enableSleep=" << py::repr(py::cast(self.enableSleep)).cast<std::string>();
            ss << ", ";
            ss << "isAwake=" << py::repr(py::cast(self.isAwake)).cast<std::string>();
            ss << ", ";
            ss << "isBullet=" << py::repr(py::cast(self.isBullet)).cast<std::string>();
            ss << ", ";
            ss << "isEnabled=" << py::repr(py::cast(self.isEnabled)).cast<std::string>();
            ss << ", ";
            ss << "allowFastRotation=" << py::repr(py::cast(self.allowFastRotation)).cast<std::string>();
            ss << ", ";
            ss << "internalValue=" << py::repr(py::cast(self.internalValue)).cast<std::string>();
            ss << ")";
            return ss.str();
        })
    ;

    _box2d
    .def("default_body_def", &b2DefaultBodyDef
        , py::return_value_policy::automatic_reference)
    ;

    py::class_<b2Filter> _Filter(_box2d, "Filter");
    registry.on(_box2d, "Filter", _Filter);
        _Filter
        .def_readwrite("category_bits", &b2Filter::categoryBits)
        .def_readwrite("mask_bits", &b2Filter::maskBits)
        .def_readwrite("group_index", &b2Filter::groupIndex)
    ;

    _box2d
    .def("default_filter", &b2DefaultFilter
        , py::return_value_policy::automatic_reference)
    ;

    py::class_<b2QueryFilter> _QueryFilter(_box2d, "QueryFilter");
    registry.on(_box2d, "QueryFilter", _QueryFilter);
        _QueryFilter
        .def_readwrite("category_bits", &b2QueryFilter::categoryBits)
        .def_readwrite("mask_bits", &b2QueryFilter::maskBits)
    ;

    _box2d
    .def("default_query_filter", &b2DefaultQueryFilter
        , py::return_value_policy::automatic_reference)
    ;

    py::enum_<b2ShapeType>(_box2d, "ShapeType", py::arithmetic())
        .value("CIRCLE_SHAPE", b2ShapeType::b2_circleShape)
        .value("CAPSULE_SHAPE", b2ShapeType::b2_capsuleShape)
        .value("SEGMENT_SHAPE", b2ShapeType::b2_segmentShape)
        .value("POLYGON_SHAPE", b2ShapeType::b2_polygonShape)
        .value("CHAIN_SEGMENT_SHAPE", b2ShapeType::b2_chainSegmentShape)
        .value("SHAPE_TYPE_COUNT", b2ShapeType::b2_shapeTypeCount)
        .export_values()
    ;
    py::class_<b2SurfaceMaterial> _SurfaceMaterial(_box2d, "SurfaceMaterial");
    registry.on(_box2d, "SurfaceMaterial", _SurfaceMaterial);
        _SurfaceMaterial
        .def_readwrite("friction", &b2SurfaceMaterial::friction)
        .def_readwrite("restitution", &b2SurfaceMaterial::restitution)
        .def_readwrite("rolling_resistance", &b2SurfaceMaterial::rollingResistance)
        .def_readwrite("tangent_speed", &b2SurfaceMaterial::tangentSpeed)
        .def_readwrite("user_material_id", &b2SurfaceMaterial::userMaterialId)
        .def_readwrite("custom_color", &b2SurfaceMaterial::customColor)
    ;

    _box2d
    .def("default_surface_material", &b2DefaultSurfaceMaterial
        , py::return_value_policy::automatic_reference)
    ;

    py::class_<b2ShapeDef> _ShapeDef(_box2d, "ShapeDef");
    registry.on(_box2d, "ShapeDef", _ShapeDef);
        _ShapeDef
        .def_readwrite("user_data", &b2ShapeDef::userData)
        .def_readwrite("material", &b2ShapeDef::material)
        .def_readwrite("density", &b2ShapeDef::density)
        .def_readwrite("filter", &b2ShapeDef::filter)
        .def_readwrite("enable_custom_filtering", &b2ShapeDef::enableCustomFiltering)
        .def_readwrite("is_sensor", &b2ShapeDef::isSensor)
        .def_readwrite("enable_sensor_events", &b2ShapeDef::enableSensorEvents)
        .def_readwrite("enable_contact_events", &b2ShapeDef::enableContactEvents)
        .def_readwrite("enable_hit_events", &b2ShapeDef::enableHitEvents)
        .def_readwrite("enable_pre_solve_events", &b2ShapeDef::enablePreSolveEvents)
        .def_readwrite("invoke_contact_creation", &b2ShapeDef::invokeContactCreation)
        .def_readwrite("update_body_mass", &b2ShapeDef::updateBodyMass)
        .def_readwrite("internal_value", &b2ShapeDef::internalValue)
        .def(py::init([](const py::kwargs& kwargs)
        {
            b2ShapeDef obj = b2DefaultShapeDef();
            if (kwargs.contains("user_data"))
            {
                auto value = kwargs["user_data"].cast<void *>();
                obj.userData = value;
            }
            if (kwargs.contains("material"))
            {
                auto value = kwargs["material"].cast<struct b2SurfaceMaterial>();
                obj.material = value;
            }
            if (kwargs.contains("density"))
            {
                auto value = kwargs["density"].cast<float>();
                obj.density = value;
            }
            if (kwargs.contains("filter"))
            {
                auto value = kwargs["filter"].cast<struct b2Filter>();
                obj.filter = value;
            }
            if (kwargs.contains("enable_custom_filtering"))
            {
                auto value = kwargs["enable_custom_filtering"].cast<_Bool>();
                obj.enableCustomFiltering = value;
            }
            if (kwargs.contains("is_sensor"))
            {
                auto value = kwargs["is_sensor"].cast<_Bool>();
                obj.isSensor = value;
            }
            if (kwargs.contains("enable_sensor_events"))
            {
                auto value = kwargs["enable_sensor_events"].cast<_Bool>();
                obj.enableSensorEvents = value;
            }
            if (kwargs.contains("enable_contact_events"))
            {
                auto value = kwargs["enable_contact_events"].cast<_Bool>();
                obj.enableContactEvents = value;
            }
            if (kwargs.contains("enable_hit_events"))
            {
                auto value = kwargs["enable_hit_events"].cast<_Bool>();
                obj.enableHitEvents = value;
            }
            if (kwargs.contains("enable_pre_solve_events"))
            {
                auto value = kwargs["enable_pre_solve_events"].cast<_Bool>();
                obj.enablePreSolveEvents = value;
            }
            if (kwargs.contains("invoke_contact_creation"))
            {
                auto value = kwargs["invoke_contact_creation"].cast<_Bool>();
                obj.invokeContactCreation = value;
            }
            if (kwargs.contains("update_body_mass"))
            {
                auto value = kwargs["update_body_mass"].cast<_Bool>();
                obj.updateBodyMass = value;
            }
            if (kwargs.contains("internal_value"))
            {
                auto value = kwargs["internal_value"].cast<int>();
                obj.internalValue = value;
            }
            return obj;
        }))
        .def("__repr__", [](const b2ShapeDef &self) {
            std::stringstream ss;
            ss << "ShapeDef(";
            ss << "userData=" << py::repr(py::cast(self.userData)).cast<std::string>();
            ss << ", ";
            ss << "material=" << py::repr(py::cast(self.material)).cast<std::string>();
            ss << ", ";
            ss << "density=" << py::repr(py::cast(self.density)).cast<std::string>();
            ss << ", ";
            ss << "filter=" << py::repr(py::cast(self.filter)).cast<std::string>();
            ss << ", ";
            ss << "enableCustomFiltering=" << py::repr(py::cast(self.enableCustomFiltering)).cast<std::string>();
            ss << ", ";
            ss << "isSensor=" << py::repr(py::cast(self.isSensor)).cast<std::string>();
            ss << ", ";
            ss << "enableSensorEvents=" << py::repr(py::cast(self.enableSensorEvents)).cast<std::string>();
            ss << ", ";
            ss << "enableContactEvents=" << py::repr(py::cast(self.enableContactEvents)).cast<std::string>();
            ss << ", ";
            ss << "enableHitEvents=" << py::repr(py::cast(self.enableHitEvents)).cast<std::string>();
            ss << ", ";
            ss << "enablePreSolveEvents=" << py::repr(py::cast(self.enablePreSolveEvents)).cast<std::string>();
            ss << ", ";
            ss << "invokeContactCreation=" << py::repr(py::cast(self.invokeContactCreation)).cast<std::string>();
            ss << ", ";
            ss << "updateBodyMass=" << py::repr(py::cast(self.updateBodyMass)).cast<std::string>();
            ss << ", ";
            ss << "internalValue=" << py::repr(py::cast(self.internalValue)).cast<std::string>();
            ss << ")";
            return ss.str();
        })
    ;

    _box2d
    .def("default_shape_def", &b2DefaultShapeDef
        , py::return_value_policy::automatic_reference)
    ;

    py::class_<b2ChainDef> _ChainDef(_box2d, "ChainDef");
    registry.on(_box2d, "ChainDef", _ChainDef);
        _ChainDef
        .def_readwrite("user_data", &b2ChainDef::userData)
        .def_readwrite("points", &b2ChainDef::points)
        .def_readwrite("count", &b2ChainDef::count)
        .def_readwrite("materials", &b2ChainDef::materials)
        .def_readwrite("material_count", &b2ChainDef::materialCount)
        .def_readwrite("filter", &b2ChainDef::filter)
        .def_readwrite("is_loop", &b2ChainDef::isLoop)
        .def_readwrite("enable_sensor_events", &b2ChainDef::enableSensorEvents)
        .def_readwrite("internal_value", &b2ChainDef::internalValue)
    ;

    _box2d
    .def("default_chain_def", &b2DefaultChainDef
        , py::return_value_policy::automatic_reference)
    ;

    py::class_<b2Profile> _Profile(_box2d, "Profile");
    registry.on(_box2d, "Profile", _Profile);
        _Profile
        .def_readwrite("step", &b2Profile::step)
        .def_readwrite("pairs", &b2Profile::pairs)
        .def_readwrite("collide", &b2Profile::collide)
        .def_readwrite("solve", &b2Profile::solve)
        .def_readwrite("prepare_stages", &b2Profile::prepareStages)
        .def_readwrite("solve_constraints", &b2Profile::solveConstraints)
        .def_readwrite("prepare_constraints", &b2Profile::prepareConstraints)
        .def_readwrite("integrate_velocities", &b2Profile::integrateVelocities)
        .def_readwrite("warm_start", &b2Profile::warmStart)
        .def_readwrite("solve_impulses", &b2Profile::solveImpulses)
        .def_readwrite("integrate_positions", &b2Profile::integratePositions)
        .def_readwrite("relax_impulses", &b2Profile::relaxImpulses)
        .def_readwrite("apply_restitution", &b2Profile::applyRestitution)
        .def_readwrite("store_impulses", &b2Profile::storeImpulses)
        .def_readwrite("split_islands", &b2Profile::splitIslands)
        .def_readwrite("transforms", &b2Profile::transforms)
        .def_readwrite("sensor_hits", &b2Profile::sensorHits)
        .def_readwrite("joint_events", &b2Profile::jointEvents)
        .def_readwrite("hit_events", &b2Profile::hitEvents)
        .def_readwrite("refit", &b2Profile::refit)
        .def_readwrite("bullets", &b2Profile::bullets)
        .def_readwrite("sleep_islands", &b2Profile::sleepIslands)
        .def_readwrite("sensors", &b2Profile::sensors)
    ;

    py::class_<b2Counters> _Counters(_box2d, "Counters");
    registry.on(_box2d, "Counters", _Counters);
        _Counters
        .def_readwrite("body_count", &b2Counters::bodyCount)
        .def_readwrite("shape_count", &b2Counters::shapeCount)
        .def_readwrite("contact_count", &b2Counters::contactCount)
        .def_readwrite("joint_count", &b2Counters::jointCount)
        .def_readwrite("island_count", &b2Counters::islandCount)
        .def_readwrite("stack_used", &b2Counters::stackUsed)
        .def_readwrite("static_tree_height", &b2Counters::staticTreeHeight)
        .def_readwrite("tree_height", &b2Counters::treeHeight)
        .def_readwrite("byte_count", &b2Counters::byteCount)
        .def_readwrite("task_count", &b2Counters::taskCount)
        .def_readonly("color_counts", &b2Counters::colorCounts)
    ;

    py::enum_<b2JointType>(_box2d, "JointType", py::arithmetic())
        .value("DISTANCE_JOINT", b2JointType::b2_distanceJoint)
        .value("FILTER_JOINT", b2JointType::b2_filterJoint)
        .value("MOTOR_JOINT", b2JointType::b2_motorJoint)
        .value("PRISMATIC_JOINT", b2JointType::b2_prismaticJoint)
        .value("REVOLUTE_JOINT", b2JointType::b2_revoluteJoint)
        .value("WELD_JOINT", b2JointType::b2_weldJoint)
        .value("WHEEL_JOINT", b2JointType::b2_wheelJoint)
        .export_values()
    ;
    py::class_<b2JointDef> _JointDef(_box2d, "JointDef");
    registry.on(_box2d, "JointDef", _JointDef);
        _JointDef
        .def_readwrite("user_data", &b2JointDef::userData)
        .def_readwrite("body_id_a", &b2JointDef::bodyIdA)
        .def_readwrite("body_id_b", &b2JointDef::bodyIdB)
        .def_readwrite("local_frame_a", &b2JointDef::localFrameA)
        .def_readwrite("local_frame_b", &b2JointDef::localFrameB)
        .def_readwrite("force_threshold", &b2JointDef::forceThreshold)
        .def_readwrite("torque_threshold", &b2JointDef::torqueThreshold)
        .def_readwrite("constraint_hertz", &b2JointDef::constraintHertz)
        .def_readwrite("constraint_damping_ratio", &b2JointDef::constraintDampingRatio)
        .def_readwrite("draw_scale", &b2JointDef::drawScale)
        .def_readwrite("collide_connected", &b2JointDef::collideConnected)
    ;

    py::class_<b2DistanceJointDef> _DistanceJointDef(_box2d, "DistanceJointDef");
    registry.on(_box2d, "DistanceJointDef", _DistanceJointDef);
        _DistanceJointDef
        .def_readwrite("base", &b2DistanceJointDef::base)
        .def_readwrite("length", &b2DistanceJointDef::length)
        .def_readwrite("enable_spring", &b2DistanceJointDef::enableSpring)
        .def_readwrite("lower_spring_force", &b2DistanceJointDef::lowerSpringForce)
        .def_readwrite("upper_spring_force", &b2DistanceJointDef::upperSpringForce)
        .def_readwrite("hertz", &b2DistanceJointDef::hertz)
        .def_readwrite("damping_ratio", &b2DistanceJointDef::dampingRatio)
        .def_readwrite("enable_limit", &b2DistanceJointDef::enableLimit)
        .def_readwrite("min_length", &b2DistanceJointDef::minLength)
        .def_readwrite("max_length", &b2DistanceJointDef::maxLength)
        .def_readwrite("enable_motor", &b2DistanceJointDef::enableMotor)
        .def_readwrite("max_motor_force", &b2DistanceJointDef::maxMotorForce)
        .def_readwrite("motor_speed", &b2DistanceJointDef::motorSpeed)
        .def_readwrite("internal_value", &b2DistanceJointDef::internalValue)
    ;

    _box2d
    .def("default_distance_joint_def", &b2DefaultDistanceJointDef
        , py::return_value_policy::automatic_reference)
    ;

    py::class_<b2MotorJointDef> _MotorJointDef(_box2d, "MotorJointDef");
    registry.on(_box2d, "MotorJointDef", _MotorJointDef);
        _MotorJointDef
        .def_readwrite("base", &b2MotorJointDef::base)
        .def_readwrite("linear_velocity", &b2MotorJointDef::linearVelocity)
        .def_readwrite("max_velocity_force", &b2MotorJointDef::maxVelocityForce)
        .def_readwrite("angular_velocity", &b2MotorJointDef::angularVelocity)
        .def_readwrite("max_velocity_torque", &b2MotorJointDef::maxVelocityTorque)
        .def_readwrite("linear_hertz", &b2MotorJointDef::linearHertz)
        .def_readwrite("linear_damping_ratio", &b2MotorJointDef::linearDampingRatio)
        .def_readwrite("max_spring_force", &b2MotorJointDef::maxSpringForce)
        .def_readwrite("angular_hertz", &b2MotorJointDef::angularHertz)
        .def_readwrite("angular_damping_ratio", &b2MotorJointDef::angularDampingRatio)
        .def_readwrite("max_spring_torque", &b2MotorJointDef::maxSpringTorque)
        .def_readwrite("internal_value", &b2MotorJointDef::internalValue)
    ;

    _box2d
    .def("default_motor_joint_def", &b2DefaultMotorJointDef
        , py::return_value_policy::automatic_reference)
    ;

    py::class_<b2FilterJointDef> _FilterJointDef(_box2d, "FilterJointDef");
    registry.on(_box2d, "FilterJointDef", _FilterJointDef);
        _FilterJointDef
        .def_readwrite("base", &b2FilterJointDef::base)
        .def_readwrite("internal_value", &b2FilterJointDef::internalValue)
    ;

    _box2d
    .def("default_filter_joint_def", &b2DefaultFilterJointDef
        , py::return_value_policy::automatic_reference)
    ;

    py::class_<b2PrismaticJointDef> _PrismaticJointDef(_box2d, "PrismaticJointDef");
    registry.on(_box2d, "PrismaticJointDef", _PrismaticJointDef);
        _PrismaticJointDef
        .def_readwrite("base", &b2PrismaticJointDef::base)
        .def_readwrite("enable_spring", &b2PrismaticJointDef::enableSpring)
        .def_readwrite("hertz", &b2PrismaticJointDef::hertz)
        .def_readwrite("damping_ratio", &b2PrismaticJointDef::dampingRatio)
        .def_readwrite("target_translation", &b2PrismaticJointDef::targetTranslation)
        .def_readwrite("enable_limit", &b2PrismaticJointDef::enableLimit)
        .def_readwrite("lower_translation", &b2PrismaticJointDef::lowerTranslation)
        .def_readwrite("upper_translation", &b2PrismaticJointDef::upperTranslation)
        .def_readwrite("enable_motor", &b2PrismaticJointDef::enableMotor)
        .def_readwrite("max_motor_force", &b2PrismaticJointDef::maxMotorForce)
        .def_readwrite("motor_speed", &b2PrismaticJointDef::motorSpeed)
        .def_readwrite("internal_value", &b2PrismaticJointDef::internalValue)
    ;

    _box2d
    .def("default_prismatic_joint_def", &b2DefaultPrismaticJointDef
        , py::return_value_policy::automatic_reference)
    ;

    py::class_<b2RevoluteJointDef> _RevoluteJointDef(_box2d, "RevoluteJointDef");
    registry.on(_box2d, "RevoluteJointDef", _RevoluteJointDef);
        _RevoluteJointDef
        .def_readwrite("base", &b2RevoluteJointDef::base)
        .def_readwrite("target_angle", &b2RevoluteJointDef::targetAngle)
        .def_readwrite("enable_spring", &b2RevoluteJointDef::enableSpring)
        .def_readwrite("hertz", &b2RevoluteJointDef::hertz)
        .def_readwrite("damping_ratio", &b2RevoluteJointDef::dampingRatio)
        .def_readwrite("enable_limit", &b2RevoluteJointDef::enableLimit)
        .def_readwrite("lower_angle", &b2RevoluteJointDef::lowerAngle)
        .def_readwrite("upper_angle", &b2RevoluteJointDef::upperAngle)
        .def_readwrite("enable_motor", &b2RevoluteJointDef::enableMotor)
        .def_readwrite("max_motor_torque", &b2RevoluteJointDef::maxMotorTorque)
        .def_readwrite("motor_speed", &b2RevoluteJointDef::motorSpeed)
        .def_readwrite("internal_value", &b2RevoluteJointDef::internalValue)
    ;

    _box2d
    .def("default_revolute_joint_def", &b2DefaultRevoluteJointDef
        , py::return_value_policy::automatic_reference)
    ;

    py::class_<b2WeldJointDef> _WeldJointDef(_box2d, "WeldJointDef");
    registry.on(_box2d, "WeldJointDef", _WeldJointDef);
        _WeldJointDef
        .def_readwrite("base", &b2WeldJointDef::base)
        .def_readwrite("linear_hertz", &b2WeldJointDef::linearHertz)
        .def_readwrite("angular_hertz", &b2WeldJointDef::angularHertz)
        .def_readwrite("linear_damping_ratio", &b2WeldJointDef::linearDampingRatio)
        .def_readwrite("angular_damping_ratio", &b2WeldJointDef::angularDampingRatio)
        .def_readwrite("internal_value", &b2WeldJointDef::internalValue)
    ;

    _box2d
    .def("default_weld_joint_def", &b2DefaultWeldJointDef
        , py::return_value_policy::automatic_reference)
    ;

    py::class_<b2WheelJointDef> _WheelJointDef(_box2d, "WheelJointDef");
    registry.on(_box2d, "WheelJointDef", _WheelJointDef);
        _WheelJointDef
        .def_readwrite("base", &b2WheelJointDef::base)
        .def_readwrite("enable_spring", &b2WheelJointDef::enableSpring)
        .def_readwrite("hertz", &b2WheelJointDef::hertz)
        .def_readwrite("damping_ratio", &b2WheelJointDef::dampingRatio)
        .def_readwrite("enable_limit", &b2WheelJointDef::enableLimit)
        .def_readwrite("lower_translation", &b2WheelJointDef::lowerTranslation)
        .def_readwrite("upper_translation", &b2WheelJointDef::upperTranslation)
        .def_readwrite("enable_motor", &b2WheelJointDef::enableMotor)
        .def_readwrite("max_motor_torque", &b2WheelJointDef::maxMotorTorque)
        .def_readwrite("motor_speed", &b2WheelJointDef::motorSpeed)
        .def_readwrite("internal_value", &b2WheelJointDef::internalValue)
    ;

    _box2d
    .def("default_wheel_joint_def", &b2DefaultWheelJointDef
        , py::return_value_policy::automatic_reference)
    ;

    py::class_<b2ExplosionDef> _ExplosionDef(_box2d, "ExplosionDef");
    registry.on(_box2d, "ExplosionDef", _ExplosionDef);
        _ExplosionDef
        .def_readwrite("mask_bits", &b2ExplosionDef::maskBits)
        .def_readwrite("position", &b2ExplosionDef::position)
        .def_readwrite("radius", &b2ExplosionDef::radius)
        .def_readwrite("falloff", &b2ExplosionDef::falloff)
        .def_readwrite("impulse_per_length", &b2ExplosionDef::impulsePerLength)
    ;

    _box2d
    .def("default_explosion_def", &b2DefaultExplosionDef
        , py::return_value_policy::automatic_reference)
    ;

    py::class_<b2SensorBeginTouchEvent> _SensorBeginTouchEvent(_box2d, "SensorBeginTouchEvent");
    registry.on(_box2d, "SensorBeginTouchEvent", _SensorBeginTouchEvent);
        _SensorBeginTouchEvent
        .def_readwrite("sensor_shape_id", &b2SensorBeginTouchEvent::sensorShapeId)
        .def_readwrite("visitor_shape_id", &b2SensorBeginTouchEvent::visitorShapeId)
    ;

    py::class_<b2SensorEndTouchEvent> _SensorEndTouchEvent(_box2d, "SensorEndTouchEvent");
    registry.on(_box2d, "SensorEndTouchEvent", _SensorEndTouchEvent);
        _SensorEndTouchEvent
        .def_readwrite("sensor_shape_id", &b2SensorEndTouchEvent::sensorShapeId)
        .def_readwrite("visitor_shape_id", &b2SensorEndTouchEvent::visitorShapeId)
    ;

    py::class_<b2SensorEvents> _SensorEvents(_box2d, "SensorEvents");
    registry.on(_box2d, "SensorEvents", _SensorEvents);
        _SensorEvents
        .def_readwrite("begin_events", &b2SensorEvents::beginEvents)
        .def_readwrite("end_events", &b2SensorEvents::endEvents)
        .def_readwrite("begin_count", &b2SensorEvents::beginCount)
        .def_readwrite("end_count", &b2SensorEvents::endCount)
    ;

    py::class_<b2ContactBeginTouchEvent> _ContactBeginTouchEvent(_box2d, "ContactBeginTouchEvent");
    registry.on(_box2d, "ContactBeginTouchEvent", _ContactBeginTouchEvent);
        _ContactBeginTouchEvent
        .def_readwrite("shape_id_a", &b2ContactBeginTouchEvent::shapeIdA)
        .def_readwrite("shape_id_b", &b2ContactBeginTouchEvent::shapeIdB)
        .def_readwrite("contact_id", &b2ContactBeginTouchEvent::contactId)
    ;

    py::class_<b2ContactEndTouchEvent> _ContactEndTouchEvent(_box2d, "ContactEndTouchEvent");
    registry.on(_box2d, "ContactEndTouchEvent", _ContactEndTouchEvent);
        _ContactEndTouchEvent
        .def_readwrite("shape_id_a", &b2ContactEndTouchEvent::shapeIdA)
        .def_readwrite("shape_id_b", &b2ContactEndTouchEvent::shapeIdB)
        .def_readwrite("contact_id", &b2ContactEndTouchEvent::contactId)
    ;

    py::class_<b2ContactHitEvent> _ContactHitEvent(_box2d, "ContactHitEvent");
    registry.on(_box2d, "ContactHitEvent", _ContactHitEvent);
        _ContactHitEvent
        .def_readwrite("shape_id_a", &b2ContactHitEvent::shapeIdA)
        .def_readwrite("shape_id_b", &b2ContactHitEvent::shapeIdB)
        .def_readwrite("contact_id", &b2ContactHitEvent::contactId)
        .def_readwrite("point", &b2ContactHitEvent::point)
        .def_readwrite("normal", &b2ContactHitEvent::normal)
        .def_readwrite("approach_speed", &b2ContactHitEvent::approachSpeed)
    ;

    py::class_<b2ContactEvents> _ContactEvents(_box2d, "ContactEvents");
    registry.on(_box2d, "ContactEvents", _ContactEvents);
        _ContactEvents
        .def_readwrite("begin_events", &b2ContactEvents::beginEvents)
        .def_readwrite("end_events", &b2ContactEvents::endEvents)
        .def_readwrite("hit_events", &b2ContactEvents::hitEvents)
        .def_readwrite("begin_count", &b2ContactEvents::beginCount)
        .def_readwrite("end_count", &b2ContactEvents::endCount)
        .def_readwrite("hit_count", &b2ContactEvents::hitCount)
    ;

    py::class_<b2BodyMoveEvent> _BodyMoveEvent(_box2d, "BodyMoveEvent");
    registry.on(_box2d, "BodyMoveEvent", _BodyMoveEvent);
        _BodyMoveEvent
        .def_readwrite("user_data", &b2BodyMoveEvent::userData)
        .def_readwrite("transform", &b2BodyMoveEvent::transform)
        .def_readwrite("body_id", &b2BodyMoveEvent::bodyId)
        .def_readwrite("fell_asleep", &b2BodyMoveEvent::fellAsleep)
    ;

    py::class_<b2BodyEvents> _BodyEvents(_box2d, "BodyEvents");
    registry.on(_box2d, "BodyEvents", _BodyEvents);
        _BodyEvents
        .def_readwrite("move_events", &b2BodyEvents::moveEvents)
        .def_readwrite("move_count", &b2BodyEvents::moveCount)
    ;

    py::class_<b2JointEvent> _JointEvent(_box2d, "JointEvent");
    registry.on(_box2d, "JointEvent", _JointEvent);
        _JointEvent
        .def_readwrite("joint_id", &b2JointEvent::jointId)
        .def_readwrite("user_data", &b2JointEvent::userData)
    ;

    py::class_<b2JointEvents> _JointEvents(_box2d, "JointEvents");
    registry.on(_box2d, "JointEvents", _JointEvents);
        _JointEvents
        .def_readwrite("joint_events", &b2JointEvents::jointEvents)
        .def_readwrite("count", &b2JointEvents::count)
    ;

    py::class_<b2ContactData> _ContactData(_box2d, "ContactData");
    registry.on(_box2d, "ContactData", _ContactData);
        _ContactData
        .def_readwrite("contact_id", &b2ContactData::contactId)
        .def_readwrite("shape_id_a", &b2ContactData::shapeIdA)
        .def_readwrite("shape_id_b", &b2ContactData::shapeIdB)
        .def_readwrite("manifold", &b2ContactData::manifold)
    ;

    py::enum_<b2HexColor>(_box2d, "HexColor", py::arithmetic())
        .value("COLOR_ALICE_BLUE", b2HexColor::b2_colorAliceBlue)
        .value("COLOR_ANTIQUE_WHITE", b2HexColor::b2_colorAntiqueWhite)
        .value("COLOR_AQUA", b2HexColor::b2_colorAqua)
        .value("COLOR_AQUAMARINE", b2HexColor::b2_colorAquamarine)
        .value("COLOR_AZURE", b2HexColor::b2_colorAzure)
        .value("COLOR_BEIGE", b2HexColor::b2_colorBeige)
        .value("COLOR_BISQUE", b2HexColor::b2_colorBisque)
        .value("COLOR_BLACK", b2HexColor::b2_colorBlack)
        .value("COLOR_BLANCHED_ALMOND", b2HexColor::b2_colorBlanchedAlmond)
        .value("COLOR_BLUE", b2HexColor::b2_colorBlue)
        .value("COLOR_BLUE_VIOLET", b2HexColor::b2_colorBlueViolet)
        .value("COLOR_BROWN", b2HexColor::b2_colorBrown)
        .value("COLOR_BURLYWOOD", b2HexColor::b2_colorBurlywood)
        .value("COLOR_CADET_BLUE", b2HexColor::b2_colorCadetBlue)
        .value("COLOR_CHARTREUSE", b2HexColor::b2_colorChartreuse)
        .value("COLOR_CHOCOLATE", b2HexColor::b2_colorChocolate)
        .value("COLOR_CORAL", b2HexColor::b2_colorCoral)
        .value("COLOR_CORNFLOWER_BLUE", b2HexColor::b2_colorCornflowerBlue)
        .value("COLOR_CORNSILK", b2HexColor::b2_colorCornsilk)
        .value("COLOR_CRIMSON", b2HexColor::b2_colorCrimson)
        .value("COLOR_CYAN", b2HexColor::b2_colorCyan)
        .value("COLOR_DARK_BLUE", b2HexColor::b2_colorDarkBlue)
        .value("COLOR_DARK_CYAN", b2HexColor::b2_colorDarkCyan)
        .value("COLOR_DARK_GOLDEN_ROD", b2HexColor::b2_colorDarkGoldenRod)
        .value("COLOR_DARK_GRAY", b2HexColor::b2_colorDarkGray)
        .value("COLOR_DARK_GREEN", b2HexColor::b2_colorDarkGreen)
        .value("COLOR_DARK_KHAKI", b2HexColor::b2_colorDarkKhaki)
        .value("COLOR_DARK_MAGENTA", b2HexColor::b2_colorDarkMagenta)
        .value("COLOR_DARK_OLIVE_GREEN", b2HexColor::b2_colorDarkOliveGreen)
        .value("COLOR_DARK_ORANGE", b2HexColor::b2_colorDarkOrange)
        .value("COLOR_DARK_ORCHID", b2HexColor::b2_colorDarkOrchid)
        .value("COLOR_DARK_RED", b2HexColor::b2_colorDarkRed)
        .value("COLOR_DARK_SALMON", b2HexColor::b2_colorDarkSalmon)
        .value("COLOR_DARK_SEA_GREEN", b2HexColor::b2_colorDarkSeaGreen)
        .value("COLOR_DARK_SLATE_BLUE", b2HexColor::b2_colorDarkSlateBlue)
        .value("COLOR_DARK_SLATE_GRAY", b2HexColor::b2_colorDarkSlateGray)
        .value("COLOR_DARK_TURQUOISE", b2HexColor::b2_colorDarkTurquoise)
        .value("COLOR_DARK_VIOLET", b2HexColor::b2_colorDarkViolet)
        .value("COLOR_DEEP_PINK", b2HexColor::b2_colorDeepPink)
        .value("COLOR_DEEP_SKY_BLUE", b2HexColor::b2_colorDeepSkyBlue)
        .value("COLOR_DIM_GRAY", b2HexColor::b2_colorDimGray)
        .value("COLOR_DODGER_BLUE", b2HexColor::b2_colorDodgerBlue)
        .value("COLOR_FIRE_BRICK", b2HexColor::b2_colorFireBrick)
        .value("COLOR_FLORAL_WHITE", b2HexColor::b2_colorFloralWhite)
        .value("COLOR_FOREST_GREEN", b2HexColor::b2_colorForestGreen)
        .value("COLOR_FUCHSIA", b2HexColor::b2_colorFuchsia)
        .value("COLOR_GAINSBORO", b2HexColor::b2_colorGainsboro)
        .value("COLOR_GHOST_WHITE", b2HexColor::b2_colorGhostWhite)
        .value("COLOR_GOLD", b2HexColor::b2_colorGold)
        .value("COLOR_GOLDEN_ROD", b2HexColor::b2_colorGoldenRod)
        .value("COLOR_GRAY", b2HexColor::b2_colorGray)
        .value("COLOR_GREEN", b2HexColor::b2_colorGreen)
        .value("COLOR_GREEN_YELLOW", b2HexColor::b2_colorGreenYellow)
        .value("COLOR_HONEY_DEW", b2HexColor::b2_colorHoneyDew)
        .value("COLOR_HOT_PINK", b2HexColor::b2_colorHotPink)
        .value("COLOR_INDIAN_RED", b2HexColor::b2_colorIndianRed)
        .value("COLOR_INDIGO", b2HexColor::b2_colorIndigo)
        .value("COLOR_IVORY", b2HexColor::b2_colorIvory)
        .value("COLOR_KHAKI", b2HexColor::b2_colorKhaki)
        .value("COLOR_LAVENDER", b2HexColor::b2_colorLavender)
        .value("COLOR_LAVENDER_BLUSH", b2HexColor::b2_colorLavenderBlush)
        .value("COLOR_LAWN_GREEN", b2HexColor::b2_colorLawnGreen)
        .value("COLOR_LEMON_CHIFFON", b2HexColor::b2_colorLemonChiffon)
        .value("COLOR_LIGHT_BLUE", b2HexColor::b2_colorLightBlue)
        .value("COLOR_LIGHT_CORAL", b2HexColor::b2_colorLightCoral)
        .value("COLOR_LIGHT_CYAN", b2HexColor::b2_colorLightCyan)
        .value("COLOR_LIGHT_GOLDEN_ROD_YELLOW", b2HexColor::b2_colorLightGoldenRodYellow)
        .value("COLOR_LIGHT_GRAY", b2HexColor::b2_colorLightGray)
        .value("COLOR_LIGHT_GREEN", b2HexColor::b2_colorLightGreen)
        .value("COLOR_LIGHT_PINK", b2HexColor::b2_colorLightPink)
        .value("COLOR_LIGHT_SALMON", b2HexColor::b2_colorLightSalmon)
        .value("COLOR_LIGHT_SEA_GREEN", b2HexColor::b2_colorLightSeaGreen)
        .value("COLOR_LIGHT_SKY_BLUE", b2HexColor::b2_colorLightSkyBlue)
        .value("COLOR_LIGHT_SLATE_GRAY", b2HexColor::b2_colorLightSlateGray)
        .value("COLOR_LIGHT_STEEL_BLUE", b2HexColor::b2_colorLightSteelBlue)
        .value("COLOR_LIGHT_YELLOW", b2HexColor::b2_colorLightYellow)
        .value("COLOR_LIME", b2HexColor::b2_colorLime)
        .value("COLOR_LIME_GREEN", b2HexColor::b2_colorLimeGreen)
        .value("COLOR_LINEN", b2HexColor::b2_colorLinen)
        .value("COLOR_MAGENTA", b2HexColor::b2_colorMagenta)
        .value("COLOR_MAROON", b2HexColor::b2_colorMaroon)
        .value("COLOR_MEDIUM_AQUA_MARINE", b2HexColor::b2_colorMediumAquaMarine)
        .value("COLOR_MEDIUM_BLUE", b2HexColor::b2_colorMediumBlue)
        .value("COLOR_MEDIUM_ORCHID", b2HexColor::b2_colorMediumOrchid)
        .value("COLOR_MEDIUM_PURPLE", b2HexColor::b2_colorMediumPurple)
        .value("COLOR_MEDIUM_SEA_GREEN", b2HexColor::b2_colorMediumSeaGreen)
        .value("COLOR_MEDIUM_SLATE_BLUE", b2HexColor::b2_colorMediumSlateBlue)
        .value("COLOR_MEDIUM_SPRING_GREEN", b2HexColor::b2_colorMediumSpringGreen)
        .value("COLOR_MEDIUM_TURQUOISE", b2HexColor::b2_colorMediumTurquoise)
        .value("COLOR_MEDIUM_VIOLET_RED", b2HexColor::b2_colorMediumVioletRed)
        .value("COLOR_MIDNIGHT_BLUE", b2HexColor::b2_colorMidnightBlue)
        .value("COLOR_MINT_CREAM", b2HexColor::b2_colorMintCream)
        .value("COLOR_MISTY_ROSE", b2HexColor::b2_colorMistyRose)
        .value("COLOR_MOCCASIN", b2HexColor::b2_colorMoccasin)
        .value("COLOR_NAVAJO_WHITE", b2HexColor::b2_colorNavajoWhite)
        .value("COLOR_NAVY", b2HexColor::b2_colorNavy)
        .value("COLOR_OLD_LACE", b2HexColor::b2_colorOldLace)
        .value("COLOR_OLIVE", b2HexColor::b2_colorOlive)
        .value("COLOR_OLIVE_DRAB", b2HexColor::b2_colorOliveDrab)
        .value("COLOR_ORANGE", b2HexColor::b2_colorOrange)
        .value("COLOR_ORANGE_RED", b2HexColor::b2_colorOrangeRed)
        .value("COLOR_ORCHID", b2HexColor::b2_colorOrchid)
        .value("COLOR_PALE_GOLDEN_ROD", b2HexColor::b2_colorPaleGoldenRod)
        .value("COLOR_PALE_GREEN", b2HexColor::b2_colorPaleGreen)
        .value("COLOR_PALE_TURQUOISE", b2HexColor::b2_colorPaleTurquoise)
        .value("COLOR_PALE_VIOLET_RED", b2HexColor::b2_colorPaleVioletRed)
        .value("COLOR_PAPAYA_WHIP", b2HexColor::b2_colorPapayaWhip)
        .value("COLOR_PEACH_PUFF", b2HexColor::b2_colorPeachPuff)
        .value("COLOR_PERU", b2HexColor::b2_colorPeru)
        .value("COLOR_PINK", b2HexColor::b2_colorPink)
        .value("COLOR_PLUM", b2HexColor::b2_colorPlum)
        .value("COLOR_POWDER_BLUE", b2HexColor::b2_colorPowderBlue)
        .value("COLOR_PURPLE", b2HexColor::b2_colorPurple)
        .value("COLOR_REBECCA_PURPLE", b2HexColor::b2_colorRebeccaPurple)
        .value("COLOR_RED", b2HexColor::b2_colorRed)
        .value("COLOR_ROSY_BROWN", b2HexColor::b2_colorRosyBrown)
        .value("COLOR_ROYAL_BLUE", b2HexColor::b2_colorRoyalBlue)
        .value("COLOR_SADDLE_BROWN", b2HexColor::b2_colorSaddleBrown)
        .value("COLOR_SALMON", b2HexColor::b2_colorSalmon)
        .value("COLOR_SANDY_BROWN", b2HexColor::b2_colorSandyBrown)
        .value("COLOR_SEA_GREEN", b2HexColor::b2_colorSeaGreen)
        .value("COLOR_SEA_SHELL", b2HexColor::b2_colorSeaShell)
        .value("COLOR_SIENNA", b2HexColor::b2_colorSienna)
        .value("COLOR_SILVER", b2HexColor::b2_colorSilver)
        .value("COLOR_SKY_BLUE", b2HexColor::b2_colorSkyBlue)
        .value("COLOR_SLATE_BLUE", b2HexColor::b2_colorSlateBlue)
        .value("COLOR_SLATE_GRAY", b2HexColor::b2_colorSlateGray)
        .value("COLOR_SNOW", b2HexColor::b2_colorSnow)
        .value("COLOR_SPRING_GREEN", b2HexColor::b2_colorSpringGreen)
        .value("COLOR_STEEL_BLUE", b2HexColor::b2_colorSteelBlue)
        .value("COLOR_TAN", b2HexColor::b2_colorTan)
        .value("COLOR_TEAL", b2HexColor::b2_colorTeal)
        .value("COLOR_THISTLE", b2HexColor::b2_colorThistle)
        .value("COLOR_TOMATO", b2HexColor::b2_colorTomato)
        .value("COLOR_TURQUOISE", b2HexColor::b2_colorTurquoise)
        .value("COLOR_VIOLET", b2HexColor::b2_colorViolet)
        .value("COLOR_WHEAT", b2HexColor::b2_colorWheat)
        .value("COLOR_WHITE", b2HexColor::b2_colorWhite)
        .value("COLOR_WHITE_SMOKE", b2HexColor::b2_colorWhiteSmoke)
        .value("COLOR_YELLOW", b2HexColor::b2_colorYellow)
        .value("COLOR_YELLOW_GREEN", b2HexColor::b2_colorYellowGreen)
        .value("COLOR_BOX2_D_RED", b2HexColor::b2_colorBox2DRed)
        .value("COLOR_BOX2_D_BLUE", b2HexColor::b2_colorBox2DBlue)
        .value("COLOR_BOX2_D_GREEN", b2HexColor::b2_colorBox2DGreen)
        .value("COLOR_BOX2_D_YELLOW", b2HexColor::b2_colorBox2DYellow)
        .export_values()
    ;
    _box2d
    .def("default_debug_draw", &b2DefaultDebugDraw
        , py::return_value_policy::automatic_reference)
    ;


}