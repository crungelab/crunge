#include <pybind11/pybind11.h>

namespace py = pybind11;

// void b2Body_SetUserData( b2BodyId bodyId, void* userData )

class PyHolder
{
public:
    py::object obj;
    explicit PyHolder(py::object o) : obj(std::move(o)) {}
};

void Body_SetUserData(b2BodyId bodyId, py::object userData)
{
    // Clean up any previously stored PyHolder to avoid memory leaks
    auto* existing = static_cast<PyHolder*>(b2Body_GetUserData(bodyId));
    delete existing;

    b2Body_SetUserData(bodyId, new PyHolder(std::move(userData)));
}

py::object Body_GetUserData(b2BodyId bodyId)
{
    auto* holder = static_cast<PyHolder*>(b2Body_GetUserData(bodyId));
    if (holder == nullptr)
        return py::none();

    return holder->obj;
}