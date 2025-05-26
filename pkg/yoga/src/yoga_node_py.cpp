#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/yoga/crunge-yoga.h>
#include <crunge/yoga/conversions.h>

#include <yoga/node/Node.h>

namespace py = pybind11;

using namespace facebook::yoga;

void init_yoga_node_py(py::module &_yoga, Registry &registry) {
    PYEXTEND_BEGIN(Node, Node)
    _Node.def("insert_child", [](Node& self, Node& child, size_t index)
    {
        child.setOwner(&self);
        self.insertChild(&child, index);
        self.markDirtyAndPropagate();
    }, py::arg("child"), py::arg("index"));

    _Node.def("add_child", [](Node& self, Node& child)
    {
        child.setOwner(&self);
        self.insertChild(&child, self.getChildCount());
        self.markDirtyAndPropagate();
    }, py::arg("child"));
    PYEXTEND_END
}