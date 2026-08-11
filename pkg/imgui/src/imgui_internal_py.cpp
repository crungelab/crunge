#include <filesystem>
#include <limits>

#include <pybind11/functional.h>
#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>

#define BUILDING_DLL

#include "imgui.h"
#include "imgui_internal.h"

#include <cxbind/cxbind.h>

#include <crunge/imgui/conversions.h>
#include <crunge/imgui/crunge-imgui.h>

namespace py = pybind11;

void init_imgui_internal_py(py::module &m, Registry &registry) {

    // in your existing imgui module init, after the public bindings
    auto internal = m.def_submodule("internal");

    py::class_<ImGuiDockNode>(internal, "DockNode")
        .def_readonly("id", &ImGuiDockNode::ID)
        .def_readonly("pos", &ImGuiDockNode::Pos)
        .def_readonly("size", &ImGuiDockNode::Size)
        .def("is_root_node", &ImGuiDockNode::IsRootNode)
        .def("is_split_node", &ImGuiDockNode::IsSplitNode)
        .def("is_leaf_node", &ImGuiDockNode::IsLeafNode)
        .def("is_central_node", &ImGuiDockNode::IsCentralNode)
        .def("is_empty", &ImGuiDockNode::IsEmpty);

    // private flags live in ImGuiDockNodeFlagsPrivate_ — expose only what you
    // need

    py::enum_<ImGuiDockNodeFlagsPrivate_>(internal, "DockNodeFlags", py::arithmetic())
        //.value("NONE", ImGuiDockNodeFlags_None)
        //.value("DOCK_SPACE", (ImGuiDockNodeFlags_)ImGuiDockNodeFlags_DockSpace)
        .value("DOCK_SPACE", ImGuiDockNodeFlags_DockSpace)
        .export_values();

    internal.def("dock_builder_dock_window", &ImGui::DockBuilderDockWindow,
                 py::arg("window_name"), py::arg("node_id"));

    internal.def("dock_builder_get_node", &ImGui::DockBuilderGetNode,
                 py::arg("node_id"), py::return_value_policy::reference);

    internal.def("dock_builder_get_central_node",
                 &ImGui::DockBuilderGetCentralNode, py::arg("node_id"),
                 py::return_value_policy::reference);

    internal.def("dock_builder_add_node", &ImGui::DockBuilderAddNode,
                 py::arg("node_id") = 0, py::arg("flags") = 0);

    internal.def("dock_builder_remove_node", &ImGui::DockBuilderRemoveNode,
                 py::arg("node_id"));

    internal.def("dock_builder_remove_node_docked_windows",
                 &ImGui::DockBuilderRemoveNodeDockedWindows, py::arg("node_id"),
                 py::arg("clear_settings_refs") = true);

    internal.def("dock_builder_remove_node_child_nodes",
                 &ImGui::DockBuilderRemoveNodeChildNodes, py::arg("node_id"));

    internal.def("dock_builder_set_node_pos", &ImGui::DockBuilderSetNodePos,
                 py::arg("node_id"), py::arg("pos"));

    internal.def("dock_builder_set_node_size", &ImGui::DockBuilderSetNodeSize,
                 py::arg("node_id"), py::arg("size"));

    internal.def(
        "dock_builder_split_node",
        [](ImGuiID node_id, ImGuiDir dir, float ratio) {
            ImGuiID at_dir = 0, at_opposite = 0;
            ImGui::DockBuilderSplitNode(node_id, dir, ratio, &at_dir,
                                        &at_opposite);
            return std::make_pair(at_dir, at_opposite);
        },
        py::arg("node_id"), py::arg("split_dir"),
        py::arg("size_ratio_for_node_at_dir"));

    internal.def("dock_builder_finish", &ImGui::DockBuilderFinish,
                 py::arg("node_id"));
}
