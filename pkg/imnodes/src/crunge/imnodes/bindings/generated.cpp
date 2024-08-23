#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include "imgui.h"
#include "imgui_internal.h"

#include <crunge/imgui/crunge-imgui.h>
#include <crunge/imgui/conversions.h>
#include <cxbind/cxbind.h>

#include "imnodes.h"
#include "imnodes_internal.h"

namespace py = pybind11;

void init_generated(py::module &_imnodes, Registry &registry) {
    py::enum_<ImNodesCol_>(_imnodes, "Col", py::arithmetic())
        .value("COL_NODE_BACKGROUND", ImNodesCol_::ImNodesCol_NodeBackground)
        .value("COL_NODE_BACKGROUND_HOVERED", ImNodesCol_::ImNodesCol_NodeBackgroundHovered)
        .value("COL_NODE_BACKGROUND_SELECTED", ImNodesCol_::ImNodesCol_NodeBackgroundSelected)
        .value("COL_NODE_OUTLINE", ImNodesCol_::ImNodesCol_NodeOutline)
        .value("COL_TITLE_BAR", ImNodesCol_::ImNodesCol_TitleBar)
        .value("COL_TITLE_BAR_HOVERED", ImNodesCol_::ImNodesCol_TitleBarHovered)
        .value("COL_TITLE_BAR_SELECTED", ImNodesCol_::ImNodesCol_TitleBarSelected)
        .value("COL_LINK", ImNodesCol_::ImNodesCol_Link)
        .value("COL_LINK_HOVERED", ImNodesCol_::ImNodesCol_LinkHovered)
        .value("COL_LINK_SELECTED", ImNodesCol_::ImNodesCol_LinkSelected)
        .value("COL_PIN", ImNodesCol_::ImNodesCol_Pin)
        .value("COL_PIN_HOVERED", ImNodesCol_::ImNodesCol_PinHovered)
        .value("COL_BOX_SELECTOR", ImNodesCol_::ImNodesCol_BoxSelector)
        .value("COL_BOX_SELECTOR_OUTLINE", ImNodesCol_::ImNodesCol_BoxSelectorOutline)
        .value("COL_GRID_BACKGROUND", ImNodesCol_::ImNodesCol_GridBackground)
        .value("COL_GRID_LINE", ImNodesCol_::ImNodesCol_GridLine)
        .value("COL_GRID_LINE_PRIMARY", ImNodesCol_::ImNodesCol_GridLinePrimary)
        .value("COL_MINI_MAP_BACKGROUND", ImNodesCol_::ImNodesCol_MiniMapBackground)
        .value("COL_MINI_MAP_BACKGROUND_HOVERED", ImNodesCol_::ImNodesCol_MiniMapBackgroundHovered)
        .value("COL_MINI_MAP_OUTLINE", ImNodesCol_::ImNodesCol_MiniMapOutline)
        .value("COL_MINI_MAP_OUTLINE_HOVERED", ImNodesCol_::ImNodesCol_MiniMapOutlineHovered)
        .value("COL_MINI_MAP_NODE_BACKGROUND", ImNodesCol_::ImNodesCol_MiniMapNodeBackground)
        .value("COL_MINI_MAP_NODE_BACKGROUND_HOVERED", ImNodesCol_::ImNodesCol_MiniMapNodeBackgroundHovered)
        .value("COL_MINI_MAP_NODE_BACKGROUND_SELECTED", ImNodesCol_::ImNodesCol_MiniMapNodeBackgroundSelected)
        .value("COL_MINI_MAP_NODE_OUTLINE", ImNodesCol_::ImNodesCol_MiniMapNodeOutline)
        .value("COL_MINI_MAP_LINK", ImNodesCol_::ImNodesCol_MiniMapLink)
        .value("COL_MINI_MAP_LINK_SELECTED", ImNodesCol_::ImNodesCol_MiniMapLinkSelected)
        .value("COL_MINI_MAP_CANVAS", ImNodesCol_::ImNodesCol_MiniMapCanvas)
        .value("COL_MINI_MAP_CANVAS_OUTLINE", ImNodesCol_::ImNodesCol_MiniMapCanvasOutline)
        .value("COL_COUNT", ImNodesCol_::ImNodesCol_COUNT)
        .export_values();

    py::enum_<ImNodesStyleVar_>(_imnodes, "StyleVar", py::arithmetic())
        .value("STYLE_VAR_GRID_SPACING", ImNodesStyleVar_::ImNodesStyleVar_GridSpacing)
        .value("STYLE_VAR_NODE_CORNER_ROUNDING", ImNodesStyleVar_::ImNodesStyleVar_NodeCornerRounding)
        .value("STYLE_VAR_NODE_PADDING", ImNodesStyleVar_::ImNodesStyleVar_NodePadding)
        .value("STYLE_VAR_NODE_BORDER_THICKNESS", ImNodesStyleVar_::ImNodesStyleVar_NodeBorderThickness)
        .value("STYLE_VAR_LINK_THICKNESS", ImNodesStyleVar_::ImNodesStyleVar_LinkThickness)
        .value("STYLE_VAR_LINK_LINE_SEGMENTS_PER_LENGTH", ImNodesStyleVar_::ImNodesStyleVar_LinkLineSegmentsPerLength)
        .value("STYLE_VAR_LINK_HOVER_DISTANCE", ImNodesStyleVar_::ImNodesStyleVar_LinkHoverDistance)
        .value("STYLE_VAR_PIN_CIRCLE_RADIUS", ImNodesStyleVar_::ImNodesStyleVar_PinCircleRadius)
        .value("STYLE_VAR_PIN_QUAD_SIDE_LENGTH", ImNodesStyleVar_::ImNodesStyleVar_PinQuadSideLength)
        .value("STYLE_VAR_PIN_TRIANGLE_SIDE_LENGTH", ImNodesStyleVar_::ImNodesStyleVar_PinTriangleSideLength)
        .value("STYLE_VAR_PIN_LINE_THICKNESS", ImNodesStyleVar_::ImNodesStyleVar_PinLineThickness)
        .value("STYLE_VAR_PIN_HOVER_RADIUS", ImNodesStyleVar_::ImNodesStyleVar_PinHoverRadius)
        .value("STYLE_VAR_PIN_OFFSET", ImNodesStyleVar_::ImNodesStyleVar_PinOffset)
        .value("STYLE_VAR_MINI_MAP_PADDING", ImNodesStyleVar_::ImNodesStyleVar_MiniMapPadding)
        .value("STYLE_VAR_MINI_MAP_OFFSET", ImNodesStyleVar_::ImNodesStyleVar_MiniMapOffset)
        .value("STYLE_VAR_COUNT", ImNodesStyleVar_::ImNodesStyleVar_COUNT)
        .export_values();

    py::enum_<ImNodesStyleFlags_>(_imnodes, "StyleFlags", py::arithmetic())
        .value("STYLE_FLAGS_NONE", ImNodesStyleFlags_::ImNodesStyleFlags_None)
        .value("STYLE_FLAGS_NODE_OUTLINE", ImNodesStyleFlags_::ImNodesStyleFlags_NodeOutline)
        .value("STYLE_FLAGS_GRID_LINES", ImNodesStyleFlags_::ImNodesStyleFlags_GridLines)
        .value("STYLE_FLAGS_GRID_LINES_PRIMARY", ImNodesStyleFlags_::ImNodesStyleFlags_GridLinesPrimary)
        .value("STYLE_FLAGS_GRID_SNAPPING", ImNodesStyleFlags_::ImNodesStyleFlags_GridSnapping)
        .export_values();

    py::enum_<ImNodesPinShape_>(_imnodes, "PinShape", py::arithmetic())
        .value("PIN_SHAPE_CIRCLE", ImNodesPinShape_::ImNodesPinShape_Circle)
        .value("PIN_SHAPE_CIRCLE_FILLED", ImNodesPinShape_::ImNodesPinShape_CircleFilled)
        .value("PIN_SHAPE_TRIANGLE", ImNodesPinShape_::ImNodesPinShape_Triangle)
        .value("PIN_SHAPE_TRIANGLE_FILLED", ImNodesPinShape_::ImNodesPinShape_TriangleFilled)
        .value("PIN_SHAPE_QUAD", ImNodesPinShape_::ImNodesPinShape_Quad)
        .value("PIN_SHAPE_QUAD_FILLED", ImNodesPinShape_::ImNodesPinShape_QuadFilled)
        .export_values();

    py::enum_<ImNodesAttributeFlags_>(_imnodes, "AttributeFlags", py::arithmetic())
        .value("ATTRIBUTE_FLAGS_NONE", ImNodesAttributeFlags_::ImNodesAttributeFlags_None)
        .value("ATTRIBUTE_FLAGS_ENABLE_LINK_DETACH_WITH_DRAG_CLICK", ImNodesAttributeFlags_::ImNodesAttributeFlags_EnableLinkDetachWithDragClick)
        .value("ATTRIBUTE_FLAGS_ENABLE_LINK_CREATION_ON_SNAP", ImNodesAttributeFlags_::ImNodesAttributeFlags_EnableLinkCreationOnSnap)
        .export_values();

    PYCLASS_BEGIN(_imnodes, ImNodesIO, IO)
        IO.def_readwrite("alt_mouse_button", &ImNodesIO::AltMouseButton);
        IO.def_readwrite("auto_panning_speed", &ImNodesIO::AutoPanningSpeed);
        IO.def(py::init<>());
    PYCLASS_END(_imnodes, ImNodesIO, IO)

    PYCLASS_BEGIN(_imnodes, ImNodesStyle, Style)
        Style.def_readwrite("grid_spacing", &ImNodesStyle::GridSpacing);
        Style.def_readwrite("node_corner_rounding", &ImNodesStyle::NodeCornerRounding);
        Style.def_readwrite("node_padding", &ImNodesStyle::NodePadding);
        Style.def_readwrite("node_border_thickness", &ImNodesStyle::NodeBorderThickness);
        Style.def_readwrite("link_thickness", &ImNodesStyle::LinkThickness);
        Style.def_readwrite("link_line_segments_per_length", &ImNodesStyle::LinkLineSegmentsPerLength);
        Style.def_readwrite("link_hover_distance", &ImNodesStyle::LinkHoverDistance);
        Style.def_readwrite("pin_circle_radius", &ImNodesStyle::PinCircleRadius);
        Style.def_readwrite("pin_quad_side_length", &ImNodesStyle::PinQuadSideLength);
        Style.def_readwrite("pin_triangle_side_length", &ImNodesStyle::PinTriangleSideLength);
        Style.def_readwrite("pin_line_thickness", &ImNodesStyle::PinLineThickness);
        Style.def_readwrite("pin_hover_radius", &ImNodesStyle::PinHoverRadius);
        Style.def_readwrite("pin_offset", &ImNodesStyle::PinOffset);
        Style.def_readwrite("mini_map_padding", &ImNodesStyle::MiniMapPadding);
        Style.def_readwrite("mini_map_offset", &ImNodesStyle::MiniMapOffset);
        Style.def_readwrite("flags", &ImNodesStyle::Flags);
        Style.def_readonly("colors", &ImNodesStyle::Colors);
        Style.def(py::init<>());
    PYCLASS_END(_imnodes, ImNodesStyle, Style)

    py::enum_<ImNodesMiniMapLocation_>(_imnodes, "MiniMapLocation", py::arithmetic())
        .value("MINI_MAP_LOCATION_BOTTOM_LEFT", ImNodesMiniMapLocation_::ImNodesMiniMapLocation_BottomLeft)
        .value("MINI_MAP_LOCATION_BOTTOM_RIGHT", ImNodesMiniMapLocation_::ImNodesMiniMapLocation_BottomRight)
        .value("MINI_MAP_LOCATION_TOP_LEFT", ImNodesMiniMapLocation_::ImNodesMiniMapLocation_TopLeft)
        .value("MINI_MAP_LOCATION_TOP_RIGHT", ImNodesMiniMapLocation_::ImNodesMiniMapLocation_TopRight)
        .export_values();

    _imnodes.def("set_im_gui_context", &ImNodes::SetImGuiContext
    , py::arg("ctx")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("editor_context_get_panning", &ImNodes::EditorContextGetPanning
    , py::return_value_policy::automatic_reference);

    _imnodes.def("editor_context_reset_panning", &ImNodes::EditorContextResetPanning
    , py::arg("pos")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("editor_context_move_to_node", &ImNodes::EditorContextMoveToNode
    , py::arg("node_id")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("get_io", &ImNodes::GetIO
    , py::return_value_policy::reference);

    _imnodes.def("get_style", &ImNodes::GetStyle
    , py::return_value_policy::reference);

    _imnodes.def("style_colors_dark", &ImNodes::StyleColorsDark
    , py::arg("dest") = nullptr
    , py::return_value_policy::automatic_reference);

    _imnodes.def("style_colors_classic", &ImNodes::StyleColorsClassic
    , py::arg("dest") = nullptr
    , py::return_value_policy::automatic_reference);

    _imnodes.def("style_colors_light", &ImNodes::StyleColorsLight
    , py::arg("dest") = nullptr
    , py::return_value_policy::automatic_reference);

    _imnodes.def("begin_node_editor", &ImNodes::BeginNodeEditor
    , py::return_value_policy::automatic_reference);

    _imnodes.def("end_node_editor", &ImNodes::EndNodeEditor
    , py::return_value_policy::automatic_reference);

    _imnodes.def("push_color_style", &ImNodes::PushColorStyle
    , py::arg("item")
    , py::arg("color")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("pop_color_style", &ImNodes::PopColorStyle
    , py::return_value_policy::automatic_reference);

    _imnodes.def("push_style_var", py::overload_cast<ImNodesStyleVar, float>(&ImNodes::PushStyleVar)
    , py::arg("style_item")
    , py::arg("value")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("push_style_var", py::overload_cast<ImNodesStyleVar, const ImVec2 &>(&ImNodes::PushStyleVar)
    , py::arg("style_item")
    , py::arg("value")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("pop_style_var", &ImNodes::PopStyleVar
    , py::arg("count") = 1
    , py::return_value_policy::automatic_reference);

    _imnodes.def("begin_node", &ImNodes::BeginNode
    , py::arg("id")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("end_node", &ImNodes::EndNode
    , py::return_value_policy::automatic_reference);

    _imnodes.def("get_node_dimensions", &ImNodes::GetNodeDimensions
    , py::arg("id")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("begin_node_title_bar", &ImNodes::BeginNodeTitleBar
    , py::return_value_policy::automatic_reference);

    _imnodes.def("end_node_title_bar", &ImNodes::EndNodeTitleBar
    , py::return_value_policy::automatic_reference);

    _imnodes.def("begin_input_attribute", &ImNodes::BeginInputAttribute
    , py::arg("id")
    , py::arg("shape") = ImNodesPinShape_CircleFilled
    , py::return_value_policy::automatic_reference);

    _imnodes.def("end_input_attribute", &ImNodes::EndInputAttribute
    , py::return_value_policy::automatic_reference);

    _imnodes.def("begin_output_attribute", &ImNodes::BeginOutputAttribute
    , py::arg("id")
    , py::arg("shape") = ImNodesPinShape_CircleFilled
    , py::return_value_policy::automatic_reference);

    _imnodes.def("end_output_attribute", &ImNodes::EndOutputAttribute
    , py::return_value_policy::automatic_reference);

    _imnodes.def("begin_static_attribute", &ImNodes::BeginStaticAttribute
    , py::arg("id")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("end_static_attribute", &ImNodes::EndStaticAttribute
    , py::return_value_policy::automatic_reference);

    _imnodes.def("push_attribute_flag", &ImNodes::PushAttributeFlag
    , py::arg("flag")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("pop_attribute_flag", &ImNodes::PopAttributeFlag
    , py::return_value_policy::automatic_reference);

    _imnodes.def("link", &ImNodes::Link
    , py::arg("id")
    , py::arg("start_attribute_id")
    , py::arg("end_attribute_id")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("set_node_draggable", &ImNodes::SetNodeDraggable
    , py::arg("node_id")
    , py::arg("draggable")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("set_node_screen_space_pos", &ImNodes::SetNodeScreenSpacePos
    , py::arg("node_id")
    , py::arg("screen_space_pos")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("set_node_editor_space_pos", &ImNodes::SetNodeEditorSpacePos
    , py::arg("node_id")
    , py::arg("editor_space_pos")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("set_node_grid_space_pos", &ImNodes::SetNodeGridSpacePos
    , py::arg("node_id")
    , py::arg("grid_pos")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("get_node_screen_space_pos", &ImNodes::GetNodeScreenSpacePos
    , py::arg("node_id")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("get_node_editor_space_pos", &ImNodes::GetNodeEditorSpacePos
    , py::arg("node_id")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("get_node_grid_space_pos", &ImNodes::GetNodeGridSpacePos
    , py::arg("node_id")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("snap_node_to_grid", &ImNodes::SnapNodeToGrid
    , py::arg("node_id")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("is_editor_hovered", &ImNodes::IsEditorHovered
    , py::return_value_policy::automatic_reference);

    _imnodes.def("is_node_hovered", [](int * node_id)
    {
        auto ret = ImNodes::IsNodeHovered(node_id);
        return std::make_tuple(ret, node_id);
    }
    , py::arg("node_id")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("is_link_hovered", [](int * link_id)
    {
        auto ret = ImNodes::IsLinkHovered(link_id);
        return std::make_tuple(ret, link_id);
    }
    , py::arg("link_id")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("is_pin_hovered", [](int * attribute_id)
    {
        auto ret = ImNodes::IsPinHovered(attribute_id);
        return std::make_tuple(ret, attribute_id);
    }
    , py::arg("attribute_id")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("num_selected_nodes", &ImNodes::NumSelectedNodes
    , py::return_value_policy::automatic_reference);

    _imnodes.def("num_selected_links", &ImNodes::NumSelectedLinks
    , py::return_value_policy::automatic_reference);

    _imnodes.def("get_selected_nodes", [](int * node_ids)
    {
        ImNodes::GetSelectedNodes(node_ids);
        return node_ids;
    }
    , py::arg("node_ids")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("get_selected_links", [](int * link_ids)
    {
        ImNodes::GetSelectedLinks(link_ids);
        return link_ids;
    }
    , py::arg("link_ids")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("clear_node_selection", py::overload_cast<>(&ImNodes::ClearNodeSelection)
    , py::return_value_policy::automatic_reference);

    _imnodes.def("clear_link_selection", py::overload_cast<>(&ImNodes::ClearLinkSelection)
    , py::return_value_policy::automatic_reference);

    _imnodes.def("select_node", &ImNodes::SelectNode
    , py::arg("node_id")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("clear_node_selection", py::overload_cast<int>(&ImNodes::ClearNodeSelection)
    , py::arg("node_id")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("is_node_selected", &ImNodes::IsNodeSelected
    , py::arg("node_id")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("select_link", &ImNodes::SelectLink
    , py::arg("link_id")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("clear_link_selection", py::overload_cast<int>(&ImNodes::ClearLinkSelection)
    , py::arg("link_id")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("is_link_selected", &ImNodes::IsLinkSelected
    , py::arg("link_id")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("is_attribute_active", &ImNodes::IsAttributeActive
    , py::return_value_policy::automatic_reference);

    _imnodes.def("is_any_attribute_active", [](int * attribute_id)
    {
        auto ret = ImNodes::IsAnyAttributeActive(attribute_id);
        return std::make_tuple(ret, attribute_id);
    }
    , py::arg("attribute_id") = nullptr
    , py::return_value_policy::automatic_reference);

    _imnodes.def("is_link_started", [](int * started_at_attribute_id)
    {
        auto ret = ImNodes::IsLinkStarted(started_at_attribute_id);
        return std::make_tuple(ret, started_at_attribute_id);
    }
    , py::arg("started_at_attribute_id")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("is_link_dropped", [](int * started_at_attribute_id, bool including_detached_links)
    {
        auto ret = ImNodes::IsLinkDropped(started_at_attribute_id, including_detached_links);
        return std::make_tuple(ret, started_at_attribute_id);
    }
    , py::arg("started_at_attribute_id") = nullptr
    , py::arg("including_detached_links") = true
    , py::return_value_policy::automatic_reference);

    _imnodes.def("is_link_created", [](int * started_at_attribute_id, int * ended_at_attribute_id, bool * created_from_snap)
    {
        auto ret = ImNodes::IsLinkCreated(started_at_attribute_id, ended_at_attribute_id, created_from_snap);
        return std::make_tuple(ret, started_at_attribute_id, ended_at_attribute_id, created_from_snap);
    }
    , py::arg("started_at_attribute_id")
    , py::arg("ended_at_attribute_id")
    , py::arg("created_from_snap") = nullptr
    , py::return_value_policy::automatic_reference);

    _imnodes.def("is_link_created", [](int * started_at_node_id, int * started_at_attribute_id, int * ended_at_node_id, int * ended_at_attribute_id, bool * created_from_snap)
    {
        auto ret = ImNodes::IsLinkCreated(started_at_node_id, started_at_attribute_id, ended_at_node_id, ended_at_attribute_id, created_from_snap);
        return std::make_tuple(ret, started_at_node_id, started_at_attribute_id, ended_at_node_id, ended_at_attribute_id, created_from_snap);
    }
    , py::arg("started_at_node_id")
    , py::arg("started_at_attribute_id")
    , py::arg("ended_at_node_id")
    , py::arg("ended_at_attribute_id")
    , py::arg("created_from_snap") = nullptr
    , py::return_value_policy::automatic_reference);

    _imnodes.def("is_link_destroyed", [](int * link_id)
    {
        auto ret = ImNodes::IsLinkDestroyed(link_id);
        return std::make_tuple(ret, link_id);
    }
    , py::arg("link_id")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("save_current_editor_state_to_ini_string", [](size_t * data_size)
    {
        auto ret = ImNodes::SaveCurrentEditorStateToIniString(data_size);
        return std::make_tuple(ret, data_size);
    }
    , py::arg("data_size") = nullptr
    , py::return_value_policy::automatic_reference);

    _imnodes.def("save_editor_state_to_ini_string", [](const ImNodesEditorContext * editor, size_t * data_size)
    {
        auto ret = ImNodes::SaveEditorStateToIniString(editor, data_size);
        return std::make_tuple(ret, data_size);
    }
    , py::arg("editor")
    , py::arg("data_size") = nullptr
    , py::return_value_policy::automatic_reference);

    _imnodes.def("load_current_editor_state_from_ini_string", &ImNodes::LoadCurrentEditorStateFromIniString
    , py::arg("data")
    , py::arg("data_size")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("load_editor_state_from_ini_string", &ImNodes::LoadEditorStateFromIniString
    , py::arg("editor")
    , py::arg("data")
    , py::arg("data_size")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("save_current_editor_state_to_ini_file", &ImNodes::SaveCurrentEditorStateToIniFile
    , py::arg("file_name")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("save_editor_state_to_ini_file", &ImNodes::SaveEditorStateToIniFile
    , py::arg("editor")
    , py::arg("file_name")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("load_current_editor_state_from_ini_file", &ImNodes::LoadCurrentEditorStateFromIniFile
    , py::arg("file_name")
    , py::return_value_policy::automatic_reference);

    _imnodes.def("load_editor_state_from_ini_file", &ImNodes::LoadEditorStateFromIniFile
    , py::arg("editor")
    , py::arg("file_name")
    , py::return_value_policy::automatic_reference);


}