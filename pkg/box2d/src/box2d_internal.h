#include <pybind11/pybind11.h>

#include "debug_draw_py.h"

namespace py = pybind11;

class PyHolder
{
public:
    py::object obj;
    explicit PyHolder(py::object o) : obj(std::move(o)) {}
};

static void World_Draw(b2WorldId worldId, PyDebugDrawBase& dbg)
{
    // IMPORTANT: dbg must outlive this call (it does because Python owns dbg).
    // The thunks acquire the GIL, so this is safe as long as you're calling
    // b2World_Draw from Python while the interpreter is alive.
    b2World_Draw(worldId, dbg.ptr());
}

static void Body_SetUserData(b2BodyId bodyId, py::object userData)
{
    // Clean up any previously stored PyHolder to avoid memory leaks
    auto* existing = static_cast<PyHolder*>(b2Body_GetUserData(bodyId));
    delete existing;

    b2Body_SetUserData(bodyId, new PyHolder(std::move(userData)));
}

static py::object Body_GetUserData(b2BodyId bodyId)
{
    auto* holder = static_cast<PyHolder*>(b2Body_GetUserData(bodyId));
    if (holder == nullptr)
        return py::none();

    return holder->obj;
}

static float Body_GetAngle(b2BodyId bodyId)
{
    //return b2Body_GetAngle(bodyId);
    auto rotation = b2Body_GetRotation(bodyId);
    auto angle = b2Rot_GetAngle(rotation);
    return angle;
}

static void Shape_SetUserData(b2ShapeId shapeId, py::object userData)
{
    // Clean up any previously stored PyHolder to avoid memory leaks
    auto* existing = static_cast<PyHolder*>(b2Shape_GetUserData(shapeId));
    delete existing;

    b2Shape_SetUserData(shapeId, new PyHolder(std::move(userData)));
}

static py::object Shape_GetUserData(b2ShapeId shapeId)
{
    auto* holder = static_cast<PyHolder*>(b2Shape_GetUserData(shapeId));
    if (holder == nullptr)
        return py::none();

    return holder->obj;
}
