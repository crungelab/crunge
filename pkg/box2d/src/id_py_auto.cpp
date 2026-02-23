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

namespace py = pybind11;

void init_id_py_auto(py::module &_box2d, Registry &registry) {
    py::class_<b2WorldId> _World(_box2d, "World");
    registry.on(_box2d, "World", _World);
        _World
        .def_readwrite("index1", &b2WorldId::index1)
        .def_readwrite("generation", &b2WorldId::generation)
        .def("create_body", &b2CreateBody)
    ;

    py::class_<b2BodyId> _BodyId(_box2d, "BodyId");
    registry.on(_box2d, "BodyId", _BodyId);
        _BodyId
        .def_readwrite("index1", &b2BodyId::index1)
        .def_readwrite("world0", &b2BodyId::world0)
        .def_readwrite("generation", &b2BodyId::generation)
    ;

    py::class_<b2ShapeId> _ShapeId(_box2d, "ShapeId");
    registry.on(_box2d, "ShapeId", _ShapeId);
        _ShapeId
        .def_readwrite("index1", &b2ShapeId::index1)
        .def_readwrite("world0", &b2ShapeId::world0)
        .def_readwrite("generation", &b2ShapeId::generation)
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