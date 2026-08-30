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

#include "id_internal.h"


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

b2ChainId CreateChainFromPoints(
    b2BodyId body,
    const b2ChainDef& base_def,
    const std::vector<b2Vec2>& points,
    const std::vector<b2SurfaceMaterial>& materials = {})
{
    b2ChainDef def = base_def;
    def.points = points.data();
    def.count = static_cast<int32_t>(points.size());

    b2SurfaceMaterial fallback;
    if (materials.empty()) {
        fallback = b2DefaultSurfaceMaterial();
        def.materials = &fallback;
        def.materialCount = 1;
    } else {
        def.materials = materials.data();
        def.materialCount = static_cast<int32_t>(materials.size());
    }
    return b2CreateChain(body, &def);
}

void init_id_py(py::module &_box2d, Registry &registry) {
    PYEXTEND_BEGIN(b2BodyId, Body)
    _Body.def("destroy", &DestroyBody)
    .def("create_chain_from_points", &CreateChainFromPoints,
        py::arg("base_def"),
        py::arg("points"),
        py::arg("materials") = std::vector<b2SurfaceMaterial>{})
    ;
    PYEXTEND_END

    PYEXTEND_BEGIN(b2ShapeId, Shape)
    _Shape.def("destroy", &DestroyShape, py::arg("update_body_mass"))
    ;
    PYEXTEND_END
}

/*
b2ChainId CreateChainFromPoints(
    b2BodyId body,
    const b2ChainDef& base_def,   // everything except points/count
    const std::vector<b2Vec2>& points)
{
    b2ChainDef def = base_def;
    def.points = points.data();
    def.count = static_cast<int32_t>(points.size());
    return b2CreateChain(body, &def);
}

void init_id_py(py::module &_box2d, Registry &registry) {
    PYEXTEND_BEGIN(b2BodyId, Body)
    _Body.def("destroy", &DestroyBody)
         .def("create_chain_from_points", &CreateChainFromPoints, py::arg("base_def"), py::arg("points"))
    ;
    PYEXTEND_END

    PYEXTEND_BEGIN(b2ShapeId, Shape)
    _Shape.def("destroy", &DestroyShape, py::arg("update_body_mass"))
    ;
    PYEXTEND_END
}
*/