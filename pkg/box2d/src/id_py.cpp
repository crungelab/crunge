#include <limits>
// #include <iostream>

#include <pybind11/functional.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <cxbind/callback.h>
#include <cxbind/cxbind.h>

#include <crunge/box2d/conversions.h>
#include <crunge/box2d/crunge-box2d.h>

#include <box2d/box2d.h>

#include "box2d_internal.h"


namespace py = pybind11;

void DestroyBody(b2BodyId bodyId) {
    auto* userData = static_cast<PyHolder*>(b2Body_GetUserData(bodyId));
    delete userData;
    b2DestroyBody(bodyId);
}

void DestroyShape(b2ShapeId shapeId, bool updateBodyMass) {
    auto* userData = static_cast<PyHolder*>(b2Shape_GetUserData(shapeId));
    delete userData;
    b2DestroyShape(shapeId, updateBodyMass);
}

void init_id_py(py::module &_box2d, Registry &registry) {
    PYEXTEND_BEGIN(b2BodyId, Body)
    _Body.def("destroy", &DestroyBody)
    ;
    PYEXTEND_END

    PYEXTEND_BEGIN(b2ShapeId, Shape)
    _Shape.def("destroy", &DestroyShape, py::arg("update_body_mass"))
    ;
    PYEXTEND_END
}