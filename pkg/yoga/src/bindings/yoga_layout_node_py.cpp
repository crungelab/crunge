#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/yoga/crunge-yoga.h>
#include <crunge/yoga/conversions.h>

#include <yoga/node/Node.h>
#include "../LayoutNode.h"

namespace py = pybind11;

//using namespace facebook::yoga;

void init_yoga_layout_node_py(py::module &_yoga, Registry &registry) {
    PYEXTEND_BEGIN(LayoutNode, LayoutNode)

    _LayoutNode.def(py::init<>(&LayoutNode::createDefault));
    //_LayoutNode.def(py::init<Config *>(), LayoutNode::createWithConfig, py::arg("config"), py::return_value_policy::take_ownership);

    _LayoutNode.def("set_style", [](LayoutNode& self, facebook::yoga::Style& style) {
        auto node = static_cast<facebook::yoga::Node*>(self.m_node);
        if (!node) {
            throw std::runtime_error("LayoutNode is not initialized.");
        }
        //self.m_node->setStyle(style);
        node->setStyle(style);
        node->markDirtyAndPropagate();
    }, py::arg("style"));

    _LayoutNode.def("get_style", [](LayoutNode& self) -> facebook::yoga::Style& {
        auto node = static_cast<facebook::yoga::Node*>(self.m_node);
        if (!node) {
            throw std::runtime_error("LayoutNode is not initialized.");
        }
        return node->style();
    });

    _LayoutNode.def("set_config", [](LayoutNode& self, Config* config) {
        auto node = static_cast<facebook::yoga::Node*>(self.m_node);
        if (!node) {
            throw std::runtime_error("LayoutNode is not initialized.");
        }
        //node->setConfig(config->getConfig());
        node->setConfig(static_cast<facebook::yoga::Config*>(config->getConfigRef()));
    }, py::arg("config"), py::keep_alive<1, 2>());

    PYEXTEND_END

    /*
    PYEXTEND_BEGIN(LayoutNode, LayoutNode)
    _LayoutNode.def("insert_child", [](LayoutNode& self, LayoutNode& child, size_t index)
    {
        child.setOwner(&self);
        self.insertChild(&child, index);
        self.markDirtyAndPropagate();
    }, py::arg("child"), py::arg("index"));

    _LayoutNode.def("add_child", [](LayoutNode& self, LayoutNode& child)
    {
        child.setOwner(&self);
        self.insertChild(&child, self.getChildCount());
        self.markDirtyAndPropagate();
    }, py::arg("child"));
    PYEXTEND_END
    */
}