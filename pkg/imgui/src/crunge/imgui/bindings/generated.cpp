#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

#include "imgui_internal.h"
//#include "imgui.h"

#include <cxbind/cxbind.h>
#include <crunge/imgui/conversions.h>

namespace py = pybind11;

void init_generated(py::module &_imgui, Registry &registry) {
    PYCLASS_BEGIN(_imgui, ImVec2, Vec2)
        Vec2.def_readwrite("x", &ImVec2::x);
        Vec2.def_readwrite("y", &ImVec2::y);
        Vec2.def(py::init<>());
    PYCLASS_END(_imgui, ImVec2, Vec2)
    PYCLASS_BEGIN(_imgui, ImVec4, Vec4)
        Vec4.def_readwrite("x", &ImVec4::x);
        Vec4.def_readwrite("y", &ImVec4::y);
        Vec4.def_readwrite("z", &ImVec4::z);
        Vec4.def_readwrite("w", &ImVec4::w);
        Vec4.def(py::init<>());
    PYCLASS_END(_imgui, ImVec4, Vec4)
    _imgui.def("get_io", &ImGui::GetIO
    , py::return_value_policy::reference);
    
    _imgui.def("get_style", &ImGui::GetStyle
    , py::return_value_policy::reference);
    
    _imgui.def("new_frame", &ImGui::NewFrame
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("end_frame", &ImGui::EndFrame
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("render", &ImGui::Render
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_draw_data", &ImGui::GetDrawData
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("show_demo_window", [](bool * p_open)
    {
        ImGui::ShowDemoWindow(p_open);
        return p_open;
    }
    , py::arg("p_open") = nullptr
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("show_metrics_window", [](bool * p_open)
    {
        ImGui::ShowMetricsWindow(p_open);
        return p_open;
    }
    , py::arg("p_open") = nullptr
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("show_debug_log_window", [](bool * p_open)
    {
        ImGui::ShowDebugLogWindow(p_open);
        return p_open;
    }
    , py::arg("p_open") = nullptr
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("show_id_stack_tool_window", [](bool * p_open)
    {
        ImGui::ShowIDStackToolWindow(p_open);
        return p_open;
    }
    , py::arg("p_open") = nullptr
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("show_about_window", [](bool * p_open)
    {
        ImGui::ShowAboutWindow(p_open);
        return p_open;
    }
    , py::arg("p_open") = nullptr
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("show_style_editor", &ImGui::ShowStyleEditor
    , py::arg("ref") = nullptr
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("show_style_selector", &ImGui::ShowStyleSelector
    , py::arg("label")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("show_font_selector", &ImGui::ShowFontSelector
    , py::arg("label")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("show_user_guide", &ImGui::ShowUserGuide
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_version", &ImGui::GetVersion
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("style_colors_dark", &ImGui::StyleColorsDark
    , py::arg("dst") = nullptr
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("style_colors_light", &ImGui::StyleColorsLight
    , py::arg("dst") = nullptr
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("style_colors_classic", &ImGui::StyleColorsClassic
    , py::arg("dst") = nullptr
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("begin", [](const char * name, bool * p_open, int flags)
    {
        auto ret = ImGui::Begin(name, p_open, flags);
        return std::make_tuple(ret, p_open);
    }
    , py::arg("name")
    , py::arg("p_open") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("end", &ImGui::End
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("begin_child", py::overload_cast<const char *, const ImVec2 &, bool, int>(&ImGui::BeginChild)
    , py::arg("str_id")
    , py::arg("size") = ImVec2(0,0)
    , py::arg("border") = false
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("end_child", &ImGui::EndChild
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("is_window_appearing", &ImGui::IsWindowAppearing
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("is_window_collapsed", &ImGui::IsWindowCollapsed
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("is_window_focused", &ImGui::IsWindowFocused
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("is_window_hovered", &ImGui::IsWindowHovered
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_window_draw_list", &ImGui::GetWindowDrawList
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_window_dpi_scale", &ImGui::GetWindowDpiScale
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_window_pos", &ImGui::GetWindowPos
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_window_size", &ImGui::GetWindowSize
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_window_width", &ImGui::GetWindowWidth
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_window_height", &ImGui::GetWindowHeight
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_window_viewport", &ImGui::GetWindowViewport
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_next_window_pos", &ImGui::SetNextWindowPos
    , py::arg("pos")
    , py::arg("cond") = 0
    , py::arg("pivot") = ImVec2(0,0)
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_next_window_size", &ImGui::SetNextWindowSize
    , py::arg("size")
    , py::arg("cond") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_next_window_content_size", &ImGui::SetNextWindowContentSize
    , py::arg("size")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_next_window_collapsed", &ImGui::SetNextWindowCollapsed
    , py::arg("collapsed")
    , py::arg("cond") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_next_window_focus", &ImGui::SetNextWindowFocus
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_next_window_scroll", &ImGui::SetNextWindowScroll
    , py::arg("scroll")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_next_window_bg_alpha", &ImGui::SetNextWindowBgAlpha
    , py::arg("alpha")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_next_window_viewport", &ImGui::SetNextWindowViewport
    , py::arg("viewport_id")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_window_pos", py::overload_cast<const ImVec2 &, int>(&ImGui::SetWindowPos)
    , py::arg("pos")
    , py::arg("cond") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_window_size", py::overload_cast<const ImVec2 &, int>(&ImGui::SetWindowSize)
    , py::arg("size")
    , py::arg("cond") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_window_collapsed", py::overload_cast<bool, int>(&ImGui::SetWindowCollapsed)
    , py::arg("collapsed")
    , py::arg("cond") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_window_focus", py::overload_cast<>(&ImGui::SetWindowFocus)
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_window_font_scale", &ImGui::SetWindowFontScale
    , py::arg("scale")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_content_region_avail", &ImGui::GetContentRegionAvail
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_content_region_max", &ImGui::GetContentRegionMax
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_window_content_region_min", &ImGui::GetWindowContentRegionMin
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_window_content_region_max", &ImGui::GetWindowContentRegionMax
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_scroll_x", &ImGui::GetScrollX
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_scroll_y", &ImGui::GetScrollY
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_scroll_x", py::overload_cast<float>(&ImGui::SetScrollX)
    , py::arg("scroll_x")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_scroll_y", py::overload_cast<float>(&ImGui::SetScrollY)
    , py::arg("scroll_y")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_scroll_max_x", &ImGui::GetScrollMaxX
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_scroll_max_y", &ImGui::GetScrollMaxY
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_scroll_here_x", &ImGui::SetScrollHereX
    , py::arg("center_x_ratio") = 0.5f
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_scroll_here_y", &ImGui::SetScrollHereY
    , py::arg("center_y_ratio") = 0.5f
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_scroll_from_pos_x", py::overload_cast<float, float>(&ImGui::SetScrollFromPosX)
    , py::arg("local_x")
    , py::arg("center_x_ratio") = 0.5f
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_scroll_from_pos_y", py::overload_cast<float, float>(&ImGui::SetScrollFromPosY)
    , py::arg("local_y")
    , py::arg("center_y_ratio") = 0.5f
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("push_font", &ImGui::PushFont
    , py::arg("font")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("pop_font", &ImGui::PopFont
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("push_style_color", py::overload_cast<int, unsigned int>(&ImGui::PushStyleColor)
    , py::arg("idx")
    , py::arg("col")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("pop_style_color", &ImGui::PopStyleColor
    , py::arg("count") = 1
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("push_style_var", py::overload_cast<int, float>(&ImGui::PushStyleVar)
    , py::arg("idx")
    , py::arg("val")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("pop_style_var", &ImGui::PopStyleVar
    , py::arg("count") = 1
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("push_tab_stop", &ImGui::PushTabStop
    , py::arg("tab_stop")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("pop_tab_stop", &ImGui::PopTabStop
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("push_button_repeat", &ImGui::PushButtonRepeat
    , py::arg("repeat")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("pop_button_repeat", &ImGui::PopButtonRepeat
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("push_item_width", &ImGui::PushItemWidth
    , py::arg("item_width")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("pop_item_width", &ImGui::PopItemWidth
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_next_item_width", &ImGui::SetNextItemWidth
    , py::arg("item_width")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("calc_item_width", &ImGui::CalcItemWidth
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("push_text_wrap_pos", &ImGui::PushTextWrapPos
    , py::arg("wrap_local_pos_x") = 0.0f
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("pop_text_wrap_pos", &ImGui::PopTextWrapPos
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_font", &ImGui::GetFont
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_font_size", &ImGui::GetFontSize
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_font_tex_uv_white_pixel", &ImGui::GetFontTexUvWhitePixel
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_color_u32", py::overload_cast<int, float>(&ImGui::GetColorU32)
    , py::arg("idx")
    , py::arg("alpha_mul") = 1.0f
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_style_color_vec4", &ImGui::GetStyleColorVec4
    , py::arg("idx")
    , py::return_value_policy::reference);
    
    _imgui.def("get_cursor_screen_pos", &ImGui::GetCursorScreenPos
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_cursor_screen_pos", &ImGui::SetCursorScreenPos
    , py::arg("pos")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_cursor_pos", &ImGui::GetCursorPos
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_cursor_pos_x", &ImGui::GetCursorPosX
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_cursor_pos_y", &ImGui::GetCursorPosY
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_cursor_pos", &ImGui::SetCursorPos
    , py::arg("local_pos")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_cursor_pos_x", &ImGui::SetCursorPosX
    , py::arg("local_x")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_cursor_pos_y", &ImGui::SetCursorPosY
    , py::arg("local_y")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_cursor_start_pos", &ImGui::GetCursorStartPos
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("separator", &ImGui::Separator
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("same_line", &ImGui::SameLine
    , py::arg("offset_from_start_x") = 0.0f
    , py::arg("spacing") = -1.0f
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("new_line", &ImGui::NewLine
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("spacing", &ImGui::Spacing
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("dummy", &ImGui::Dummy
    , py::arg("size")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("indent", &ImGui::Indent
    , py::arg("indent_w") = 0.0f
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("unindent", &ImGui::Unindent
    , py::arg("indent_w") = 0.0f
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("begin_group", &ImGui::BeginGroup
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("end_group", &ImGui::EndGroup
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("align_text_to_frame_padding", &ImGui::AlignTextToFramePadding
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_text_line_height", &ImGui::GetTextLineHeight
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_text_line_height_with_spacing", &ImGui::GetTextLineHeightWithSpacing
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_frame_height", &ImGui::GetFrameHeight
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_frame_height_with_spacing", &ImGui::GetFrameHeightWithSpacing
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("push_id", py::overload_cast<const char *>(&ImGui::PushID)
    , py::arg("str_id")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("pop_id", &ImGui::PopID
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_id", py::overload_cast<const char *>(&ImGui::GetID)
    , py::arg("str_id")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("text_unformatted", &ImGui::TextUnformatted
    , py::arg("text")
    , py::arg("text_end") = nullptr
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("text", [](const char * fmt)
    {
        ImGui::Text(fmt);
        return ;
    }
    , py::arg("fmt")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("text_colored", [](const ImVec4 & col, const char * fmt)
    {
        ImGui::TextColored(col, fmt);
        return ;
    }
    , py::arg("col")
    , py::arg("fmt")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("text_disabled", [](const char * fmt)
    {
        ImGui::TextDisabled(fmt);
        return ;
    }
    , py::arg("fmt")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("text_wrapped", [](const char * fmt)
    {
        ImGui::TextWrapped(fmt);
        return ;
    }
    , py::arg("fmt")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("label_text", [](const char * label, const char * fmt)
    {
        ImGui::LabelText(label, fmt);
        return ;
    }
    , py::arg("label")
    , py::arg("fmt")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("bullet_text", [](const char * fmt)
    {
        ImGui::BulletText(fmt);
        return ;
    }
    , py::arg("fmt")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("separator_text", &ImGui::SeparatorText
    , py::arg("label")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("button", &ImGui::Button
    , py::arg("label")
    , py::arg("size") = ImVec2(0,0)
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("small_button", &ImGui::SmallButton
    , py::arg("label")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("invisible_button", &ImGui::InvisibleButton
    , py::arg("str_id")
    , py::arg("size")
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("arrow_button", &ImGui::ArrowButton
    , py::arg("str_id")
    , py::arg("dir")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("checkbox", [](const char * label, bool * v)
    {
        auto ret = ImGui::Checkbox(label, v);
        return std::make_tuple(ret, v);
    }
    , py::arg("label")
    , py::arg("v")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("checkbox_flags", [](const char * label, int * flags, int flags_value)
    {
        auto ret = ImGui::CheckboxFlags(label, flags, flags_value);
        return std::make_tuple(ret, flags);
    }
    , py::arg("label")
    , py::arg("flags")
    , py::arg("flags_value")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("radio_button", py::overload_cast<const char *, bool>(&ImGui::RadioButton)
    , py::arg("label")
    , py::arg("active")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("progress_bar", &ImGui::ProgressBar
    , py::arg("fraction")
    , py::arg("size_arg") = ImVec2(-FLT_MIN,0)
    , py::arg("overlay") = nullptr
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("bullet", &ImGui::Bullet
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("image", &ImGui::Image
    , py::arg("user_texture_id")
    , py::arg("size")
    , py::arg("uv0") = ImVec2(0,0)
    , py::arg("uv1") = ImVec2(1,1)
    , py::arg("tint_col") = ImVec4(1,1,1,1)
    , py::arg("border_col") = ImVec4(0,0,0,0)
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("image_button", &ImGui::ImageButton
    , py::arg("str_id")
    , py::arg("user_texture_id")
    , py::arg("size")
    , py::arg("uv0") = ImVec2(0,0)
    , py::arg("uv1") = ImVec2(1,1)
    , py::arg("bg_col") = ImVec4(0,0,0,0)
    , py::arg("tint_col") = ImVec4(1,1,1,1)
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("begin_combo", &ImGui::BeginCombo
    , py::arg("label")
    , py::arg("preview_value")
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("end_combo", &ImGui::EndCombo
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("drag_float", [](const char * label, float * v, float v_speed, float v_min, float v_max, const char * format, int flags)
    {
        auto ret = ImGui::DragFloat(label, v, v_speed, v_min, v_max, format, flags);
        return std::make_tuple(ret, v);
    }
    , py::arg("label")
    , py::arg("v")
    , py::arg("v_speed") = 1.0f
    , py::arg("v_min") = 0.0f
    , py::arg("v_max") = 0.0f
    , py::arg("format") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("drag_float2", [](const char * label, std::array<float, 2>& v, float v_speed, float v_min, float v_max, const char * format, int flags)
    {
        auto ret = ImGui::DragFloat2(label, &v[0], v_speed, v_min, v_max, format, flags);
        return std::make_tuple(ret, v);
    }
    , py::arg("label")
    , py::arg("v")
    , py::arg("v_speed") = 1.0f
    , py::arg("v_min") = 0.0f
    , py::arg("v_max") = 0.0f
    , py::arg("format") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("drag_float3", [](const char * label, std::array<float, 3>& v, float v_speed, float v_min, float v_max, const char * format, int flags)
    {
        auto ret = ImGui::DragFloat3(label, &v[0], v_speed, v_min, v_max, format, flags);
        return std::make_tuple(ret, v);
    }
    , py::arg("label")
    , py::arg("v")
    , py::arg("v_speed") = 1.0f
    , py::arg("v_min") = 0.0f
    , py::arg("v_max") = 0.0f
    , py::arg("format") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("drag_float4", [](const char * label, std::array<float, 4>& v, float v_speed, float v_min, float v_max, const char * format, int flags)
    {
        auto ret = ImGui::DragFloat4(label, &v[0], v_speed, v_min, v_max, format, flags);
        return std::make_tuple(ret, v);
    }
    , py::arg("label")
    , py::arg("v")
    , py::arg("v_speed") = 1.0f
    , py::arg("v_min") = 0.0f
    , py::arg("v_max") = 0.0f
    , py::arg("format") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("drag_float_range2", [](const char * label, float * v_current_min, float * v_current_max, float v_speed, float v_min, float v_max, const char * format, const char * format_max, int flags)
    {
        auto ret = ImGui::DragFloatRange2(label, v_current_min, v_current_max, v_speed, v_min, v_max, format, format_max, flags);
        return std::make_tuple(ret, v_current_min, v_current_max);
    }
    , py::arg("label")
    , py::arg("v_current_min")
    , py::arg("v_current_max")
    , py::arg("v_speed") = 1.0f
    , py::arg("v_min") = 0.0f
    , py::arg("v_max") = 0.0f
    , py::arg("format") = nullptr
    , py::arg("format_max") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("drag_int", [](const char * label, int * v, float v_speed, int v_min, int v_max, const char * format, int flags)
    {
        auto ret = ImGui::DragInt(label, v, v_speed, v_min, v_max, format, flags);
        return std::make_tuple(ret, v);
    }
    , py::arg("label")
    , py::arg("v")
    , py::arg("v_speed") = 1.0f
    , py::arg("v_min") = 0
    , py::arg("v_max") = 0
    , py::arg("format") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("drag_int2", [](const char * label, std::array<int, 2>& v, float v_speed, int v_min, int v_max, const char * format, int flags)
    {
        auto ret = ImGui::DragInt2(label, &v[0], v_speed, v_min, v_max, format, flags);
        return std::make_tuple(ret, v);
    }
    , py::arg("label")
    , py::arg("v")
    , py::arg("v_speed") = 1.0f
    , py::arg("v_min") = 0
    , py::arg("v_max") = 0
    , py::arg("format") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("drag_int3", [](const char * label, std::array<int, 3>& v, float v_speed, int v_min, int v_max, const char * format, int flags)
    {
        auto ret = ImGui::DragInt3(label, &v[0], v_speed, v_min, v_max, format, flags);
        return std::make_tuple(ret, v);
    }
    , py::arg("label")
    , py::arg("v")
    , py::arg("v_speed") = 1.0f
    , py::arg("v_min") = 0
    , py::arg("v_max") = 0
    , py::arg("format") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("drag_int4", [](const char * label, std::array<int, 4>& v, float v_speed, int v_min, int v_max, const char * format, int flags)
    {
        auto ret = ImGui::DragInt4(label, &v[0], v_speed, v_min, v_max, format, flags);
        return std::make_tuple(ret, v);
    }
    , py::arg("label")
    , py::arg("v")
    , py::arg("v_speed") = 1.0f
    , py::arg("v_min") = 0
    , py::arg("v_max") = 0
    , py::arg("format") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("drag_int_range2", [](const char * label, int * v_current_min, int * v_current_max, float v_speed, int v_min, int v_max, const char * format, const char * format_max, int flags)
    {
        auto ret = ImGui::DragIntRange2(label, v_current_min, v_current_max, v_speed, v_min, v_max, format, format_max, flags);
        return std::make_tuple(ret, v_current_min, v_current_max);
    }
    , py::arg("label")
    , py::arg("v_current_min")
    , py::arg("v_current_max")
    , py::arg("v_speed") = 1.0f
    , py::arg("v_min") = 0
    , py::arg("v_max") = 0
    , py::arg("format") = nullptr
    , py::arg("format_max") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("drag_scalar", &ImGui::DragScalar
    , py::arg("label")
    , py::arg("data_type")
    , py::arg("p_data")
    , py::arg("v_speed") = 1.0f
    , py::arg("p_min") = nullptr
    , py::arg("p_max") = nullptr
    , py::arg("format") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("drag_scalar_n", &ImGui::DragScalarN
    , py::arg("label")
    , py::arg("data_type")
    , py::arg("p_data")
    , py::arg("components")
    , py::arg("v_speed") = 1.0f
    , py::arg("p_min") = nullptr
    , py::arg("p_max") = nullptr
    , py::arg("format") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("slider_float", [](const char * label, float * v, float v_min, float v_max, const char * format, int flags)
    {
        auto ret = ImGui::SliderFloat(label, v, v_min, v_max, format, flags);
        return std::make_tuple(ret, v);
    }
    , py::arg("label")
    , py::arg("v")
    , py::arg("v_min")
    , py::arg("v_max")
    , py::arg("format") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("slider_float2", [](const char * label, std::array<float, 2>& v, float v_min, float v_max, const char * format, int flags)
    {
        auto ret = ImGui::SliderFloat2(label, &v[0], v_min, v_max, format, flags);
        return std::make_tuple(ret, v);
    }
    , py::arg("label")
    , py::arg("v")
    , py::arg("v_min")
    , py::arg("v_max")
    , py::arg("format") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("slider_float3", [](const char * label, std::array<float, 3>& v, float v_min, float v_max, const char * format, int flags)
    {
        auto ret = ImGui::SliderFloat3(label, &v[0], v_min, v_max, format, flags);
        return std::make_tuple(ret, v);
    }
    , py::arg("label")
    , py::arg("v")
    , py::arg("v_min")
    , py::arg("v_max")
    , py::arg("format") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("slider_float4", [](const char * label, std::array<float, 4>& v, float v_min, float v_max, const char * format, int flags)
    {
        auto ret = ImGui::SliderFloat4(label, &v[0], v_min, v_max, format, flags);
        return std::make_tuple(ret, v);
    }
    , py::arg("label")
    , py::arg("v")
    , py::arg("v_min")
    , py::arg("v_max")
    , py::arg("format") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("slider_angle", [](const char * label, float * v_rad, float v_degrees_min, float v_degrees_max, const char * format, int flags)
    {
        auto ret = ImGui::SliderAngle(label, v_rad, v_degrees_min, v_degrees_max, format, flags);
        return std::make_tuple(ret, v_rad);
    }
    , py::arg("label")
    , py::arg("v_rad")
    , py::arg("v_degrees_min") = -360.0f
    , py::arg("v_degrees_max") = +360.0f
    , py::arg("format") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("slider_int", [](const char * label, int * v, int v_min, int v_max, const char * format, int flags)
    {
        auto ret = ImGui::SliderInt(label, v, v_min, v_max, format, flags);
        return std::make_tuple(ret, v);
    }
    , py::arg("label")
    , py::arg("v")
    , py::arg("v_min")
    , py::arg("v_max")
    , py::arg("format") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("slider_int2", [](const char * label, std::array<int, 2>& v, int v_min, int v_max, const char * format, int flags)
    {
        auto ret = ImGui::SliderInt2(label, &v[0], v_min, v_max, format, flags);
        return std::make_tuple(ret, v);
    }
    , py::arg("label")
    , py::arg("v")
    , py::arg("v_min")
    , py::arg("v_max")
    , py::arg("format") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("slider_int3", [](const char * label, std::array<int, 3>& v, int v_min, int v_max, const char * format, int flags)
    {
        auto ret = ImGui::SliderInt3(label, &v[0], v_min, v_max, format, flags);
        return std::make_tuple(ret, v);
    }
    , py::arg("label")
    , py::arg("v")
    , py::arg("v_min")
    , py::arg("v_max")
    , py::arg("format") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("slider_int4", [](const char * label, std::array<int, 4>& v, int v_min, int v_max, const char * format, int flags)
    {
        auto ret = ImGui::SliderInt4(label, &v[0], v_min, v_max, format, flags);
        return std::make_tuple(ret, v);
    }
    , py::arg("label")
    , py::arg("v")
    , py::arg("v_min")
    , py::arg("v_max")
    , py::arg("format") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("slider_scalar", &ImGui::SliderScalar
    , py::arg("label")
    , py::arg("data_type")
    , py::arg("p_data")
    , py::arg("p_min")
    , py::arg("p_max")
    , py::arg("format") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("slider_scalar_n", &ImGui::SliderScalarN
    , py::arg("label")
    , py::arg("data_type")
    , py::arg("p_data")
    , py::arg("components")
    , py::arg("p_min")
    , py::arg("p_max")
    , py::arg("format") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("v_slider_float", [](const char * label, const ImVec2 & size, float * v, float v_min, float v_max, const char * format, int flags)
    {
        auto ret = ImGui::VSliderFloat(label, size, v, v_min, v_max, format, flags);
        return std::make_tuple(ret, v);
    }
    , py::arg("label")
    , py::arg("size")
    , py::arg("v")
    , py::arg("v_min")
    , py::arg("v_max")
    , py::arg("format") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("v_slider_int", [](const char * label, const ImVec2 & size, int * v, int v_min, int v_max, const char * format, int flags)
    {
        auto ret = ImGui::VSliderInt(label, size, v, v_min, v_max, format, flags);
        return std::make_tuple(ret, v);
    }
    , py::arg("label")
    , py::arg("size")
    , py::arg("v")
    , py::arg("v_min")
    , py::arg("v_max")
    , py::arg("format") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("v_slider_scalar", &ImGui::VSliderScalar
    , py::arg("label")
    , py::arg("size")
    , py::arg("data_type")
    , py::arg("p_data")
    , py::arg("p_min")
    , py::arg("p_max")
    , py::arg("format") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("input_text_with_hint", &ImGui::InputTextWithHint
    , py::arg("label")
    , py::arg("hint")
    , py::arg("buf")
    , py::arg("buf_size")
    , py::arg("flags") = 0
    , py::arg("callback") = NULL
    , py::arg("user_data") = nullptr
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("input_float", [](const char * label, float * v, float step, float step_fast, const char * format, int flags)
    {
        auto ret = ImGui::InputFloat(label, v, step, step_fast, format, flags);
        return std::make_tuple(ret, v);
    }
    , py::arg("label")
    , py::arg("v")
    , py::arg("step") = 0.0f
    , py::arg("step_fast") = 0.0f
    , py::arg("format") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("input_float2", [](const char * label, std::array<float, 2>& v, const char * format, int flags)
    {
        auto ret = ImGui::InputFloat2(label, &v[0], format, flags);
        return std::make_tuple(ret, v);
    }
    , py::arg("label")
    , py::arg("v")
    , py::arg("format") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("input_float3", [](const char * label, std::array<float, 3>& v, const char * format, int flags)
    {
        auto ret = ImGui::InputFloat3(label, &v[0], format, flags);
        return std::make_tuple(ret, v);
    }
    , py::arg("label")
    , py::arg("v")
    , py::arg("format") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("input_float4", [](const char * label, std::array<float, 4>& v, const char * format, int flags)
    {
        auto ret = ImGui::InputFloat4(label, &v[0], format, flags);
        return std::make_tuple(ret, v);
    }
    , py::arg("label")
    , py::arg("v")
    , py::arg("format") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("input_int", [](const char * label, int * v, int step, int step_fast, int flags)
    {
        auto ret = ImGui::InputInt(label, v, step, step_fast, flags);
        return std::make_tuple(ret, v);
    }
    , py::arg("label")
    , py::arg("v")
    , py::arg("step") = 1
    , py::arg("step_fast") = 100
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("input_int2", [](const char * label, std::array<int, 2>& v, int flags)
    {
        auto ret = ImGui::InputInt2(label, &v[0], flags);
        return std::make_tuple(ret, v);
    }
    , py::arg("label")
    , py::arg("v")
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("input_int3", [](const char * label, std::array<int, 3>& v, int flags)
    {
        auto ret = ImGui::InputInt3(label, &v[0], flags);
        return std::make_tuple(ret, v);
    }
    , py::arg("label")
    , py::arg("v")
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("input_int4", [](const char * label, std::array<int, 4>& v, int flags)
    {
        auto ret = ImGui::InputInt4(label, &v[0], flags);
        return std::make_tuple(ret, v);
    }
    , py::arg("label")
    , py::arg("v")
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("input_double", [](const char * label, double * v, double step, double step_fast, const char * format, int flags)
    {
        auto ret = ImGui::InputDouble(label, v, step, step_fast, format, flags);
        return std::make_tuple(ret, v);
    }
    , py::arg("label")
    , py::arg("v")
    , py::arg("step") = 0.0
    , py::arg("step_fast") = 0.0
    , py::arg("format") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("input_scalar", &ImGui::InputScalar
    , py::arg("label")
    , py::arg("data_type")
    , py::arg("p_data")
    , py::arg("p_step") = nullptr
    , py::arg("p_step_fast") = nullptr
    , py::arg("format") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("input_scalar_n", &ImGui::InputScalarN
    , py::arg("label")
    , py::arg("data_type")
    , py::arg("p_data")
    , py::arg("components")
    , py::arg("p_step") = nullptr
    , py::arg("p_step_fast") = nullptr
    , py::arg("format") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("color_edit3", [](const char * label, std::array<float, 3>& col, int flags)
    {
        auto ret = ImGui::ColorEdit3(label, &col[0], flags);
        return std::make_tuple(ret, col);
    }
    , py::arg("label")
    , py::arg("col")
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("color_edit4", [](const char * label, std::array<float, 4>& col, int flags)
    {
        auto ret = ImGui::ColorEdit4(label, &col[0], flags);
        return std::make_tuple(ret, col);
    }
    , py::arg("label")
    , py::arg("col")
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("color_picker3", [](const char * label, std::array<float, 3>& col, int flags)
    {
        auto ret = ImGui::ColorPicker3(label, &col[0], flags);
        return std::make_tuple(ret, col);
    }
    , py::arg("label")
    , py::arg("col")
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("color_picker4", [](const char * label, std::array<float, 4>& col, int flags, const float * ref_col)
    {
        auto ret = ImGui::ColorPicker4(label, &col[0], flags, ref_col);
        return std::make_tuple(ret, col);
    }
    , py::arg("label")
    , py::arg("col")
    , py::arg("flags") = 0
    , py::arg("ref_col") = nullptr
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("color_button", &ImGui::ColorButton
    , py::arg("desc_id")
    , py::arg("col")
    , py::arg("flags") = 0
    , py::arg("size") = ImVec2(0,0)
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_color_edit_options", &ImGui::SetColorEditOptions
    , py::arg("flags")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("tree_node", py::overload_cast<const char *>(&ImGui::TreeNode)
    , py::arg("label")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("tree_node_ex", py::overload_cast<const char *, int>(&ImGui::TreeNodeEx)
    , py::arg("label")
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("tree_push", py::overload_cast<const char *>(&ImGui::TreePush)
    , py::arg("str_id")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("tree_pop", &ImGui::TreePop
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_tree_node_to_label_spacing", &ImGui::GetTreeNodeToLabelSpacing
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_next_item_open", &ImGui::SetNextItemOpen
    , py::arg("is_open")
    , py::arg("cond") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("begin_list_box", &ImGui::BeginListBox
    , py::arg("label")
    , py::arg("size") = ImVec2(0,0)
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("end_list_box", &ImGui::EndListBox
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("value", py::overload_cast<const char *, bool>(&ImGui::Value)
    , py::arg("prefix")
    , py::arg("b")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("begin_menu_bar", &ImGui::BeginMenuBar
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("end_menu_bar", &ImGui::EndMenuBar
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("begin_main_menu_bar", &ImGui::BeginMainMenuBar
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("end_main_menu_bar", &ImGui::EndMainMenuBar
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("begin_menu", &ImGui::BeginMenu
    , py::arg("label")
    , py::arg("enabled") = true
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("end_menu", &ImGui::EndMenu
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("begin_tooltip", &ImGui::BeginTooltip
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("end_tooltip", &ImGui::EndTooltip
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_tooltip", [](const char * fmt)
    {
        ImGui::SetTooltip(fmt);
        return ;
    }
    , py::arg("fmt")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("begin_item_tooltip", &ImGui::BeginItemTooltip
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_item_tooltip", [](const char * fmt)
    {
        ImGui::SetItemTooltip(fmt);
        return ;
    }
    , py::arg("fmt")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("begin_popup", &ImGui::BeginPopup
    , py::arg("str_id")
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("begin_popup_modal", [](const char * name, bool * p_open, int flags)
    {
        auto ret = ImGui::BeginPopupModal(name, p_open, flags);
        return std::make_tuple(ret, p_open);
    }
    , py::arg("name")
    , py::arg("p_open") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("end_popup", &ImGui::EndPopup
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("open_popup", py::overload_cast<const char *, int>(&ImGui::OpenPopup)
    , py::arg("str_id")
    , py::arg("popup_flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("open_popup_on_item_click", &ImGui::OpenPopupOnItemClick
    , py::arg("str_id") = nullptr
    , py::arg("popup_flags") = 1
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("close_current_popup", &ImGui::CloseCurrentPopup
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("begin_popup_context_item", &ImGui::BeginPopupContextItem
    , py::arg("str_id") = nullptr
    , py::arg("popup_flags") = 1
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("begin_popup_context_window", &ImGui::BeginPopupContextWindow
    , py::arg("str_id") = nullptr
    , py::arg("popup_flags") = 1
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("begin_popup_context_void", &ImGui::BeginPopupContextVoid
    , py::arg("str_id") = nullptr
    , py::arg("popup_flags") = 1
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("is_popup_open", py::overload_cast<const char *, int>(&ImGui::IsPopupOpen)
    , py::arg("str_id")
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("begin_table", &ImGui::BeginTable
    , py::arg("str_id")
    , py::arg("column")
    , py::arg("flags") = 0
    , py::arg("outer_size") = ImVec2(0.0f,0.0f)
    , py::arg("inner_width") = 0.0f
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("end_table", &ImGui::EndTable
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("table_next_row", &ImGui::TableNextRow
    , py::arg("row_flags") = 0
    , py::arg("min_row_height") = 0.0f
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("table_next_column", &ImGui::TableNextColumn
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("table_set_column_index", &ImGui::TableSetColumnIndex
    , py::arg("column_n")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("table_setup_column", &ImGui::TableSetupColumn
    , py::arg("label")
    , py::arg("flags") = 0
    , py::arg("init_width_or_weight") = 0.0f
    , py::arg("user_id") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("table_setup_scroll_freeze", &ImGui::TableSetupScrollFreeze
    , py::arg("cols")
    , py::arg("rows")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("table_headers_row", &ImGui::TableHeadersRow
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("table_header", &ImGui::TableHeader
    , py::arg("label")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("table_get_sort_specs", &ImGui::TableGetSortSpecs
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("table_get_column_count", &ImGui::TableGetColumnCount
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("table_get_column_index", &ImGui::TableGetColumnIndex
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("table_get_row_index", &ImGui::TableGetRowIndex
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("table_get_column_flags", &ImGui::TableGetColumnFlags
    , py::arg("column_n") = -1
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("table_set_column_enabled", &ImGui::TableSetColumnEnabled
    , py::arg("column_n")
    , py::arg("v")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("table_set_bg_color", &ImGui::TableSetBgColor
    , py::arg("target")
    , py::arg("color")
    , py::arg("column_n") = -1
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("columns", &ImGui::Columns
    , py::arg("count") = 1
    , py::arg("id") = nullptr
    , py::arg("border") = true
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("next_column", &ImGui::NextColumn
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_column_index", &ImGui::GetColumnIndex
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_column_width", &ImGui::GetColumnWidth
    , py::arg("column_index") = -1
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_column_width", &ImGui::SetColumnWidth
    , py::arg("column_index")
    , py::arg("width")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_column_offset", &ImGui::GetColumnOffset
    , py::arg("column_index") = -1
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_column_offset", &ImGui::SetColumnOffset
    , py::arg("column_index")
    , py::arg("offset_x")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_columns_count", &ImGui::GetColumnsCount
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("begin_tab_bar", &ImGui::BeginTabBar
    , py::arg("str_id")
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("end_tab_bar", &ImGui::EndTabBar
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("begin_tab_item", [](const char * label, bool * p_open, int flags)
    {
        auto ret = ImGui::BeginTabItem(label, p_open, flags);
        return std::make_tuple(ret, p_open);
    }
    , py::arg("label")
    , py::arg("p_open") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("end_tab_item", &ImGui::EndTabItem
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("tab_item_button", &ImGui::TabItemButton
    , py::arg("label")
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_tab_item_closed", &ImGui::SetTabItemClosed
    , py::arg("tab_or_docked_window_label")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("dock_space", &ImGui::DockSpace
    , py::arg("id")
    , py::arg("size") = ImVec2(0,0)
    , py::arg("flags") = 0
    , py::arg("window_class") = nullptr
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("dock_space_over_viewport", &ImGui::DockSpaceOverViewport
    , py::arg("viewport") = nullptr
    , py::arg("flags") = 0
    , py::arg("window_class") = nullptr
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_next_window_dock_id", &ImGui::SetNextWindowDockID
    , py::arg("dock_id")
    , py::arg("cond") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_next_window_class", &ImGui::SetNextWindowClass
    , py::arg("window_class")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_window_dock_id", &ImGui::GetWindowDockID
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("is_window_docked", &ImGui::IsWindowDocked
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("log_to_tty", &ImGui::LogToTTY
    , py::arg("auto_open_depth") = -1
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("log_to_file", &ImGui::LogToFile
    , py::arg("auto_open_depth") = -1
    , py::arg("filename") = nullptr
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("log_to_clipboard", &ImGui::LogToClipboard
    , py::arg("auto_open_depth") = -1
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("log_finish", &ImGui::LogFinish
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("log_buttons", &ImGui::LogButtons
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("log_text", [](const char * fmt)
    {
        ImGui::LogText(fmt);
        return ;
    }
    , py::arg("fmt")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("begin_drag_drop_source", &ImGui::BeginDragDropSource
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("end_drag_drop_source", &ImGui::EndDragDropSource
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("begin_drag_drop_target", &ImGui::BeginDragDropTarget
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("accept_drag_drop_payload", &ImGui::AcceptDragDropPayload
    , py::arg("type")
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("end_drag_drop_target", &ImGui::EndDragDropTarget
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_drag_drop_payload", &ImGui::GetDragDropPayload
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("begin_disabled", &ImGui::BeginDisabled
    , py::arg("disabled") = true
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("end_disabled", &ImGui::EndDisabled
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("push_clip_rect", &ImGui::PushClipRect
    , py::arg("clip_rect_min")
    , py::arg("clip_rect_max")
    , py::arg("intersect_with_current_clip_rect")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("pop_clip_rect", &ImGui::PopClipRect
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_item_default_focus", &ImGui::SetItemDefaultFocus
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_keyboard_focus_here", &ImGui::SetKeyboardFocusHere
    , py::arg("offset") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_next_item_allow_overlap", &ImGui::SetNextItemAllowOverlap
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("is_item_hovered", &ImGui::IsItemHovered
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("is_item_active", &ImGui::IsItemActive
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("is_item_focused", &ImGui::IsItemFocused
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("is_item_clicked", &ImGui::IsItemClicked
    , py::arg("mouse_button") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("is_item_visible", &ImGui::IsItemVisible
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("is_item_edited", &ImGui::IsItemEdited
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("is_item_activated", &ImGui::IsItemActivated
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("is_item_deactivated", &ImGui::IsItemDeactivated
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("is_item_deactivated_after_edit", &ImGui::IsItemDeactivatedAfterEdit
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("is_item_toggled_open", &ImGui::IsItemToggledOpen
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("is_any_item_hovered", &ImGui::IsAnyItemHovered
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("is_any_item_active", &ImGui::IsAnyItemActive
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("is_any_item_focused", &ImGui::IsAnyItemFocused
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_item_id", &ImGui::GetItemID
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_item_rect_min", &ImGui::GetItemRectMin
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_item_rect_max", &ImGui::GetItemRectMax
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_item_rect_size", &ImGui::GetItemRectSize
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_main_viewport", &ImGui::GetMainViewport
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_background_draw_list", py::overload_cast<>(&ImGui::GetBackgroundDrawList)
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_foreground_draw_list", py::overload_cast<>(&ImGui::GetForegroundDrawList)
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("is_rect_visible", py::overload_cast<const ImVec2 &>(&ImGui::IsRectVisible)
    , py::arg("size")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_time", &ImGui::GetTime
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_frame_count", &ImGui::GetFrameCount
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_draw_list_shared_data", &ImGui::GetDrawListSharedData
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_style_color_name", &ImGui::GetStyleColorName
    , py::arg("idx")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_state_storage", &ImGui::SetStateStorage
    , py::arg("storage")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_state_storage", &ImGui::GetStateStorage
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("begin_child_frame", &ImGui::BeginChildFrame
    , py::arg("id")
    , py::arg("size")
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("end_child_frame", &ImGui::EndChildFrame
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("calc_text_size", &ImGui::CalcTextSize
    , py::arg("text")
    , py::arg("text_end") = nullptr
    , py::arg("hide_text_after_double_hash") = false
    , py::arg("wrap_width") = -1.0f
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("color_convert_u32_to_float4", &ImGui::ColorConvertU32ToFloat4
    , py::arg("in")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("color_convert_float4_to_u32", &ImGui::ColorConvertFloat4ToU32
    , py::arg("in")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("color_convert_rg_bto_hsv", [](float r, float g, float b, float & out_h, float & out_s, float & out_v)
    {
        ImGui::ColorConvertRGBtoHSV(r, g, b, out_h, out_s, out_v);
        return std::make_tuple(out_h, out_s, out_v);
    }
    , py::arg("r")
    , py::arg("g")
    , py::arg("b")
    , py::arg("out_h") = 0
    , py::arg("out_s") = 0
    , py::arg("out_v") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("color_convert_hs_vto_rgb", [](float h, float s, float v, float & out_r, float & out_g, float & out_b)
    {
        ImGui::ColorConvertHSVtoRGB(h, s, v, out_r, out_g, out_b);
        return std::make_tuple(out_r, out_g, out_b);
    }
    , py::arg("h")
    , py::arg("s")
    , py::arg("v")
    , py::arg("out_r") = 0
    , py::arg("out_g") = 0
    , py::arg("out_b") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("is_key_down", py::overload_cast<ImGuiKey>(&ImGui::IsKeyDown)
    , py::arg("key")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("is_key_pressed", py::overload_cast<ImGuiKey, bool>(&ImGui::IsKeyPressed)
    , py::arg("key")
    , py::arg("repeat") = true
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("is_key_released", py::overload_cast<ImGuiKey>(&ImGui::IsKeyReleased)
    , py::arg("key")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_key_pressed_amount", &ImGui::GetKeyPressedAmount
    , py::arg("key")
    , py::arg("repeat_delay")
    , py::arg("rate")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_key_name", &ImGui::GetKeyName
    , py::arg("key")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_next_frame_want_capture_keyboard", &ImGui::SetNextFrameWantCaptureKeyboard
    , py::arg("want_capture_keyboard")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("is_mouse_down", py::overload_cast<int>(&ImGui::IsMouseDown)
    , py::arg("button")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("is_mouse_clicked", py::overload_cast<int, bool>(&ImGui::IsMouseClicked)
    , py::arg("button")
    , py::arg("repeat") = false
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("is_mouse_released", py::overload_cast<int>(&ImGui::IsMouseReleased)
    , py::arg("button")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("is_mouse_double_clicked", &ImGui::IsMouseDoubleClicked
    , py::arg("button")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_mouse_clicked_count", &ImGui::GetMouseClickedCount
    , py::arg("button")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("is_mouse_hovering_rect", &ImGui::IsMouseHoveringRect
    , py::arg("r_min")
    , py::arg("r_max")
    , py::arg("clip") = true
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("is_mouse_pos_valid", &ImGui::IsMousePosValid
    , py::arg("mouse_pos") = nullptr
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("is_any_mouse_down", &ImGui::IsAnyMouseDown
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_mouse_pos", &ImGui::GetMousePos
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_mouse_pos_on_opening_current_popup", &ImGui::GetMousePosOnOpeningCurrentPopup
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("is_mouse_dragging", &ImGui::IsMouseDragging
    , py::arg("button")
    , py::arg("lock_threshold") = -1.0f
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_mouse_drag_delta", &ImGui::GetMouseDragDelta
    , py::arg("button") = 0
    , py::arg("lock_threshold") = -1.0f
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("reset_mouse_drag_delta", &ImGui::ResetMouseDragDelta
    , py::arg("button") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_mouse_cursor", &ImGui::GetMouseCursor
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_mouse_cursor", &ImGui::SetMouseCursor
    , py::arg("cursor_type")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_next_frame_want_capture_mouse", &ImGui::SetNextFrameWantCaptureMouse
    , py::arg("want_capture_mouse")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_clipboard_text", &ImGui::GetClipboardText
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("set_clipboard_text", &ImGui::SetClipboardText
    , py::arg("text")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("load_ini_settings_from_disk", &ImGui::LoadIniSettingsFromDisk
    , py::arg("ini_filename")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("load_ini_settings_from_memory", &ImGui::LoadIniSettingsFromMemory
    , py::arg("ini_data")
    , py::arg("ini_size") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("save_ini_settings_to_disk", &ImGui::SaveIniSettingsToDisk
    , py::arg("ini_filename")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("save_ini_settings_to_memory", [](unsigned long * out_ini_size)
    {
        auto ret = ImGui::SaveIniSettingsToMemory(out_ini_size);
        return std::make_tuple(ret, out_ini_size);
    }
    , py::arg("out_ini_size") = 0
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("debug_text_encoding", &ImGui::DebugTextEncoding
    , py::arg("text")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("debug_check_version_and_data_layout", &ImGui::DebugCheckVersionAndDataLayout
    , py::arg("version_str")
    , py::arg("sz_io")
    , py::arg("sz_style")
    , py::arg("sz_vec2")
    , py::arg("sz_vec4")
    , py::arg("sz_drawvert")
    , py::arg("sz_drawidx")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("get_platform_io", &ImGui::GetPlatformIO
    , py::return_value_policy::reference);
    
    _imgui.def("update_platform_windows", &ImGui::UpdatePlatformWindows
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("render_platform_windows_default", &ImGui::RenderPlatformWindowsDefault
    , py::arg("platform_render_arg") = nullptr
    , py::arg("renderer_render_arg") = nullptr
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("destroy_platform_windows", &ImGui::DestroyPlatformWindows
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("find_viewport_by_id", &ImGui::FindViewportByID
    , py::arg("id")
    , py::return_value_policy::automatic_reference);
    
    _imgui.def("find_viewport_by_platform_handle", &ImGui::FindViewportByPlatformHandle
    , py::arg("platform_handle")
    , py::return_value_policy::automatic_reference);
    
    py::enum_<ImGuiWindowFlags_>(_imgui, "WindowFlags", py::arithmetic())
        .value("WINDOW_FLAGS_NONE", ImGuiWindowFlags_::ImGuiWindowFlags_None)
        .value("WINDOW_FLAGS_NO_TITLE_BAR", ImGuiWindowFlags_::ImGuiWindowFlags_NoTitleBar)
        .value("WINDOW_FLAGS_NO_RESIZE", ImGuiWindowFlags_::ImGuiWindowFlags_NoResize)
        .value("WINDOW_FLAGS_NO_MOVE", ImGuiWindowFlags_::ImGuiWindowFlags_NoMove)
        .value("WINDOW_FLAGS_NO_SCROLLBAR", ImGuiWindowFlags_::ImGuiWindowFlags_NoScrollbar)
        .value("WINDOW_FLAGS_NO_SCROLL_WITH_MOUSE", ImGuiWindowFlags_::ImGuiWindowFlags_NoScrollWithMouse)
        .value("WINDOW_FLAGS_NO_COLLAPSE", ImGuiWindowFlags_::ImGuiWindowFlags_NoCollapse)
        .value("WINDOW_FLAGS_ALWAYS_AUTO_RESIZE", ImGuiWindowFlags_::ImGuiWindowFlags_AlwaysAutoResize)
        .value("WINDOW_FLAGS_NO_BACKGROUND", ImGuiWindowFlags_::ImGuiWindowFlags_NoBackground)
        .value("WINDOW_FLAGS_NO_SAVED_SETTINGS", ImGuiWindowFlags_::ImGuiWindowFlags_NoSavedSettings)
        .value("WINDOW_FLAGS_NO_MOUSE_INPUTS", ImGuiWindowFlags_::ImGuiWindowFlags_NoMouseInputs)
        .value("WINDOW_FLAGS_MENU_BAR", ImGuiWindowFlags_::ImGuiWindowFlags_MenuBar)
        .value("WINDOW_FLAGS_HORIZONTAL_SCROLLBAR", ImGuiWindowFlags_::ImGuiWindowFlags_HorizontalScrollbar)
        .value("WINDOW_FLAGS_NO_FOCUS_ON_APPEARING", ImGuiWindowFlags_::ImGuiWindowFlags_NoFocusOnAppearing)
        .value("WINDOW_FLAGS_NO_BRING_TO_FRONT_ON_FOCUS", ImGuiWindowFlags_::ImGuiWindowFlags_NoBringToFrontOnFocus)
        .value("WINDOW_FLAGS_ALWAYS_VERTICAL_SCROLLBAR", ImGuiWindowFlags_::ImGuiWindowFlags_AlwaysVerticalScrollbar)
        .value("WINDOW_FLAGS_ALWAYS_HORIZONTAL_SCROLLBAR", ImGuiWindowFlags_::ImGuiWindowFlags_AlwaysHorizontalScrollbar)
        .value("WINDOW_FLAGS_ALWAYS_USE_WINDOW_PADDING", ImGuiWindowFlags_::ImGuiWindowFlags_AlwaysUseWindowPadding)
        .value("WINDOW_FLAGS_NO_NAV_INPUTS", ImGuiWindowFlags_::ImGuiWindowFlags_NoNavInputs)
        .value("WINDOW_FLAGS_NO_NAV_FOCUS", ImGuiWindowFlags_::ImGuiWindowFlags_NoNavFocus)
        .value("WINDOW_FLAGS_UNSAVED_DOCUMENT", ImGuiWindowFlags_::ImGuiWindowFlags_UnsavedDocument)
        .value("WINDOW_FLAGS_NO_DOCKING", ImGuiWindowFlags_::ImGuiWindowFlags_NoDocking)
        .value("WINDOW_FLAGS_NO_NAV", ImGuiWindowFlags_::ImGuiWindowFlags_NoNav)
        .value("WINDOW_FLAGS_NO_DECORATION", ImGuiWindowFlags_::ImGuiWindowFlags_NoDecoration)
        .value("WINDOW_FLAGS_NO_INPUTS", ImGuiWindowFlags_::ImGuiWindowFlags_NoInputs)
        .value("WINDOW_FLAGS_NAV_FLATTENED", ImGuiWindowFlags_::ImGuiWindowFlags_NavFlattened)
        .value("WINDOW_FLAGS_CHILD_WINDOW", ImGuiWindowFlags_::ImGuiWindowFlags_ChildWindow)
        .value("WINDOW_FLAGS_TOOLTIP", ImGuiWindowFlags_::ImGuiWindowFlags_Tooltip)
        .value("WINDOW_FLAGS_POPUP", ImGuiWindowFlags_::ImGuiWindowFlags_Popup)
        .value("WINDOW_FLAGS_MODAL", ImGuiWindowFlags_::ImGuiWindowFlags_Modal)
        .value("WINDOW_FLAGS_CHILD_MENU", ImGuiWindowFlags_::ImGuiWindowFlags_ChildMenu)
        .value("WINDOW_FLAGS_DOCK_NODE_HOST", ImGuiWindowFlags_::ImGuiWindowFlags_DockNodeHost)
        .export_values();
    py::enum_<ImGuiInputTextFlags_>(_imgui, "InputTextFlags", py::arithmetic())
        .value("INPUT_TEXT_FLAGS_NONE", ImGuiInputTextFlags_::ImGuiInputTextFlags_None)
        .value("INPUT_TEXT_FLAGS_CHARS_DECIMAL", ImGuiInputTextFlags_::ImGuiInputTextFlags_CharsDecimal)
        .value("INPUT_TEXT_FLAGS_CHARS_HEXADECIMAL", ImGuiInputTextFlags_::ImGuiInputTextFlags_CharsHexadecimal)
        .value("INPUT_TEXT_FLAGS_CHARS_UPPERCASE", ImGuiInputTextFlags_::ImGuiInputTextFlags_CharsUppercase)
        .value("INPUT_TEXT_FLAGS_CHARS_NO_BLANK", ImGuiInputTextFlags_::ImGuiInputTextFlags_CharsNoBlank)
        .value("INPUT_TEXT_FLAGS_AUTO_SELECT_ALL", ImGuiInputTextFlags_::ImGuiInputTextFlags_AutoSelectAll)
        .value("INPUT_TEXT_FLAGS_ENTER_RETURNS_TRUE", ImGuiInputTextFlags_::ImGuiInputTextFlags_EnterReturnsTrue)
        .value("INPUT_TEXT_FLAGS_CALLBACK_COMPLETION", ImGuiInputTextFlags_::ImGuiInputTextFlags_CallbackCompletion)
        .value("INPUT_TEXT_FLAGS_CALLBACK_HISTORY", ImGuiInputTextFlags_::ImGuiInputTextFlags_CallbackHistory)
        .value("INPUT_TEXT_FLAGS_CALLBACK_ALWAYS", ImGuiInputTextFlags_::ImGuiInputTextFlags_CallbackAlways)
        .value("INPUT_TEXT_FLAGS_CALLBACK_CHAR_FILTER", ImGuiInputTextFlags_::ImGuiInputTextFlags_CallbackCharFilter)
        .value("INPUT_TEXT_FLAGS_ALLOW_TAB_INPUT", ImGuiInputTextFlags_::ImGuiInputTextFlags_AllowTabInput)
        .value("INPUT_TEXT_FLAGS_CTRL_ENTER_FOR_NEW_LINE", ImGuiInputTextFlags_::ImGuiInputTextFlags_CtrlEnterForNewLine)
        .value("INPUT_TEXT_FLAGS_NO_HORIZONTAL_SCROLL", ImGuiInputTextFlags_::ImGuiInputTextFlags_NoHorizontalScroll)
        .value("INPUT_TEXT_FLAGS_ALWAYS_OVERWRITE", ImGuiInputTextFlags_::ImGuiInputTextFlags_AlwaysOverwrite)
        .value("INPUT_TEXT_FLAGS_READ_ONLY", ImGuiInputTextFlags_::ImGuiInputTextFlags_ReadOnly)
        .value("INPUT_TEXT_FLAGS_PASSWORD", ImGuiInputTextFlags_::ImGuiInputTextFlags_Password)
        .value("INPUT_TEXT_FLAGS_NO_UNDO_REDO", ImGuiInputTextFlags_::ImGuiInputTextFlags_NoUndoRedo)
        .value("INPUT_TEXT_FLAGS_CHARS_SCIENTIFIC", ImGuiInputTextFlags_::ImGuiInputTextFlags_CharsScientific)
        .value("INPUT_TEXT_FLAGS_CALLBACK_RESIZE", ImGuiInputTextFlags_::ImGuiInputTextFlags_CallbackResize)
        .value("INPUT_TEXT_FLAGS_CALLBACK_EDIT", ImGuiInputTextFlags_::ImGuiInputTextFlags_CallbackEdit)
        .value("INPUT_TEXT_FLAGS_ESCAPE_CLEARS_ALL", ImGuiInputTextFlags_::ImGuiInputTextFlags_EscapeClearsAll)
        .export_values();
    py::enum_<ImGuiTreeNodeFlags_>(_imgui, "TreeNodeFlags", py::arithmetic())
        .value("TREE_NODE_FLAGS_NONE", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_None)
        .value("TREE_NODE_FLAGS_SELECTED", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_Selected)
        .value("TREE_NODE_FLAGS_FRAMED", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_Framed)
        .value("TREE_NODE_FLAGS_ALLOW_OVERLAP", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_AllowOverlap)
        .value("TREE_NODE_FLAGS_NO_TREE_PUSH_ON_OPEN", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_NoTreePushOnOpen)
        .value("TREE_NODE_FLAGS_NO_AUTO_OPEN_ON_LOG", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_NoAutoOpenOnLog)
        .value("TREE_NODE_FLAGS_DEFAULT_OPEN", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_DefaultOpen)
        .value("TREE_NODE_FLAGS_OPEN_ON_DOUBLE_CLICK", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_OpenOnDoubleClick)
        .value("TREE_NODE_FLAGS_OPEN_ON_ARROW", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_OpenOnArrow)
        .value("TREE_NODE_FLAGS_LEAF", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_Leaf)
        .value("TREE_NODE_FLAGS_BULLET", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_Bullet)
        .value("TREE_NODE_FLAGS_FRAME_PADDING", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_FramePadding)
        .value("TREE_NODE_FLAGS_SPAN_AVAIL_WIDTH", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_SpanAvailWidth)
        .value("TREE_NODE_FLAGS_SPAN_FULL_WIDTH", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_SpanFullWidth)
        .value("TREE_NODE_FLAGS_SPAN_ALL_COLUMNS", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_SpanAllColumns)
        .value("TREE_NODE_FLAGS_NAV_LEFT_JUMPS_BACK_HERE", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_NavLeftJumpsBackHere)
        .value("TREE_NODE_FLAGS_COLLAPSING_HEADER", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_CollapsingHeader)
        .export_values();
    py::enum_<ImGuiPopupFlags_>(_imgui, "PopupFlags", py::arithmetic())
        .value("POPUP_FLAGS_NONE", ImGuiPopupFlags_::ImGuiPopupFlags_None)
        .value("POPUP_FLAGS_MOUSE_BUTTON_LEFT", ImGuiPopupFlags_::ImGuiPopupFlags_MouseButtonLeft)
        .value("POPUP_FLAGS_MOUSE_BUTTON_RIGHT", ImGuiPopupFlags_::ImGuiPopupFlags_MouseButtonRight)
        .value("POPUP_FLAGS_MOUSE_BUTTON_MIDDLE", ImGuiPopupFlags_::ImGuiPopupFlags_MouseButtonMiddle)
        .value("POPUP_FLAGS_MOUSE_BUTTON_MASK", ImGuiPopupFlags_::ImGuiPopupFlags_MouseButtonMask_)
        .value("POPUP_FLAGS_MOUSE_BUTTON_DEFAULT", ImGuiPopupFlags_::ImGuiPopupFlags_MouseButtonDefault_)
        .value("POPUP_FLAGS_NO_OPEN_OVER_EXISTING_POPUP", ImGuiPopupFlags_::ImGuiPopupFlags_NoOpenOverExistingPopup)
        .value("POPUP_FLAGS_NO_OPEN_OVER_ITEMS", ImGuiPopupFlags_::ImGuiPopupFlags_NoOpenOverItems)
        .value("POPUP_FLAGS_ANY_POPUP_ID", ImGuiPopupFlags_::ImGuiPopupFlags_AnyPopupId)
        .value("POPUP_FLAGS_ANY_POPUP_LEVEL", ImGuiPopupFlags_::ImGuiPopupFlags_AnyPopupLevel)
        .value("POPUP_FLAGS_ANY_POPUP", ImGuiPopupFlags_::ImGuiPopupFlags_AnyPopup)
        .export_values();
    py::enum_<ImGuiSelectableFlags_>(_imgui, "SelectableFlags", py::arithmetic())
        .value("SELECTABLE_FLAGS_NONE", ImGuiSelectableFlags_::ImGuiSelectableFlags_None)
        .value("SELECTABLE_FLAGS_DONT_CLOSE_POPUPS", ImGuiSelectableFlags_::ImGuiSelectableFlags_DontClosePopups)
        .value("SELECTABLE_FLAGS_SPAN_ALL_COLUMNS", ImGuiSelectableFlags_::ImGuiSelectableFlags_SpanAllColumns)
        .value("SELECTABLE_FLAGS_ALLOW_DOUBLE_CLICK", ImGuiSelectableFlags_::ImGuiSelectableFlags_AllowDoubleClick)
        .value("SELECTABLE_FLAGS_DISABLED", ImGuiSelectableFlags_::ImGuiSelectableFlags_Disabled)
        .value("SELECTABLE_FLAGS_ALLOW_OVERLAP", ImGuiSelectableFlags_::ImGuiSelectableFlags_AllowOverlap)
        .export_values();
    py::enum_<ImGuiComboFlags_>(_imgui, "ComboFlags", py::arithmetic())
        .value("COMBO_FLAGS_NONE", ImGuiComboFlags_::ImGuiComboFlags_None)
        .value("COMBO_FLAGS_POPUP_ALIGN_LEFT", ImGuiComboFlags_::ImGuiComboFlags_PopupAlignLeft)
        .value("COMBO_FLAGS_HEIGHT_SMALL", ImGuiComboFlags_::ImGuiComboFlags_HeightSmall)
        .value("COMBO_FLAGS_HEIGHT_REGULAR", ImGuiComboFlags_::ImGuiComboFlags_HeightRegular)
        .value("COMBO_FLAGS_HEIGHT_LARGE", ImGuiComboFlags_::ImGuiComboFlags_HeightLarge)
        .value("COMBO_FLAGS_HEIGHT_LARGEST", ImGuiComboFlags_::ImGuiComboFlags_HeightLargest)
        .value("COMBO_FLAGS_NO_ARROW_BUTTON", ImGuiComboFlags_::ImGuiComboFlags_NoArrowButton)
        .value("COMBO_FLAGS_NO_PREVIEW", ImGuiComboFlags_::ImGuiComboFlags_NoPreview)
        .value("COMBO_FLAGS_HEIGHT_MASK", ImGuiComboFlags_::ImGuiComboFlags_HeightMask_)
        .export_values();
    py::enum_<ImGuiTabBarFlags_>(_imgui, "TabBarFlags", py::arithmetic())
        .value("TAB_BAR_FLAGS_NONE", ImGuiTabBarFlags_::ImGuiTabBarFlags_None)
        .value("TAB_BAR_FLAGS_REORDERABLE", ImGuiTabBarFlags_::ImGuiTabBarFlags_Reorderable)
        .value("TAB_BAR_FLAGS_AUTO_SELECT_NEW_TABS", ImGuiTabBarFlags_::ImGuiTabBarFlags_AutoSelectNewTabs)
        .value("TAB_BAR_FLAGS_TAB_LIST_POPUP_BUTTON", ImGuiTabBarFlags_::ImGuiTabBarFlags_TabListPopupButton)
        .value("TAB_BAR_FLAGS_NO_CLOSE_WITH_MIDDLE_MOUSE_BUTTON", ImGuiTabBarFlags_::ImGuiTabBarFlags_NoCloseWithMiddleMouseButton)
        .value("TAB_BAR_FLAGS_NO_TAB_LIST_SCROLLING_BUTTONS", ImGuiTabBarFlags_::ImGuiTabBarFlags_NoTabListScrollingButtons)
        .value("TAB_BAR_FLAGS_NO_TOOLTIP", ImGuiTabBarFlags_::ImGuiTabBarFlags_NoTooltip)
        .value("TAB_BAR_FLAGS_FITTING_POLICY_RESIZE_DOWN", ImGuiTabBarFlags_::ImGuiTabBarFlags_FittingPolicyResizeDown)
        .value("TAB_BAR_FLAGS_FITTING_POLICY_SCROLL", ImGuiTabBarFlags_::ImGuiTabBarFlags_FittingPolicyScroll)
        .value("TAB_BAR_FLAGS_FITTING_POLICY_MASK", ImGuiTabBarFlags_::ImGuiTabBarFlags_FittingPolicyMask_)
        .value("TAB_BAR_FLAGS_FITTING_POLICY_DEFAULT", ImGuiTabBarFlags_::ImGuiTabBarFlags_FittingPolicyDefault_)
        .export_values();
    py::enum_<ImGuiTabItemFlags_>(_imgui, "TabItemFlags", py::arithmetic())
        .value("TAB_ITEM_FLAGS_NONE", ImGuiTabItemFlags_::ImGuiTabItemFlags_None)
        .value("TAB_ITEM_FLAGS_UNSAVED_DOCUMENT", ImGuiTabItemFlags_::ImGuiTabItemFlags_UnsavedDocument)
        .value("TAB_ITEM_FLAGS_SET_SELECTED", ImGuiTabItemFlags_::ImGuiTabItemFlags_SetSelected)
        .value("TAB_ITEM_FLAGS_NO_CLOSE_WITH_MIDDLE_MOUSE_BUTTON", ImGuiTabItemFlags_::ImGuiTabItemFlags_NoCloseWithMiddleMouseButton)
        .value("TAB_ITEM_FLAGS_NO_PUSH_ID", ImGuiTabItemFlags_::ImGuiTabItemFlags_NoPushId)
        .value("TAB_ITEM_FLAGS_NO_TOOLTIP", ImGuiTabItemFlags_::ImGuiTabItemFlags_NoTooltip)
        .value("TAB_ITEM_FLAGS_NO_REORDER", ImGuiTabItemFlags_::ImGuiTabItemFlags_NoReorder)
        .value("TAB_ITEM_FLAGS_LEADING", ImGuiTabItemFlags_::ImGuiTabItemFlags_Leading)
        .value("TAB_ITEM_FLAGS_TRAILING", ImGuiTabItemFlags_::ImGuiTabItemFlags_Trailing)
        .export_values();
    py::enum_<ImGuiTableFlags_>(_imgui, "TableFlags", py::arithmetic())
        .value("TABLE_FLAGS_NONE", ImGuiTableFlags_::ImGuiTableFlags_None)
        .value("TABLE_FLAGS_RESIZABLE", ImGuiTableFlags_::ImGuiTableFlags_Resizable)
        .value("TABLE_FLAGS_REORDERABLE", ImGuiTableFlags_::ImGuiTableFlags_Reorderable)
        .value("TABLE_FLAGS_HIDEABLE", ImGuiTableFlags_::ImGuiTableFlags_Hideable)
        .value("TABLE_FLAGS_SORTABLE", ImGuiTableFlags_::ImGuiTableFlags_Sortable)
        .value("TABLE_FLAGS_NO_SAVED_SETTINGS", ImGuiTableFlags_::ImGuiTableFlags_NoSavedSettings)
        .value("TABLE_FLAGS_CONTEXT_MENU_IN_BODY", ImGuiTableFlags_::ImGuiTableFlags_ContextMenuInBody)
        .value("TABLE_FLAGS_ROW_BG", ImGuiTableFlags_::ImGuiTableFlags_RowBg)
        .value("TABLE_FLAGS_BORDERS_INNER_H", ImGuiTableFlags_::ImGuiTableFlags_BordersInnerH)
        .value("TABLE_FLAGS_BORDERS_OUTER_H", ImGuiTableFlags_::ImGuiTableFlags_BordersOuterH)
        .value("TABLE_FLAGS_BORDERS_INNER_V", ImGuiTableFlags_::ImGuiTableFlags_BordersInnerV)
        .value("TABLE_FLAGS_BORDERS_OUTER_V", ImGuiTableFlags_::ImGuiTableFlags_BordersOuterV)
        .value("TABLE_FLAGS_BORDERS_H", ImGuiTableFlags_::ImGuiTableFlags_BordersH)
        .value("TABLE_FLAGS_BORDERS_V", ImGuiTableFlags_::ImGuiTableFlags_BordersV)
        .value("TABLE_FLAGS_BORDERS_INNER", ImGuiTableFlags_::ImGuiTableFlags_BordersInner)
        .value("TABLE_FLAGS_BORDERS_OUTER", ImGuiTableFlags_::ImGuiTableFlags_BordersOuter)
        .value("TABLE_FLAGS_BORDERS", ImGuiTableFlags_::ImGuiTableFlags_Borders)
        .value("TABLE_FLAGS_NO_BORDERS_IN_BODY", ImGuiTableFlags_::ImGuiTableFlags_NoBordersInBody)
        .value("TABLE_FLAGS_NO_BORDERS_IN_BODY_UNTIL_RESIZE", ImGuiTableFlags_::ImGuiTableFlags_NoBordersInBodyUntilResize)
        .value("TABLE_FLAGS_SIZING_FIXED_FIT", ImGuiTableFlags_::ImGuiTableFlags_SizingFixedFit)
        .value("TABLE_FLAGS_SIZING_FIXED_SAME", ImGuiTableFlags_::ImGuiTableFlags_SizingFixedSame)
        .value("TABLE_FLAGS_SIZING_STRETCH_PROP", ImGuiTableFlags_::ImGuiTableFlags_SizingStretchProp)
        .value("TABLE_FLAGS_SIZING_STRETCH_SAME", ImGuiTableFlags_::ImGuiTableFlags_SizingStretchSame)
        .value("TABLE_FLAGS_NO_HOST_EXTEND_X", ImGuiTableFlags_::ImGuiTableFlags_NoHostExtendX)
        .value("TABLE_FLAGS_NO_HOST_EXTEND_Y", ImGuiTableFlags_::ImGuiTableFlags_NoHostExtendY)
        .value("TABLE_FLAGS_NO_KEEP_COLUMNS_VISIBLE", ImGuiTableFlags_::ImGuiTableFlags_NoKeepColumnsVisible)
        .value("TABLE_FLAGS_PRECISE_WIDTHS", ImGuiTableFlags_::ImGuiTableFlags_PreciseWidths)
        .value("TABLE_FLAGS_NO_CLIP", ImGuiTableFlags_::ImGuiTableFlags_NoClip)
        .value("TABLE_FLAGS_PAD_OUTER_X", ImGuiTableFlags_::ImGuiTableFlags_PadOuterX)
        .value("TABLE_FLAGS_NO_PAD_OUTER_X", ImGuiTableFlags_::ImGuiTableFlags_NoPadOuterX)
        .value("TABLE_FLAGS_NO_PAD_INNER_X", ImGuiTableFlags_::ImGuiTableFlags_NoPadInnerX)
        .value("TABLE_FLAGS_SCROLL_X", ImGuiTableFlags_::ImGuiTableFlags_ScrollX)
        .value("TABLE_FLAGS_SCROLL_Y", ImGuiTableFlags_::ImGuiTableFlags_ScrollY)
        .value("TABLE_FLAGS_SORT_MULTI", ImGuiTableFlags_::ImGuiTableFlags_SortMulti)
        .value("TABLE_FLAGS_SORT_TRISTATE", ImGuiTableFlags_::ImGuiTableFlags_SortTristate)
        .value("TABLE_FLAGS_SIZING_MASK", ImGuiTableFlags_::ImGuiTableFlags_SizingMask_)
        .export_values();
    py::enum_<ImGuiTableColumnFlags_>(_imgui, "TableColumnFlags", py::arithmetic())
        .value("TABLE_COLUMN_FLAGS_NONE", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_None)
        .value("TABLE_COLUMN_FLAGS_DISABLED", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_Disabled)
        .value("TABLE_COLUMN_FLAGS_DEFAULT_HIDE", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_DefaultHide)
        .value("TABLE_COLUMN_FLAGS_DEFAULT_SORT", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_DefaultSort)
        .value("TABLE_COLUMN_FLAGS_WIDTH_STRETCH", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_WidthStretch)
        .value("TABLE_COLUMN_FLAGS_WIDTH_FIXED", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_WidthFixed)
        .value("TABLE_COLUMN_FLAGS_NO_RESIZE", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_NoResize)
        .value("TABLE_COLUMN_FLAGS_NO_REORDER", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_NoReorder)
        .value("TABLE_COLUMN_FLAGS_NO_HIDE", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_NoHide)
        .value("TABLE_COLUMN_FLAGS_NO_CLIP", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_NoClip)
        .value("TABLE_COLUMN_FLAGS_NO_SORT", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_NoSort)
        .value("TABLE_COLUMN_FLAGS_NO_SORT_ASCENDING", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_NoSortAscending)
        .value("TABLE_COLUMN_FLAGS_NO_SORT_DESCENDING", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_NoSortDescending)
        .value("TABLE_COLUMN_FLAGS_NO_HEADER_LABEL", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_NoHeaderLabel)
        .value("TABLE_COLUMN_FLAGS_NO_HEADER_WIDTH", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_NoHeaderWidth)
        .value("TABLE_COLUMN_FLAGS_PREFER_SORT_ASCENDING", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_PreferSortAscending)
        .value("TABLE_COLUMN_FLAGS_PREFER_SORT_DESCENDING", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_PreferSortDescending)
        .value("TABLE_COLUMN_FLAGS_INDENT_ENABLE", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_IndentEnable)
        .value("TABLE_COLUMN_FLAGS_INDENT_DISABLE", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_IndentDisable)
        .value("TABLE_COLUMN_FLAGS_IS_ENABLED", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_IsEnabled)
        .value("TABLE_COLUMN_FLAGS_IS_VISIBLE", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_IsVisible)
        .value("TABLE_COLUMN_FLAGS_IS_SORTED", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_IsSorted)
        .value("TABLE_COLUMN_FLAGS_IS_HOVERED", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_IsHovered)
        .value("TABLE_COLUMN_FLAGS_WIDTH_MASK", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_WidthMask_)
        .value("TABLE_COLUMN_FLAGS_INDENT_MASK", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_IndentMask_)
        .value("TABLE_COLUMN_FLAGS_STATUS_MASK", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_StatusMask_)
        .value("TABLE_COLUMN_FLAGS_NO_DIRECT_RESIZE", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_NoDirectResize_)
        .export_values();
    py::enum_<ImGuiTableRowFlags_>(_imgui, "TableRowFlags", py::arithmetic())
        .value("TABLE_ROW_FLAGS_NONE", ImGuiTableRowFlags_::ImGuiTableRowFlags_None)
        .value("TABLE_ROW_FLAGS_HEADERS", ImGuiTableRowFlags_::ImGuiTableRowFlags_Headers)
        .export_values();
    py::enum_<ImGuiTableBgTarget_>(_imgui, "TableBgTarget", py::arithmetic())
        .value("TABLE_BG_TARGET_NONE", ImGuiTableBgTarget_::ImGuiTableBgTarget_None)
        .value("TABLE_BG_TARGET_ROW_BG0", ImGuiTableBgTarget_::ImGuiTableBgTarget_RowBg0)
        .value("TABLE_BG_TARGET_ROW_BG1", ImGuiTableBgTarget_::ImGuiTableBgTarget_RowBg1)
        .value("TABLE_BG_TARGET_CELL_BG", ImGuiTableBgTarget_::ImGuiTableBgTarget_CellBg)
        .export_values();
    py::enum_<ImGuiFocusedFlags_>(_imgui, "FocusedFlags", py::arithmetic())
        .value("FOCUSED_FLAGS_NONE", ImGuiFocusedFlags_::ImGuiFocusedFlags_None)
        .value("FOCUSED_FLAGS_CHILD_WINDOWS", ImGuiFocusedFlags_::ImGuiFocusedFlags_ChildWindows)
        .value("FOCUSED_FLAGS_ROOT_WINDOW", ImGuiFocusedFlags_::ImGuiFocusedFlags_RootWindow)
        .value("FOCUSED_FLAGS_ANY_WINDOW", ImGuiFocusedFlags_::ImGuiFocusedFlags_AnyWindow)
        .value("FOCUSED_FLAGS_NO_POPUP_HIERARCHY", ImGuiFocusedFlags_::ImGuiFocusedFlags_NoPopupHierarchy)
        .value("FOCUSED_FLAGS_DOCK_HIERARCHY", ImGuiFocusedFlags_::ImGuiFocusedFlags_DockHierarchy)
        .value("FOCUSED_FLAGS_ROOT_AND_CHILD_WINDOWS", ImGuiFocusedFlags_::ImGuiFocusedFlags_RootAndChildWindows)
        .export_values();
    py::enum_<ImGuiHoveredFlags_>(_imgui, "HoveredFlags", py::arithmetic())
        .value("HOVERED_FLAGS_NONE", ImGuiHoveredFlags_::ImGuiHoveredFlags_None)
        .value("HOVERED_FLAGS_CHILD_WINDOWS", ImGuiHoveredFlags_::ImGuiHoveredFlags_ChildWindows)
        .value("HOVERED_FLAGS_ROOT_WINDOW", ImGuiHoveredFlags_::ImGuiHoveredFlags_RootWindow)
        .value("HOVERED_FLAGS_ANY_WINDOW", ImGuiHoveredFlags_::ImGuiHoveredFlags_AnyWindow)
        .value("HOVERED_FLAGS_NO_POPUP_HIERARCHY", ImGuiHoveredFlags_::ImGuiHoveredFlags_NoPopupHierarchy)
        .value("HOVERED_FLAGS_DOCK_HIERARCHY", ImGuiHoveredFlags_::ImGuiHoveredFlags_DockHierarchy)
        .value("HOVERED_FLAGS_ALLOW_WHEN_BLOCKED_BY_POPUP", ImGuiHoveredFlags_::ImGuiHoveredFlags_AllowWhenBlockedByPopup)
        .value("HOVERED_FLAGS_ALLOW_WHEN_BLOCKED_BY_ACTIVE_ITEM", ImGuiHoveredFlags_::ImGuiHoveredFlags_AllowWhenBlockedByActiveItem)
        .value("HOVERED_FLAGS_ALLOW_WHEN_OVERLAPPED_BY_ITEM", ImGuiHoveredFlags_::ImGuiHoveredFlags_AllowWhenOverlappedByItem)
        .value("HOVERED_FLAGS_ALLOW_WHEN_OVERLAPPED_BY_WINDOW", ImGuiHoveredFlags_::ImGuiHoveredFlags_AllowWhenOverlappedByWindow)
        .value("HOVERED_FLAGS_ALLOW_WHEN_DISABLED", ImGuiHoveredFlags_::ImGuiHoveredFlags_AllowWhenDisabled)
        .value("HOVERED_FLAGS_NO_NAV_OVERRIDE", ImGuiHoveredFlags_::ImGuiHoveredFlags_NoNavOverride)
        .value("HOVERED_FLAGS_ALLOW_WHEN_OVERLAPPED", ImGuiHoveredFlags_::ImGuiHoveredFlags_AllowWhenOverlapped)
        .value("HOVERED_FLAGS_RECT_ONLY", ImGuiHoveredFlags_::ImGuiHoveredFlags_RectOnly)
        .value("HOVERED_FLAGS_ROOT_AND_CHILD_WINDOWS", ImGuiHoveredFlags_::ImGuiHoveredFlags_RootAndChildWindows)
        .value("HOVERED_FLAGS_FOR_TOOLTIP", ImGuiHoveredFlags_::ImGuiHoveredFlags_ForTooltip)
        .value("HOVERED_FLAGS_STATIONARY", ImGuiHoveredFlags_::ImGuiHoveredFlags_Stationary)
        .value("HOVERED_FLAGS_DELAY_NONE", ImGuiHoveredFlags_::ImGuiHoveredFlags_DelayNone)
        .value("HOVERED_FLAGS_DELAY_SHORT", ImGuiHoveredFlags_::ImGuiHoveredFlags_DelayShort)
        .value("HOVERED_FLAGS_DELAY_NORMAL", ImGuiHoveredFlags_::ImGuiHoveredFlags_DelayNormal)
        .value("HOVERED_FLAGS_NO_SHARED_DELAY", ImGuiHoveredFlags_::ImGuiHoveredFlags_NoSharedDelay)
        .export_values();
    py::enum_<ImGuiDockNodeFlags_>(_imgui, "DockNodeFlags", py::arithmetic())
        .value("DOCK_NODE_FLAGS_NONE", ImGuiDockNodeFlags_::ImGuiDockNodeFlags_None)
        .value("DOCK_NODE_FLAGS_KEEP_ALIVE_ONLY", ImGuiDockNodeFlags_::ImGuiDockNodeFlags_KeepAliveOnly)
        .value("DOCK_NODE_FLAGS_NO_DOCKING_OVER_CENTRAL_NODE", ImGuiDockNodeFlags_::ImGuiDockNodeFlags_NoDockingOverCentralNode)
        .value("DOCK_NODE_FLAGS_PASSTHRU_CENTRAL_NODE", ImGuiDockNodeFlags_::ImGuiDockNodeFlags_PassthruCentralNode)
        .value("DOCK_NODE_FLAGS_NO_DOCKING_SPLIT", ImGuiDockNodeFlags_::ImGuiDockNodeFlags_NoDockingSplit)
        .value("DOCK_NODE_FLAGS_NO_RESIZE", ImGuiDockNodeFlags_::ImGuiDockNodeFlags_NoResize)
        .value("DOCK_NODE_FLAGS_AUTO_HIDE_TAB_BAR", ImGuiDockNodeFlags_::ImGuiDockNodeFlags_AutoHideTabBar)
        .value("DOCK_NODE_FLAGS_NO_UNDOCKING", ImGuiDockNodeFlags_::ImGuiDockNodeFlags_NoUndocking)
        .export_values();
    py::enum_<ImGuiDragDropFlags_>(_imgui, "DragDropFlags", py::arithmetic())
        .value("DRAG_DROP_FLAGS_NONE", ImGuiDragDropFlags_::ImGuiDragDropFlags_None)
        .value("DRAG_DROP_FLAGS_SOURCE_NO_PREVIEW_TOOLTIP", ImGuiDragDropFlags_::ImGuiDragDropFlags_SourceNoPreviewTooltip)
        .value("DRAG_DROP_FLAGS_SOURCE_NO_DISABLE_HOVER", ImGuiDragDropFlags_::ImGuiDragDropFlags_SourceNoDisableHover)
        .value("DRAG_DROP_FLAGS_SOURCE_NO_HOLD_TO_OPEN_OTHERS", ImGuiDragDropFlags_::ImGuiDragDropFlags_SourceNoHoldToOpenOthers)
        .value("DRAG_DROP_FLAGS_SOURCE_ALLOW_NULL_ID", ImGuiDragDropFlags_::ImGuiDragDropFlags_SourceAllowNullID)
        .value("DRAG_DROP_FLAGS_SOURCE_EXTERN", ImGuiDragDropFlags_::ImGuiDragDropFlags_SourceExtern)
        .value("DRAG_DROP_FLAGS_SOURCE_AUTO_EXPIRE_PAYLOAD", ImGuiDragDropFlags_::ImGuiDragDropFlags_SourceAutoExpirePayload)
        .value("DRAG_DROP_FLAGS_ACCEPT_BEFORE_DELIVERY", ImGuiDragDropFlags_::ImGuiDragDropFlags_AcceptBeforeDelivery)
        .value("DRAG_DROP_FLAGS_ACCEPT_NO_DRAW_DEFAULT_RECT", ImGuiDragDropFlags_::ImGuiDragDropFlags_AcceptNoDrawDefaultRect)
        .value("DRAG_DROP_FLAGS_ACCEPT_NO_PREVIEW_TOOLTIP", ImGuiDragDropFlags_::ImGuiDragDropFlags_AcceptNoPreviewTooltip)
        .value("DRAG_DROP_FLAGS_ACCEPT_PEEK_ONLY", ImGuiDragDropFlags_::ImGuiDragDropFlags_AcceptPeekOnly)
        .export_values();
    py::enum_<ImGuiDataType_>(_imgui, "DataType", py::arithmetic())
        .value("DATA_TYPE_S8", ImGuiDataType_::ImGuiDataType_S8)
        .value("DATA_TYPE_U8", ImGuiDataType_::ImGuiDataType_U8)
        .value("DATA_TYPE_S16", ImGuiDataType_::ImGuiDataType_S16)
        .value("DATA_TYPE_U16", ImGuiDataType_::ImGuiDataType_U16)
        .value("DATA_TYPE_S32", ImGuiDataType_::ImGuiDataType_S32)
        .value("DATA_TYPE_U32", ImGuiDataType_::ImGuiDataType_U32)
        .value("DATA_TYPE_S64", ImGuiDataType_::ImGuiDataType_S64)
        .value("DATA_TYPE_U64", ImGuiDataType_::ImGuiDataType_U64)
        .value("DATA_TYPE_FLOAT", ImGuiDataType_::ImGuiDataType_Float)
        .value("DATA_TYPE_DOUBLE", ImGuiDataType_::ImGuiDataType_Double)
        .value("DATA_TYPE_COUNT", ImGuiDataType_::ImGuiDataType_COUNT)
        .export_values();
    py::enum_<ImGuiDir_>(_imgui, "Dir", py::arithmetic())
        .value("DIR_NONE", ImGuiDir_::ImGuiDir_None)
        .value("DIR_LEFT", ImGuiDir_::ImGuiDir_Left)
        .value("DIR_RIGHT", ImGuiDir_::ImGuiDir_Right)
        .value("DIR_UP", ImGuiDir_::ImGuiDir_Up)
        .value("DIR_DOWN", ImGuiDir_::ImGuiDir_Down)
        .value("DIR_COUNT", ImGuiDir_::ImGuiDir_COUNT)
        .export_values();
    py::enum_<ImGuiSortDirection_>(_imgui, "SortDirection", py::arithmetic())
        .value("SORT_DIRECTION_NONE", ImGuiSortDirection_::ImGuiSortDirection_None)
        .value("SORT_DIRECTION_ASCENDING", ImGuiSortDirection_::ImGuiSortDirection_Ascending)
        .value("SORT_DIRECTION_DESCENDING", ImGuiSortDirection_::ImGuiSortDirection_Descending)
        .export_values();
    py::enum_<ImGuiKey>(_imgui, "Key", py::arithmetic())
        .value("KEY_NONE", ImGuiKey::ImGuiKey_None)
        .value("KEY_TAB", ImGuiKey::ImGuiKey_Tab)
        .value("KEY_LEFT_ARROW", ImGuiKey::ImGuiKey_LeftArrow)
        .value("KEY_RIGHT_ARROW", ImGuiKey::ImGuiKey_RightArrow)
        .value("KEY_UP_ARROW", ImGuiKey::ImGuiKey_UpArrow)
        .value("KEY_DOWN_ARROW", ImGuiKey::ImGuiKey_DownArrow)
        .value("KEY_PAGE_UP", ImGuiKey::ImGuiKey_PageUp)
        .value("KEY_PAGE_DOWN", ImGuiKey::ImGuiKey_PageDown)
        .value("KEY_HOME", ImGuiKey::ImGuiKey_Home)
        .value("KEY_END", ImGuiKey::ImGuiKey_End)
        .value("KEY_INSERT", ImGuiKey::ImGuiKey_Insert)
        .value("KEY_DELETE", ImGuiKey::ImGuiKey_Delete)
        .value("KEY_BACKSPACE", ImGuiKey::ImGuiKey_Backspace)
        .value("KEY_SPACE", ImGuiKey::ImGuiKey_Space)
        .value("KEY_ENTER", ImGuiKey::ImGuiKey_Enter)
        .value("KEY_ESCAPE", ImGuiKey::ImGuiKey_Escape)
        .value("KEY_LEFT_CTRL", ImGuiKey::ImGuiKey_LeftCtrl)
        .value("KEY_LEFT_SHIFT", ImGuiKey::ImGuiKey_LeftShift)
        .value("KEY_LEFT_ALT", ImGuiKey::ImGuiKey_LeftAlt)
        .value("KEY_LEFT_SUPER", ImGuiKey::ImGuiKey_LeftSuper)
        .value("KEY_RIGHT_CTRL", ImGuiKey::ImGuiKey_RightCtrl)
        .value("KEY_RIGHT_SHIFT", ImGuiKey::ImGuiKey_RightShift)
        .value("KEY_RIGHT_ALT", ImGuiKey::ImGuiKey_RightAlt)
        .value("KEY_RIGHT_SUPER", ImGuiKey::ImGuiKey_RightSuper)
        .value("KEY_MENU", ImGuiKey::ImGuiKey_Menu)
        .value("KEY_0", ImGuiKey::ImGuiKey_0)
        .value("KEY_1", ImGuiKey::ImGuiKey_1)
        .value("KEY_2", ImGuiKey::ImGuiKey_2)
        .value("KEY_3", ImGuiKey::ImGuiKey_3)
        .value("KEY_4", ImGuiKey::ImGuiKey_4)
        .value("KEY_5", ImGuiKey::ImGuiKey_5)
        .value("KEY_6", ImGuiKey::ImGuiKey_6)
        .value("KEY_7", ImGuiKey::ImGuiKey_7)
        .value("KEY_8", ImGuiKey::ImGuiKey_8)
        .value("KEY_9", ImGuiKey::ImGuiKey_9)
        .value("KEY_A", ImGuiKey::ImGuiKey_A)
        .value("KEY_B", ImGuiKey::ImGuiKey_B)
        .value("KEY_C", ImGuiKey::ImGuiKey_C)
        .value("KEY_D", ImGuiKey::ImGuiKey_D)
        .value("KEY_E", ImGuiKey::ImGuiKey_E)
        .value("KEY_F", ImGuiKey::ImGuiKey_F)
        .value("KEY_G", ImGuiKey::ImGuiKey_G)
        .value("KEY_H", ImGuiKey::ImGuiKey_H)
        .value("KEY_I", ImGuiKey::ImGuiKey_I)
        .value("KEY_J", ImGuiKey::ImGuiKey_J)
        .value("KEY_K", ImGuiKey::ImGuiKey_K)
        .value("KEY_L", ImGuiKey::ImGuiKey_L)
        .value("KEY_M", ImGuiKey::ImGuiKey_M)
        .value("KEY_N", ImGuiKey::ImGuiKey_N)
        .value("KEY_O", ImGuiKey::ImGuiKey_O)
        .value("KEY_P", ImGuiKey::ImGuiKey_P)
        .value("KEY_Q", ImGuiKey::ImGuiKey_Q)
        .value("KEY_R", ImGuiKey::ImGuiKey_R)
        .value("KEY_S", ImGuiKey::ImGuiKey_S)
        .value("KEY_T", ImGuiKey::ImGuiKey_T)
        .value("KEY_U", ImGuiKey::ImGuiKey_U)
        .value("KEY_V", ImGuiKey::ImGuiKey_V)
        .value("KEY_W", ImGuiKey::ImGuiKey_W)
        .value("KEY_X", ImGuiKey::ImGuiKey_X)
        .value("KEY_Y", ImGuiKey::ImGuiKey_Y)
        .value("KEY_Z", ImGuiKey::ImGuiKey_Z)
        .value("KEY_F1", ImGuiKey::ImGuiKey_F1)
        .value("KEY_F2", ImGuiKey::ImGuiKey_F2)
        .value("KEY_F3", ImGuiKey::ImGuiKey_F3)
        .value("KEY_F4", ImGuiKey::ImGuiKey_F4)
        .value("KEY_F5", ImGuiKey::ImGuiKey_F5)
        .value("KEY_F6", ImGuiKey::ImGuiKey_F6)
        .value("KEY_F7", ImGuiKey::ImGuiKey_F7)
        .value("KEY_F8", ImGuiKey::ImGuiKey_F8)
        .value("KEY_F9", ImGuiKey::ImGuiKey_F9)
        .value("KEY_F10", ImGuiKey::ImGuiKey_F10)
        .value("KEY_F11", ImGuiKey::ImGuiKey_F11)
        .value("KEY_F12", ImGuiKey::ImGuiKey_F12)
        .value("KEY_APOSTROPHE", ImGuiKey::ImGuiKey_Apostrophe)
        .value("KEY_COMMA", ImGuiKey::ImGuiKey_Comma)
        .value("KEY_MINUS", ImGuiKey::ImGuiKey_Minus)
        .value("KEY_PERIOD", ImGuiKey::ImGuiKey_Period)
        .value("KEY_SLASH", ImGuiKey::ImGuiKey_Slash)
        .value("KEY_SEMICOLON", ImGuiKey::ImGuiKey_Semicolon)
        .value("KEY_EQUAL", ImGuiKey::ImGuiKey_Equal)
        .value("KEY_LEFT_BRACKET", ImGuiKey::ImGuiKey_LeftBracket)
        .value("KEY_BACKSLASH", ImGuiKey::ImGuiKey_Backslash)
        .value("KEY_RIGHT_BRACKET", ImGuiKey::ImGuiKey_RightBracket)
        .value("KEY_GRAVE_ACCENT", ImGuiKey::ImGuiKey_GraveAccent)
        .value("KEY_CAPS_LOCK", ImGuiKey::ImGuiKey_CapsLock)
        .value("KEY_SCROLL_LOCK", ImGuiKey::ImGuiKey_ScrollLock)
        .value("KEY_NUM_LOCK", ImGuiKey::ImGuiKey_NumLock)
        .value("KEY_PRINT_SCREEN", ImGuiKey::ImGuiKey_PrintScreen)
        .value("KEY_PAUSE", ImGuiKey::ImGuiKey_Pause)
        .value("KEY_KEYPAD0", ImGuiKey::ImGuiKey_Keypad0)
        .value("KEY_KEYPAD1", ImGuiKey::ImGuiKey_Keypad1)
        .value("KEY_KEYPAD2", ImGuiKey::ImGuiKey_Keypad2)
        .value("KEY_KEYPAD3", ImGuiKey::ImGuiKey_Keypad3)
        .value("KEY_KEYPAD4", ImGuiKey::ImGuiKey_Keypad4)
        .value("KEY_KEYPAD5", ImGuiKey::ImGuiKey_Keypad5)
        .value("KEY_KEYPAD6", ImGuiKey::ImGuiKey_Keypad6)
        .value("KEY_KEYPAD7", ImGuiKey::ImGuiKey_Keypad7)
        .value("KEY_KEYPAD8", ImGuiKey::ImGuiKey_Keypad8)
        .value("KEY_KEYPAD9", ImGuiKey::ImGuiKey_Keypad9)
        .value("KEY_KEYPAD_DECIMAL", ImGuiKey::ImGuiKey_KeypadDecimal)
        .value("KEY_KEYPAD_DIVIDE", ImGuiKey::ImGuiKey_KeypadDivide)
        .value("KEY_KEYPAD_MULTIPLY", ImGuiKey::ImGuiKey_KeypadMultiply)
        .value("KEY_KEYPAD_SUBTRACT", ImGuiKey::ImGuiKey_KeypadSubtract)
        .value("KEY_KEYPAD_ADD", ImGuiKey::ImGuiKey_KeypadAdd)
        .value("KEY_KEYPAD_ENTER", ImGuiKey::ImGuiKey_KeypadEnter)
        .value("KEY_KEYPAD_EQUAL", ImGuiKey::ImGuiKey_KeypadEqual)
        .value("KEY_GAMEPAD_START", ImGuiKey::ImGuiKey_GamepadStart)
        .value("KEY_GAMEPAD_BACK", ImGuiKey::ImGuiKey_GamepadBack)
        .value("KEY_GAMEPAD_FACE_LEFT", ImGuiKey::ImGuiKey_GamepadFaceLeft)
        .value("KEY_GAMEPAD_FACE_RIGHT", ImGuiKey::ImGuiKey_GamepadFaceRight)
        .value("KEY_GAMEPAD_FACE_UP", ImGuiKey::ImGuiKey_GamepadFaceUp)
        .value("KEY_GAMEPAD_FACE_DOWN", ImGuiKey::ImGuiKey_GamepadFaceDown)
        .value("KEY_GAMEPAD_DPAD_LEFT", ImGuiKey::ImGuiKey_GamepadDpadLeft)
        .value("KEY_GAMEPAD_DPAD_RIGHT", ImGuiKey::ImGuiKey_GamepadDpadRight)
        .value("KEY_GAMEPAD_DPAD_UP", ImGuiKey::ImGuiKey_GamepadDpadUp)
        .value("KEY_GAMEPAD_DPAD_DOWN", ImGuiKey::ImGuiKey_GamepadDpadDown)
        .value("KEY_GAMEPAD_L1", ImGuiKey::ImGuiKey_GamepadL1)
        .value("KEY_GAMEPAD_R1", ImGuiKey::ImGuiKey_GamepadR1)
        .value("KEY_GAMEPAD_L2", ImGuiKey::ImGuiKey_GamepadL2)
        .value("KEY_GAMEPAD_R2", ImGuiKey::ImGuiKey_GamepadR2)
        .value("KEY_GAMEPAD_L3", ImGuiKey::ImGuiKey_GamepadL3)
        .value("KEY_GAMEPAD_R3", ImGuiKey::ImGuiKey_GamepadR3)
        .value("KEY_GAMEPAD_L_STICK_LEFT", ImGuiKey::ImGuiKey_GamepadLStickLeft)
        .value("KEY_GAMEPAD_L_STICK_RIGHT", ImGuiKey::ImGuiKey_GamepadLStickRight)
        .value("KEY_GAMEPAD_L_STICK_UP", ImGuiKey::ImGuiKey_GamepadLStickUp)
        .value("KEY_GAMEPAD_L_STICK_DOWN", ImGuiKey::ImGuiKey_GamepadLStickDown)
        .value("KEY_GAMEPAD_R_STICK_LEFT", ImGuiKey::ImGuiKey_GamepadRStickLeft)
        .value("KEY_GAMEPAD_R_STICK_RIGHT", ImGuiKey::ImGuiKey_GamepadRStickRight)
        .value("KEY_GAMEPAD_R_STICK_UP", ImGuiKey::ImGuiKey_GamepadRStickUp)
        .value("KEY_GAMEPAD_R_STICK_DOWN", ImGuiKey::ImGuiKey_GamepadRStickDown)
        .value("KEY_MOUSE_LEFT", ImGuiKey::ImGuiKey_MouseLeft)
        .value("KEY_MOUSE_RIGHT", ImGuiKey::ImGuiKey_MouseRight)
        .value("KEY_MOUSE_MIDDLE", ImGuiKey::ImGuiKey_MouseMiddle)
        .value("KEY_MOUSE_X1", ImGuiKey::ImGuiKey_MouseX1)
        .value("KEY_MOUSE_X2", ImGuiKey::ImGuiKey_MouseX2)
        .value("KEY_MOUSE_WHEEL_X", ImGuiKey::ImGuiKey_MouseWheelX)
        .value("KEY_MOUSE_WHEEL_Y", ImGuiKey::ImGuiKey_MouseWheelY)
        .value("KEY_RESERVED_FOR_MOD_CTRL", ImGuiKey::ImGuiKey_ReservedForModCtrl)
        .value("KEY_RESERVED_FOR_MOD_SHIFT", ImGuiKey::ImGuiKey_ReservedForModShift)
        .value("KEY_RESERVED_FOR_MOD_ALT", ImGuiKey::ImGuiKey_ReservedForModAlt)
        .value("KEY_RESERVED_FOR_MOD_SUPER", ImGuiKey::ImGuiKey_ReservedForModSuper)
        .value("KEY_COUNT", ImGuiKey::ImGuiKey_COUNT)
        .value("MOD_NONE", ImGuiKey::ImGuiMod_None)
        .value("MOD_CTRL", ImGuiKey::ImGuiMod_Ctrl)
        .value("MOD_SHIFT", ImGuiKey::ImGuiMod_Shift)
        .value("MOD_ALT", ImGuiKey::ImGuiMod_Alt)
        .value("MOD_SUPER", ImGuiKey::ImGuiMod_Super)
        .value("MOD_SHORTCUT", ImGuiKey::ImGuiMod_Shortcut)
        .value("MOD_MASK", ImGuiKey::ImGuiMod_Mask_)
        .value("KEY_NAMED_KEY_BEGIN", ImGuiKey::ImGuiKey_NamedKey_BEGIN)
        .value("KEY_NAMED_KEY_END", ImGuiKey::ImGuiKey_NamedKey_END)
        .value("KEY_NAMED_KEY_COUNT", ImGuiKey::ImGuiKey_NamedKey_COUNT)
        .value("KEY_KEYS_DATA_SIZE", ImGuiKey::ImGuiKey_KeysData_SIZE)
        .value("KEY_KEYS_DATA_OFFSET", ImGuiKey::ImGuiKey_KeysData_OFFSET)
        .export_values();
    py::enum_<ImGuiConfigFlags_>(_imgui, "ConfigFlags", py::arithmetic())
        .value("CONFIG_FLAGS_NONE", ImGuiConfigFlags_::ImGuiConfigFlags_None)
        .value("CONFIG_FLAGS_NAV_ENABLE_KEYBOARD", ImGuiConfigFlags_::ImGuiConfigFlags_NavEnableKeyboard)
        .value("CONFIG_FLAGS_NAV_ENABLE_GAMEPAD", ImGuiConfigFlags_::ImGuiConfigFlags_NavEnableGamepad)
        .value("CONFIG_FLAGS_NAV_ENABLE_SET_MOUSE_POS", ImGuiConfigFlags_::ImGuiConfigFlags_NavEnableSetMousePos)
        .value("CONFIG_FLAGS_NAV_NO_CAPTURE_KEYBOARD", ImGuiConfigFlags_::ImGuiConfigFlags_NavNoCaptureKeyboard)
        .value("CONFIG_FLAGS_NO_MOUSE", ImGuiConfigFlags_::ImGuiConfigFlags_NoMouse)
        .value("CONFIG_FLAGS_NO_MOUSE_CURSOR_CHANGE", ImGuiConfigFlags_::ImGuiConfigFlags_NoMouseCursorChange)
        .value("CONFIG_FLAGS_DOCKING_ENABLE", ImGuiConfigFlags_::ImGuiConfigFlags_DockingEnable)
        .value("CONFIG_FLAGS_VIEWPORTS_ENABLE", ImGuiConfigFlags_::ImGuiConfigFlags_ViewportsEnable)
        .value("CONFIG_FLAGS_DPI_ENABLE_SCALE_VIEWPORTS", ImGuiConfigFlags_::ImGuiConfigFlags_DpiEnableScaleViewports)
        .value("CONFIG_FLAGS_DPI_ENABLE_SCALE_FONTS", ImGuiConfigFlags_::ImGuiConfigFlags_DpiEnableScaleFonts)
        .value("CONFIG_FLAGS_IS_SRGB", ImGuiConfigFlags_::ImGuiConfigFlags_IsSRGB)
        .value("CONFIG_FLAGS_IS_TOUCH_SCREEN", ImGuiConfigFlags_::ImGuiConfigFlags_IsTouchScreen)
        .export_values();
    py::enum_<ImGuiBackendFlags_>(_imgui, "BackendFlags", py::arithmetic())
        .value("BACKEND_FLAGS_NONE", ImGuiBackendFlags_::ImGuiBackendFlags_None)
        .value("BACKEND_FLAGS_HAS_GAMEPAD", ImGuiBackendFlags_::ImGuiBackendFlags_HasGamepad)
        .value("BACKEND_FLAGS_HAS_MOUSE_CURSORS", ImGuiBackendFlags_::ImGuiBackendFlags_HasMouseCursors)
        .value("BACKEND_FLAGS_HAS_SET_MOUSE_POS", ImGuiBackendFlags_::ImGuiBackendFlags_HasSetMousePos)
        .value("BACKEND_FLAGS_RENDERER_HAS_VTX_OFFSET", ImGuiBackendFlags_::ImGuiBackendFlags_RendererHasVtxOffset)
        .value("BACKEND_FLAGS_PLATFORM_HAS_VIEWPORTS", ImGuiBackendFlags_::ImGuiBackendFlags_PlatformHasViewports)
        .value("BACKEND_FLAGS_HAS_MOUSE_HOVERED_VIEWPORT", ImGuiBackendFlags_::ImGuiBackendFlags_HasMouseHoveredViewport)
        .value("BACKEND_FLAGS_RENDERER_HAS_VIEWPORTS", ImGuiBackendFlags_::ImGuiBackendFlags_RendererHasViewports)
        .export_values();
    py::enum_<ImGuiCol_>(_imgui, "Col", py::arithmetic())
        .value("COL_TEXT", ImGuiCol_::ImGuiCol_Text)
        .value("COL_TEXT_DISABLED", ImGuiCol_::ImGuiCol_TextDisabled)
        .value("COL_WINDOW_BG", ImGuiCol_::ImGuiCol_WindowBg)
        .value("COL_CHILD_BG", ImGuiCol_::ImGuiCol_ChildBg)
        .value("COL_POPUP_BG", ImGuiCol_::ImGuiCol_PopupBg)
        .value("COL_BORDER", ImGuiCol_::ImGuiCol_Border)
        .value("COL_BORDER_SHADOW", ImGuiCol_::ImGuiCol_BorderShadow)
        .value("COL_FRAME_BG", ImGuiCol_::ImGuiCol_FrameBg)
        .value("COL_FRAME_BG_HOVERED", ImGuiCol_::ImGuiCol_FrameBgHovered)
        .value("COL_FRAME_BG_ACTIVE", ImGuiCol_::ImGuiCol_FrameBgActive)
        .value("COL_TITLE_BG", ImGuiCol_::ImGuiCol_TitleBg)
        .value("COL_TITLE_BG_ACTIVE", ImGuiCol_::ImGuiCol_TitleBgActive)
        .value("COL_TITLE_BG_COLLAPSED", ImGuiCol_::ImGuiCol_TitleBgCollapsed)
        .value("COL_MENU_BAR_BG", ImGuiCol_::ImGuiCol_MenuBarBg)
        .value("COL_SCROLLBAR_BG", ImGuiCol_::ImGuiCol_ScrollbarBg)
        .value("COL_SCROLLBAR_GRAB", ImGuiCol_::ImGuiCol_ScrollbarGrab)
        .value("COL_SCROLLBAR_GRAB_HOVERED", ImGuiCol_::ImGuiCol_ScrollbarGrabHovered)
        .value("COL_SCROLLBAR_GRAB_ACTIVE", ImGuiCol_::ImGuiCol_ScrollbarGrabActive)
        .value("COL_CHECK_MARK", ImGuiCol_::ImGuiCol_CheckMark)
        .value("COL_SLIDER_GRAB", ImGuiCol_::ImGuiCol_SliderGrab)
        .value("COL_SLIDER_GRAB_ACTIVE", ImGuiCol_::ImGuiCol_SliderGrabActive)
        .value("COL_BUTTON", ImGuiCol_::ImGuiCol_Button)
        .value("COL_BUTTON_HOVERED", ImGuiCol_::ImGuiCol_ButtonHovered)
        .value("COL_BUTTON_ACTIVE", ImGuiCol_::ImGuiCol_ButtonActive)
        .value("COL_HEADER", ImGuiCol_::ImGuiCol_Header)
        .value("COL_HEADER_HOVERED", ImGuiCol_::ImGuiCol_HeaderHovered)
        .value("COL_HEADER_ACTIVE", ImGuiCol_::ImGuiCol_HeaderActive)
        .value("COL_SEPARATOR", ImGuiCol_::ImGuiCol_Separator)
        .value("COL_SEPARATOR_HOVERED", ImGuiCol_::ImGuiCol_SeparatorHovered)
        .value("COL_SEPARATOR_ACTIVE", ImGuiCol_::ImGuiCol_SeparatorActive)
        .value("COL_RESIZE_GRIP", ImGuiCol_::ImGuiCol_ResizeGrip)
        .value("COL_RESIZE_GRIP_HOVERED", ImGuiCol_::ImGuiCol_ResizeGripHovered)
        .value("COL_RESIZE_GRIP_ACTIVE", ImGuiCol_::ImGuiCol_ResizeGripActive)
        .value("COL_TAB", ImGuiCol_::ImGuiCol_Tab)
        .value("COL_TAB_HOVERED", ImGuiCol_::ImGuiCol_TabHovered)
        .value("COL_TAB_ACTIVE", ImGuiCol_::ImGuiCol_TabActive)
        .value("COL_TAB_UNFOCUSED", ImGuiCol_::ImGuiCol_TabUnfocused)
        .value("COL_TAB_UNFOCUSED_ACTIVE", ImGuiCol_::ImGuiCol_TabUnfocusedActive)
        .value("COL_DOCKING_PREVIEW", ImGuiCol_::ImGuiCol_DockingPreview)
        .value("COL_DOCKING_EMPTY_BG", ImGuiCol_::ImGuiCol_DockingEmptyBg)
        .value("COL_PLOT_LINES", ImGuiCol_::ImGuiCol_PlotLines)
        .value("COL_PLOT_LINES_HOVERED", ImGuiCol_::ImGuiCol_PlotLinesHovered)
        .value("COL_PLOT_HISTOGRAM", ImGuiCol_::ImGuiCol_PlotHistogram)
        .value("COL_PLOT_HISTOGRAM_HOVERED", ImGuiCol_::ImGuiCol_PlotHistogramHovered)
        .value("COL_TABLE_HEADER_BG", ImGuiCol_::ImGuiCol_TableHeaderBg)
        .value("COL_TABLE_BORDER_STRONG", ImGuiCol_::ImGuiCol_TableBorderStrong)
        .value("COL_TABLE_BORDER_LIGHT", ImGuiCol_::ImGuiCol_TableBorderLight)
        .value("COL_TABLE_ROW_BG", ImGuiCol_::ImGuiCol_TableRowBg)
        .value("COL_TABLE_ROW_BG_ALT", ImGuiCol_::ImGuiCol_TableRowBgAlt)
        .value("COL_TEXT_SELECTED_BG", ImGuiCol_::ImGuiCol_TextSelectedBg)
        .value("COL_DRAG_DROP_TARGET", ImGuiCol_::ImGuiCol_DragDropTarget)
        .value("COL_NAV_HIGHLIGHT", ImGuiCol_::ImGuiCol_NavHighlight)
        .value("COL_NAV_WINDOWING_HIGHLIGHT", ImGuiCol_::ImGuiCol_NavWindowingHighlight)
        .value("COL_NAV_WINDOWING_DIM_BG", ImGuiCol_::ImGuiCol_NavWindowingDimBg)
        .value("COL_MODAL_WINDOW_DIM_BG", ImGuiCol_::ImGuiCol_ModalWindowDimBg)
        .value("COL_COUNT", ImGuiCol_::ImGuiCol_COUNT)
        .export_values();
    py::enum_<ImGuiStyleVar_>(_imgui, "StyleVar", py::arithmetic())
        .value("STYLE_VAR_ALPHA", ImGuiStyleVar_::ImGuiStyleVar_Alpha)
        .value("STYLE_VAR_DISABLED_ALPHA", ImGuiStyleVar_::ImGuiStyleVar_DisabledAlpha)
        .value("STYLE_VAR_WINDOW_PADDING", ImGuiStyleVar_::ImGuiStyleVar_WindowPadding)
        .value("STYLE_VAR_WINDOW_ROUNDING", ImGuiStyleVar_::ImGuiStyleVar_WindowRounding)
        .value("STYLE_VAR_WINDOW_BORDER_SIZE", ImGuiStyleVar_::ImGuiStyleVar_WindowBorderSize)
        .value("STYLE_VAR_WINDOW_MIN_SIZE", ImGuiStyleVar_::ImGuiStyleVar_WindowMinSize)
        .value("STYLE_VAR_WINDOW_TITLE_ALIGN", ImGuiStyleVar_::ImGuiStyleVar_WindowTitleAlign)
        .value("STYLE_VAR_CHILD_ROUNDING", ImGuiStyleVar_::ImGuiStyleVar_ChildRounding)
        .value("STYLE_VAR_CHILD_BORDER_SIZE", ImGuiStyleVar_::ImGuiStyleVar_ChildBorderSize)
        .value("STYLE_VAR_POPUP_ROUNDING", ImGuiStyleVar_::ImGuiStyleVar_PopupRounding)
        .value("STYLE_VAR_POPUP_BORDER_SIZE", ImGuiStyleVar_::ImGuiStyleVar_PopupBorderSize)
        .value("STYLE_VAR_FRAME_PADDING", ImGuiStyleVar_::ImGuiStyleVar_FramePadding)
        .value("STYLE_VAR_FRAME_ROUNDING", ImGuiStyleVar_::ImGuiStyleVar_FrameRounding)
        .value("STYLE_VAR_FRAME_BORDER_SIZE", ImGuiStyleVar_::ImGuiStyleVar_FrameBorderSize)
        .value("STYLE_VAR_ITEM_SPACING", ImGuiStyleVar_::ImGuiStyleVar_ItemSpacing)
        .value("STYLE_VAR_ITEM_INNER_SPACING", ImGuiStyleVar_::ImGuiStyleVar_ItemInnerSpacing)
        .value("STYLE_VAR_INDENT_SPACING", ImGuiStyleVar_::ImGuiStyleVar_IndentSpacing)
        .value("STYLE_VAR_CELL_PADDING", ImGuiStyleVar_::ImGuiStyleVar_CellPadding)
        .value("STYLE_VAR_SCROLLBAR_SIZE", ImGuiStyleVar_::ImGuiStyleVar_ScrollbarSize)
        .value("STYLE_VAR_SCROLLBAR_ROUNDING", ImGuiStyleVar_::ImGuiStyleVar_ScrollbarRounding)
        .value("STYLE_VAR_GRAB_MIN_SIZE", ImGuiStyleVar_::ImGuiStyleVar_GrabMinSize)
        .value("STYLE_VAR_GRAB_ROUNDING", ImGuiStyleVar_::ImGuiStyleVar_GrabRounding)
        .value("STYLE_VAR_TAB_ROUNDING", ImGuiStyleVar_::ImGuiStyleVar_TabRounding)
        .value("STYLE_VAR_TAB_BAR_BORDER_SIZE", ImGuiStyleVar_::ImGuiStyleVar_TabBarBorderSize)
        .value("STYLE_VAR_BUTTON_TEXT_ALIGN", ImGuiStyleVar_::ImGuiStyleVar_ButtonTextAlign)
        .value("STYLE_VAR_SELECTABLE_TEXT_ALIGN", ImGuiStyleVar_::ImGuiStyleVar_SelectableTextAlign)
        .value("STYLE_VAR_SEPARATOR_TEXT_BORDER_SIZE", ImGuiStyleVar_::ImGuiStyleVar_SeparatorTextBorderSize)
        .value("STYLE_VAR_SEPARATOR_TEXT_ALIGN", ImGuiStyleVar_::ImGuiStyleVar_SeparatorTextAlign)
        .value("STYLE_VAR_SEPARATOR_TEXT_PADDING", ImGuiStyleVar_::ImGuiStyleVar_SeparatorTextPadding)
        .value("STYLE_VAR_DOCKING_SEPARATOR_SIZE", ImGuiStyleVar_::ImGuiStyleVar_DockingSeparatorSize)
        .value("STYLE_VAR_COUNT", ImGuiStyleVar_::ImGuiStyleVar_COUNT)
        .export_values();
    py::enum_<ImGuiButtonFlags_>(_imgui, "ButtonFlags", py::arithmetic())
        .value("BUTTON_FLAGS_NONE", ImGuiButtonFlags_::ImGuiButtonFlags_None)
        .value("BUTTON_FLAGS_MOUSE_BUTTON_LEFT", ImGuiButtonFlags_::ImGuiButtonFlags_MouseButtonLeft)
        .value("BUTTON_FLAGS_MOUSE_BUTTON_RIGHT", ImGuiButtonFlags_::ImGuiButtonFlags_MouseButtonRight)
        .value("BUTTON_FLAGS_MOUSE_BUTTON_MIDDLE", ImGuiButtonFlags_::ImGuiButtonFlags_MouseButtonMiddle)
        .value("BUTTON_FLAGS_MOUSE_BUTTON_MASK", ImGuiButtonFlags_::ImGuiButtonFlags_MouseButtonMask_)
        .value("BUTTON_FLAGS_MOUSE_BUTTON_DEFAULT", ImGuiButtonFlags_::ImGuiButtonFlags_MouseButtonDefault_)
        .export_values();
    py::enum_<ImGuiColorEditFlags_>(_imgui, "ColorEditFlags", py::arithmetic())
        .value("COLOR_EDIT_FLAGS_NONE", ImGuiColorEditFlags_::ImGuiColorEditFlags_None)
        .value("COLOR_EDIT_FLAGS_NO_ALPHA", ImGuiColorEditFlags_::ImGuiColorEditFlags_NoAlpha)
        .value("COLOR_EDIT_FLAGS_NO_PICKER", ImGuiColorEditFlags_::ImGuiColorEditFlags_NoPicker)
        .value("COLOR_EDIT_FLAGS_NO_OPTIONS", ImGuiColorEditFlags_::ImGuiColorEditFlags_NoOptions)
        .value("COLOR_EDIT_FLAGS_NO_SMALL_PREVIEW", ImGuiColorEditFlags_::ImGuiColorEditFlags_NoSmallPreview)
        .value("COLOR_EDIT_FLAGS_NO_INPUTS", ImGuiColorEditFlags_::ImGuiColorEditFlags_NoInputs)
        .value("COLOR_EDIT_FLAGS_NO_TOOLTIP", ImGuiColorEditFlags_::ImGuiColorEditFlags_NoTooltip)
        .value("COLOR_EDIT_FLAGS_NO_LABEL", ImGuiColorEditFlags_::ImGuiColorEditFlags_NoLabel)
        .value("COLOR_EDIT_FLAGS_NO_SIDE_PREVIEW", ImGuiColorEditFlags_::ImGuiColorEditFlags_NoSidePreview)
        .value("COLOR_EDIT_FLAGS_NO_DRAG_DROP", ImGuiColorEditFlags_::ImGuiColorEditFlags_NoDragDrop)
        .value("COLOR_EDIT_FLAGS_NO_BORDER", ImGuiColorEditFlags_::ImGuiColorEditFlags_NoBorder)
        .value("COLOR_EDIT_FLAGS_ALPHA_BAR", ImGuiColorEditFlags_::ImGuiColorEditFlags_AlphaBar)
        .value("COLOR_EDIT_FLAGS_ALPHA_PREVIEW", ImGuiColorEditFlags_::ImGuiColorEditFlags_AlphaPreview)
        .value("COLOR_EDIT_FLAGS_ALPHA_PREVIEW_HALF", ImGuiColorEditFlags_::ImGuiColorEditFlags_AlphaPreviewHalf)
        .value("COLOR_EDIT_FLAGS_HDR", ImGuiColorEditFlags_::ImGuiColorEditFlags_HDR)
        .value("COLOR_EDIT_FLAGS_DISPLAY_RGB", ImGuiColorEditFlags_::ImGuiColorEditFlags_DisplayRGB)
        .value("COLOR_EDIT_FLAGS_DISPLAY_HSV", ImGuiColorEditFlags_::ImGuiColorEditFlags_DisplayHSV)
        .value("COLOR_EDIT_FLAGS_DISPLAY_HEX", ImGuiColorEditFlags_::ImGuiColorEditFlags_DisplayHex)
        .value("COLOR_EDIT_FLAGS_UINT8", ImGuiColorEditFlags_::ImGuiColorEditFlags_Uint8)
        .value("COLOR_EDIT_FLAGS_FLOAT", ImGuiColorEditFlags_::ImGuiColorEditFlags_Float)
        .value("COLOR_EDIT_FLAGS_PICKER_HUE_BAR", ImGuiColorEditFlags_::ImGuiColorEditFlags_PickerHueBar)
        .value("COLOR_EDIT_FLAGS_PICKER_HUE_WHEEL", ImGuiColorEditFlags_::ImGuiColorEditFlags_PickerHueWheel)
        .value("COLOR_EDIT_FLAGS_INPUT_RGB", ImGuiColorEditFlags_::ImGuiColorEditFlags_InputRGB)
        .value("COLOR_EDIT_FLAGS_INPUT_HSV", ImGuiColorEditFlags_::ImGuiColorEditFlags_InputHSV)
        .value("COLOR_EDIT_FLAGS_DEFAULT_OPTIONS", ImGuiColorEditFlags_::ImGuiColorEditFlags_DefaultOptions_)
        .value("COLOR_EDIT_FLAGS_DISPLAY_MASK", ImGuiColorEditFlags_::ImGuiColorEditFlags_DisplayMask_)
        .value("COLOR_EDIT_FLAGS_DATA_TYPE_MASK", ImGuiColorEditFlags_::ImGuiColorEditFlags_DataTypeMask_)
        .value("COLOR_EDIT_FLAGS_PICKER_MASK", ImGuiColorEditFlags_::ImGuiColorEditFlags_PickerMask_)
        .value("COLOR_EDIT_FLAGS_INPUT_MASK", ImGuiColorEditFlags_::ImGuiColorEditFlags_InputMask_)
        .export_values();
    py::enum_<ImGuiSliderFlags_>(_imgui, "SliderFlags", py::arithmetic())
        .value("SLIDER_FLAGS_NONE", ImGuiSliderFlags_::ImGuiSliderFlags_None)
        .value("SLIDER_FLAGS_ALWAYS_CLAMP", ImGuiSliderFlags_::ImGuiSliderFlags_AlwaysClamp)
        .value("SLIDER_FLAGS_LOGARITHMIC", ImGuiSliderFlags_::ImGuiSliderFlags_Logarithmic)
        .value("SLIDER_FLAGS_NO_ROUND_TO_FORMAT", ImGuiSliderFlags_::ImGuiSliderFlags_NoRoundToFormat)
        .value("SLIDER_FLAGS_NO_INPUT", ImGuiSliderFlags_::ImGuiSliderFlags_NoInput)
        .value("SLIDER_FLAGS_INVALID_MASK", ImGuiSliderFlags_::ImGuiSliderFlags_InvalidMask_)
        .export_values();
    py::enum_<ImGuiMouseButton_>(_imgui, "MouseButton", py::arithmetic())
        .value("MOUSE_BUTTON_LEFT", ImGuiMouseButton_::ImGuiMouseButton_Left)
        .value("MOUSE_BUTTON_RIGHT", ImGuiMouseButton_::ImGuiMouseButton_Right)
        .value("MOUSE_BUTTON_MIDDLE", ImGuiMouseButton_::ImGuiMouseButton_Middle)
        .value("MOUSE_BUTTON_COUNT", ImGuiMouseButton_::ImGuiMouseButton_COUNT)
        .export_values();
    py::enum_<ImGuiMouseCursor_>(_imgui, "MouseCursor", py::arithmetic())
        .value("MOUSE_CURSOR_NONE", ImGuiMouseCursor_::ImGuiMouseCursor_None)
        .value("MOUSE_CURSOR_ARROW", ImGuiMouseCursor_::ImGuiMouseCursor_Arrow)
        .value("MOUSE_CURSOR_TEXT_INPUT", ImGuiMouseCursor_::ImGuiMouseCursor_TextInput)
        .value("MOUSE_CURSOR_RESIZE_ALL", ImGuiMouseCursor_::ImGuiMouseCursor_ResizeAll)
        .value("MOUSE_CURSOR_RESIZE_NS", ImGuiMouseCursor_::ImGuiMouseCursor_ResizeNS)
        .value("MOUSE_CURSOR_RESIZE_EW", ImGuiMouseCursor_::ImGuiMouseCursor_ResizeEW)
        .value("MOUSE_CURSOR_RESIZE_NESW", ImGuiMouseCursor_::ImGuiMouseCursor_ResizeNESW)
        .value("MOUSE_CURSOR_RESIZE_NWSE", ImGuiMouseCursor_::ImGuiMouseCursor_ResizeNWSE)
        .value("MOUSE_CURSOR_HAND", ImGuiMouseCursor_::ImGuiMouseCursor_Hand)
        .value("MOUSE_CURSOR_NOT_ALLOWED", ImGuiMouseCursor_::ImGuiMouseCursor_NotAllowed)
        .value("MOUSE_CURSOR_COUNT", ImGuiMouseCursor_::ImGuiMouseCursor_COUNT)
        .export_values();
    py::enum_<ImGuiMouseSource>(_imgui, "MouseSource", py::arithmetic())
        .value("MOUSE_SOURCE_MOUSE", ImGuiMouseSource::ImGuiMouseSource_Mouse)
        .value("MOUSE_SOURCE_TOUCH_SCREEN", ImGuiMouseSource::ImGuiMouseSource_TouchScreen)
        .value("MOUSE_SOURCE_PEN", ImGuiMouseSource::ImGuiMouseSource_Pen)
        .value("MOUSE_SOURCE_COUNT", ImGuiMouseSource::ImGuiMouseSource_COUNT)
        .export_values();
    py::enum_<ImGuiCond_>(_imgui, "Cond", py::arithmetic())
        .value("COND_NONE", ImGuiCond_::ImGuiCond_None)
        .value("COND_ALWAYS", ImGuiCond_::ImGuiCond_Always)
        .value("COND_ONCE", ImGuiCond_::ImGuiCond_Once)
        .value("COND_FIRST_USE_EVER", ImGuiCond_::ImGuiCond_FirstUseEver)
        .value("COND_APPEARING", ImGuiCond_::ImGuiCond_Appearing)
        .export_values();
    PYCLASS_BEGIN(_imgui, ImNewWrapper, NewWrapper)
    PYCLASS_END(_imgui, ImNewWrapper, NewWrapper)
    PYCLASS_BEGIN(_imgui, ImGuiStyle, Style)
        Style.def_readwrite("alpha", &ImGuiStyle::Alpha);
        Style.def_readwrite("disabled_alpha", &ImGuiStyle::DisabledAlpha);
        Style.def_readwrite("window_padding", &ImGuiStyle::WindowPadding);
        Style.def_readwrite("window_rounding", &ImGuiStyle::WindowRounding);
        Style.def_readwrite("window_border_size", &ImGuiStyle::WindowBorderSize);
        Style.def_readwrite("window_min_size", &ImGuiStyle::WindowMinSize);
        Style.def_readwrite("window_title_align", &ImGuiStyle::WindowTitleAlign);
        Style.def_readwrite("window_menu_button_position", &ImGuiStyle::WindowMenuButtonPosition);
        Style.def_readwrite("child_rounding", &ImGuiStyle::ChildRounding);
        Style.def_readwrite("child_border_size", &ImGuiStyle::ChildBorderSize);
        Style.def_readwrite("popup_rounding", &ImGuiStyle::PopupRounding);
        Style.def_readwrite("popup_border_size", &ImGuiStyle::PopupBorderSize);
        Style.def_readwrite("frame_padding", &ImGuiStyle::FramePadding);
        Style.def_readwrite("frame_rounding", &ImGuiStyle::FrameRounding);
        Style.def_readwrite("frame_border_size", &ImGuiStyle::FrameBorderSize);
        Style.def_readwrite("item_spacing", &ImGuiStyle::ItemSpacing);
        Style.def_readwrite("item_inner_spacing", &ImGuiStyle::ItemInnerSpacing);
        Style.def_readwrite("cell_padding", &ImGuiStyle::CellPadding);
        Style.def_readwrite("touch_extra_padding", &ImGuiStyle::TouchExtraPadding);
        Style.def_readwrite("indent_spacing", &ImGuiStyle::IndentSpacing);
        Style.def_readwrite("columns_min_spacing", &ImGuiStyle::ColumnsMinSpacing);
        Style.def_readwrite("scrollbar_size", &ImGuiStyle::ScrollbarSize);
        Style.def_readwrite("scrollbar_rounding", &ImGuiStyle::ScrollbarRounding);
        Style.def_readwrite("grab_min_size", &ImGuiStyle::GrabMinSize);
        Style.def_readwrite("grab_rounding", &ImGuiStyle::GrabRounding);
        Style.def_readwrite("log_slider_deadzone", &ImGuiStyle::LogSliderDeadzone);
        Style.def_readwrite("tab_rounding", &ImGuiStyle::TabRounding);
        Style.def_readwrite("tab_border_size", &ImGuiStyle::TabBorderSize);
        Style.def_readwrite("tab_min_width_for_close_button", &ImGuiStyle::TabMinWidthForCloseButton);
        Style.def_readwrite("tab_bar_border_size", &ImGuiStyle::TabBarBorderSize);
        Style.def_readwrite("color_button_position", &ImGuiStyle::ColorButtonPosition);
        Style.def_readwrite("button_text_align", &ImGuiStyle::ButtonTextAlign);
        Style.def_readwrite("selectable_text_align", &ImGuiStyle::SelectableTextAlign);
        Style.def_readwrite("separator_text_border_size", &ImGuiStyle::SeparatorTextBorderSize);
        Style.def_readwrite("separator_text_align", &ImGuiStyle::SeparatorTextAlign);
        Style.def_readwrite("separator_text_padding", &ImGuiStyle::SeparatorTextPadding);
        Style.def_readwrite("display_window_padding", &ImGuiStyle::DisplayWindowPadding);
        Style.def_readwrite("display_safe_area_padding", &ImGuiStyle::DisplaySafeAreaPadding);
        Style.def_readwrite("docking_separator_size", &ImGuiStyle::DockingSeparatorSize);
        Style.def_readwrite("mouse_cursor_scale", &ImGuiStyle::MouseCursorScale);
        Style.def_readwrite("anti_aliased_lines", &ImGuiStyle::AntiAliasedLines);
        Style.def_readwrite("anti_aliased_lines_use_tex", &ImGuiStyle::AntiAliasedLinesUseTex);
        Style.def_readwrite("anti_aliased_fill", &ImGuiStyle::AntiAliasedFill);
        Style.def_readwrite("curve_tessellation_tol", &ImGuiStyle::CurveTessellationTol);
        Style.def_readwrite("circle_tessellation_max_error", &ImGuiStyle::CircleTessellationMaxError);
        Style.def_readwrite("hover_stationary_delay", &ImGuiStyle::HoverStationaryDelay);
        Style.def_readwrite("hover_delay_short", &ImGuiStyle::HoverDelayShort);
        Style.def_readwrite("hover_delay_normal", &ImGuiStyle::HoverDelayNormal);
        Style.def_readwrite("hover_flags_for_tooltip_mouse", &ImGuiStyle::HoverFlagsForTooltipMouse);
        Style.def_readwrite("hover_flags_for_tooltip_nav", &ImGuiStyle::HoverFlagsForTooltipNav);
        Style.def(py::init<>());
        Style.def("scale_all_sizes", &ImGuiStyle::ScaleAllSizes
        , py::arg("scale_factor")
        , py::return_value_policy::automatic_reference);
        
    PYCLASS_END(_imgui, ImGuiStyle, Style)
    PYCLASS_BEGIN(_imgui, ImGuiKeyData, KeyData)
        KeyData.def_readwrite("down", &ImGuiKeyData::Down);
        KeyData.def_readwrite("down_duration", &ImGuiKeyData::DownDuration);
        KeyData.def_readwrite("down_duration_prev", &ImGuiKeyData::DownDurationPrev);
        KeyData.def_readwrite("analog_value", &ImGuiKeyData::AnalogValue);
    PYCLASS_END(_imgui, ImGuiKeyData, KeyData)
    PYCLASS_BEGIN(_imgui, ImGuiIO, IO)
        IO.def_readwrite("config_flags", &ImGuiIO::ConfigFlags);
        IO.def_readwrite("backend_flags", &ImGuiIO::BackendFlags);
        IO.def_readwrite("display_size", &ImGuiIO::DisplaySize);
        IO.def_readwrite("delta_time", &ImGuiIO::DeltaTime);
        IO.def_readwrite("ini_saving_rate", &ImGuiIO::IniSavingRate);
        IO.def_property("ini_filename",
            [](const ImGuiIO& self){ return self.IniFilename; },
            [](ImGuiIO& self, const char* source){ self.IniFilename = strdup(source); }
        );
        IO.def_property("log_filename",
            [](const ImGuiIO& self){ return self.LogFilename; },
            [](ImGuiIO& self, const char* source){ self.LogFilename = strdup(source); }
        );
        IO.def_readwrite("user_data", &ImGuiIO::UserData);
        IO.def_readwrite("fonts", &ImGuiIO::Fonts);
        IO.def_readwrite("font_global_scale", &ImGuiIO::FontGlobalScale);
        IO.def_readwrite("font_allow_user_scaling", &ImGuiIO::FontAllowUserScaling);
        IO.def_readwrite("font_default", &ImGuiIO::FontDefault);
        IO.def_readwrite("display_framebuffer_scale", &ImGuiIO::DisplayFramebufferScale);
        IO.def_readwrite("config_docking_no_split", &ImGuiIO::ConfigDockingNoSplit);
        IO.def_readwrite("config_docking_with_shift", &ImGuiIO::ConfigDockingWithShift);
        IO.def_readwrite("config_docking_always_tab_bar", &ImGuiIO::ConfigDockingAlwaysTabBar);
        IO.def_readwrite("config_docking_transparent_payload", &ImGuiIO::ConfigDockingTransparentPayload);
        IO.def_readwrite("config_viewports_no_auto_merge", &ImGuiIO::ConfigViewportsNoAutoMerge);
        IO.def_readwrite("config_viewports_no_task_bar_icon", &ImGuiIO::ConfigViewportsNoTaskBarIcon);
        IO.def_readwrite("config_viewports_no_decoration", &ImGuiIO::ConfigViewportsNoDecoration);
        IO.def_readwrite("config_viewports_no_default_parent", &ImGuiIO::ConfigViewportsNoDefaultParent);
        IO.def_readwrite("mouse_draw_cursor", &ImGuiIO::MouseDrawCursor);
        IO.def_readwrite("config_mac_osx_behaviors", &ImGuiIO::ConfigMacOSXBehaviors);
        IO.def_readwrite("config_input_trickle_event_queue", &ImGuiIO::ConfigInputTrickleEventQueue);
        IO.def_readwrite("config_input_text_cursor_blink", &ImGuiIO::ConfigInputTextCursorBlink);
        IO.def_readwrite("config_input_text_enter_keep_active", &ImGuiIO::ConfigInputTextEnterKeepActive);
        IO.def_readwrite("config_drag_click_to_input_text", &ImGuiIO::ConfigDragClickToInputText);
        IO.def_readwrite("config_windows_resize_from_edges", &ImGuiIO::ConfigWindowsResizeFromEdges);
        IO.def_readwrite("config_windows_move_from_title_bar_only", &ImGuiIO::ConfigWindowsMoveFromTitleBarOnly);
        IO.def_readwrite("config_memory_compact_timer", &ImGuiIO::ConfigMemoryCompactTimer);
        IO.def_readwrite("mouse_double_click_time", &ImGuiIO::MouseDoubleClickTime);
        IO.def_readwrite("mouse_double_click_max_dist", &ImGuiIO::MouseDoubleClickMaxDist);
        IO.def_readwrite("mouse_drag_threshold", &ImGuiIO::MouseDragThreshold);
        IO.def_readwrite("key_repeat_delay", &ImGuiIO::KeyRepeatDelay);
        IO.def_readwrite("key_repeat_rate", &ImGuiIO::KeyRepeatRate);
        IO.def_readwrite("config_debug_begin_return_value_once", &ImGuiIO::ConfigDebugBeginReturnValueOnce);
        IO.def_readwrite("config_debug_begin_return_value_loop", &ImGuiIO::ConfigDebugBeginReturnValueLoop);
        IO.def_readwrite("config_debug_ignore_focus_loss", &ImGuiIO::ConfigDebugIgnoreFocusLoss);
        IO.def_readwrite("config_debug_ini_settings", &ImGuiIO::ConfigDebugIniSettings);
        IO.def_property("backend_platform_name",
            [](const ImGuiIO& self){ return self.BackendPlatformName; },
            [](ImGuiIO& self, const char* source){ self.BackendPlatformName = strdup(source); }
        );
        IO.def_property("backend_renderer_name",
            [](const ImGuiIO& self){ return self.BackendRendererName; },
            [](ImGuiIO& self, const char* source){ self.BackendRendererName = strdup(source); }
        );
        IO.def_readwrite("backend_platform_user_data", &ImGuiIO::BackendPlatformUserData);
        IO.def_readwrite("backend_renderer_user_data", &ImGuiIO::BackendRendererUserData);
        IO.def_readwrite("backend_language_user_data", &ImGuiIO::BackendLanguageUserData);
        IO.def_readwrite("clipboard_user_data", &ImGuiIO::ClipboardUserData);
        IO.def_readwrite("platform_locale_decimal_point", &ImGuiIO::PlatformLocaleDecimalPoint);
        IO.def("add_key_event", &ImGuiIO::AddKeyEvent
        , py::arg("key")
        , py::arg("down")
        , py::return_value_policy::automatic_reference);
        
        IO.def("add_key_analog_event", &ImGuiIO::AddKeyAnalogEvent
        , py::arg("key")
        , py::arg("down")
        , py::arg("v")
        , py::return_value_policy::automatic_reference);
        
        IO.def("add_mouse_pos_event", &ImGuiIO::AddMousePosEvent
        , py::arg("x")
        , py::arg("y")
        , py::return_value_policy::automatic_reference);
        
        IO.def("add_mouse_button_event", &ImGuiIO::AddMouseButtonEvent
        , py::arg("button")
        , py::arg("down")
        , py::return_value_policy::automatic_reference);
        
        IO.def("add_mouse_wheel_event", &ImGuiIO::AddMouseWheelEvent
        , py::arg("wheel_x")
        , py::arg("wheel_y")
        , py::return_value_policy::automatic_reference);
        
        IO.def("add_mouse_source_event", &ImGuiIO::AddMouseSourceEvent
        , py::arg("source")
        , py::return_value_policy::automatic_reference);
        
        IO.def("add_mouse_viewport_event", &ImGuiIO::AddMouseViewportEvent
        , py::arg("id")
        , py::return_value_policy::automatic_reference);
        
        IO.def("add_focus_event", &ImGuiIO::AddFocusEvent
        , py::arg("focused")
        , py::return_value_policy::automatic_reference);
        
        IO.def("add_input_character", &ImGuiIO::AddInputCharacter
        , py::arg("c")
        , py::return_value_policy::automatic_reference);
        
        IO.def("add_input_character_utf16", &ImGuiIO::AddInputCharacterUTF16
        , py::arg("c")
        , py::return_value_policy::automatic_reference);
        
        IO.def("add_input_characters_utf8", &ImGuiIO::AddInputCharactersUTF8
        , py::arg("str")
        , py::return_value_policy::automatic_reference);
        
        IO.def("set_key_event_native_data", &ImGuiIO::SetKeyEventNativeData
        , py::arg("key")
        , py::arg("native_keycode")
        , py::arg("native_scancode")
        , py::arg("native_legacy_index") = -1
        , py::return_value_policy::automatic_reference);
        
        IO.def("set_app_accepting_events", &ImGuiIO::SetAppAcceptingEvents
        , py::arg("accepting_events")
        , py::return_value_policy::automatic_reference);
        
        IO.def("clear_events_queue", &ImGuiIO::ClearEventsQueue
        , py::return_value_policy::automatic_reference);
        
        IO.def("clear_input_keys", &ImGuiIO::ClearInputKeys
        , py::return_value_policy::automatic_reference);
        
        IO.def_readwrite("want_capture_mouse", &ImGuiIO::WantCaptureMouse);
        IO.def_readwrite("want_capture_keyboard", &ImGuiIO::WantCaptureKeyboard);
        IO.def_readwrite("want_text_input", &ImGuiIO::WantTextInput);
        IO.def_readwrite("want_set_mouse_pos", &ImGuiIO::WantSetMousePos);
        IO.def_readwrite("want_save_ini_settings", &ImGuiIO::WantSaveIniSettings);
        IO.def_readwrite("nav_active", &ImGuiIO::NavActive);
        IO.def_readwrite("nav_visible", &ImGuiIO::NavVisible);
        IO.def_readwrite("framerate", &ImGuiIO::Framerate);
        IO.def_readwrite("metrics_render_vertices", &ImGuiIO::MetricsRenderVertices);
        IO.def_readwrite("metrics_render_indices", &ImGuiIO::MetricsRenderIndices);
        IO.def_readwrite("metrics_render_windows", &ImGuiIO::MetricsRenderWindows);
        IO.def_readwrite("metrics_active_windows", &ImGuiIO::MetricsActiveWindows);
        IO.def_readwrite("mouse_delta", &ImGuiIO::MouseDelta);
        IO.def_readwrite("mouse_pos", &ImGuiIO::MousePos);
        IO.def_readonly("mouse_down", &ImGuiIO::MouseDown);
        IO.def_readwrite("mouse_wheel", &ImGuiIO::MouseWheel);
        IO.def_readwrite("mouse_wheel_h", &ImGuiIO::MouseWheelH);
        IO.def_readwrite("mouse_source", &ImGuiIO::MouseSource);
        IO.def_readwrite("mouse_hovered_viewport", &ImGuiIO::MouseHoveredViewport);
        IO.def_readwrite("key_ctrl", &ImGuiIO::KeyCtrl);
        IO.def_readwrite("key_shift", &ImGuiIO::KeyShift);
        IO.def_readwrite("key_alt", &ImGuiIO::KeyAlt);
        IO.def_readwrite("key_super", &ImGuiIO::KeySuper);
        IO.def_readwrite("key_mods", &ImGuiIO::KeyMods);
        IO.def_readonly("keys_data", &ImGuiIO::KeysData);
        IO.def_readwrite("want_capture_mouse_unless_popup_close", &ImGuiIO::WantCaptureMouseUnlessPopupClose);
        IO.def_readwrite("mouse_pos_prev", &ImGuiIO::MousePosPrev);
        IO.def_readonly("mouse_clicked_pos", &ImGuiIO::MouseClickedPos);
        IO.def_readonly("mouse_clicked_time", &ImGuiIO::MouseClickedTime);
        IO.def_readonly("mouse_clicked", &ImGuiIO::MouseClicked);
        IO.def_readonly("mouse_double_clicked", &ImGuiIO::MouseDoubleClicked);
        IO.def_readonly("mouse_clicked_count", &ImGuiIO::MouseClickedCount);
        IO.def_readonly("mouse_clicked_last_count", &ImGuiIO::MouseClickedLastCount);
        IO.def_readonly("mouse_released", &ImGuiIO::MouseReleased);
        IO.def_readonly("mouse_down_owned", &ImGuiIO::MouseDownOwned);
        IO.def_readonly("mouse_down_owned_unless_popup_close", &ImGuiIO::MouseDownOwnedUnlessPopupClose);
        IO.def_readwrite("mouse_wheel_request_axis_swap", &ImGuiIO::MouseWheelRequestAxisSwap);
        IO.def_readonly("mouse_down_duration", &ImGuiIO::MouseDownDuration);
        IO.def_readonly("mouse_down_duration_prev", &ImGuiIO::MouseDownDurationPrev);
        IO.def_readonly("mouse_drag_max_distance_abs", &ImGuiIO::MouseDragMaxDistanceAbs);
        IO.def_readonly("mouse_drag_max_distance_sqr", &ImGuiIO::MouseDragMaxDistanceSqr);
        IO.def_readwrite("pen_pressure", &ImGuiIO::PenPressure);
        IO.def_readwrite("app_focus_lost", &ImGuiIO::AppFocusLost);
        IO.def_readwrite("app_accepting_events", &ImGuiIO::AppAcceptingEvents);
        IO.def_readwrite("backend_using_legacy_key_arrays", &ImGuiIO::BackendUsingLegacyKeyArrays);
        IO.def_readwrite("backend_using_legacy_nav_input_array", &ImGuiIO::BackendUsingLegacyNavInputArray);
        IO.def_readwrite("input_queue_surrogate", &ImGuiIO::InputQueueSurrogate);
        IO.def_readwrite("input_queue_characters", &ImGuiIO::InputQueueCharacters);
        IO.def(py::init<>());
    PYCLASS_END(_imgui, ImGuiIO, IO)
    PYCLASS_BEGIN(_imgui, ImGuiInputTextCallbackData, InputTextCallbackData)
        InputTextCallbackData.def_readwrite("event_flag", &ImGuiInputTextCallbackData::EventFlag);
        InputTextCallbackData.def_readwrite("flags", &ImGuiInputTextCallbackData::Flags);
        InputTextCallbackData.def_readwrite("user_data", &ImGuiInputTextCallbackData::UserData);
        InputTextCallbackData.def_readwrite("event_char", &ImGuiInputTextCallbackData::EventChar);
        InputTextCallbackData.def_readwrite("event_key", &ImGuiInputTextCallbackData::EventKey);
        InputTextCallbackData.def_property("buf",
            [](const ImGuiInputTextCallbackData& self){ return self.Buf; },
            [](ImGuiInputTextCallbackData& self, const char* source){ self.Buf = strdup(source); }
        );
        InputTextCallbackData.def_readwrite("buf_text_len", &ImGuiInputTextCallbackData::BufTextLen);
        InputTextCallbackData.def_readwrite("buf_size", &ImGuiInputTextCallbackData::BufSize);
        InputTextCallbackData.def_readwrite("buf_dirty", &ImGuiInputTextCallbackData::BufDirty);
        InputTextCallbackData.def_readwrite("cursor_pos", &ImGuiInputTextCallbackData::CursorPos);
        InputTextCallbackData.def_readwrite("selection_start", &ImGuiInputTextCallbackData::SelectionStart);
        InputTextCallbackData.def_readwrite("selection_end", &ImGuiInputTextCallbackData::SelectionEnd);
        InputTextCallbackData.def(py::init<>());
        InputTextCallbackData.def("delete_chars", &ImGuiInputTextCallbackData::DeleteChars
        , py::arg("pos")
        , py::arg("bytes_count")
        , py::return_value_policy::automatic_reference);
        
        InputTextCallbackData.def("insert_chars", &ImGuiInputTextCallbackData::InsertChars
        , py::arg("pos")
        , py::arg("text")
        , py::arg("text_end") = nullptr
        , py::return_value_policy::automatic_reference);
        
        InputTextCallbackData.def("select_all", &ImGuiInputTextCallbackData::SelectAll
        , py::return_value_policy::automatic_reference);
        
        InputTextCallbackData.def("clear_selection", &ImGuiInputTextCallbackData::ClearSelection
        , py::return_value_policy::automatic_reference);
        
        InputTextCallbackData.def("has_selection", &ImGuiInputTextCallbackData::HasSelection
        , py::return_value_policy::automatic_reference);
        
    PYCLASS_END(_imgui, ImGuiInputTextCallbackData, InputTextCallbackData)
    PYCLASS_BEGIN(_imgui, ImGuiSizeCallbackData, SizeCallbackData)
        SizeCallbackData.def_readwrite("user_data", &ImGuiSizeCallbackData::UserData);
        SizeCallbackData.def_readwrite("pos", &ImGuiSizeCallbackData::Pos);
        SizeCallbackData.def_readwrite("current_size", &ImGuiSizeCallbackData::CurrentSize);
        SizeCallbackData.def_readwrite("desired_size", &ImGuiSizeCallbackData::DesiredSize);
    PYCLASS_END(_imgui, ImGuiSizeCallbackData, SizeCallbackData)
    PYCLASS_BEGIN(_imgui, ImGuiWindowClass, WindowClass)
        WindowClass.def_readwrite("class_id", &ImGuiWindowClass::ClassId);
        WindowClass.def_readwrite("parent_viewport_id", &ImGuiWindowClass::ParentViewportId);
        WindowClass.def_readwrite("viewport_flags_override_set", &ImGuiWindowClass::ViewportFlagsOverrideSet);
        WindowClass.def_readwrite("viewport_flags_override_clear", &ImGuiWindowClass::ViewportFlagsOverrideClear);
        WindowClass.def_readwrite("tab_item_flags_override_set", &ImGuiWindowClass::TabItemFlagsOverrideSet);
        WindowClass.def_readwrite("dock_node_flags_override_set", &ImGuiWindowClass::DockNodeFlagsOverrideSet);
        WindowClass.def_readwrite("docking_always_tab_bar", &ImGuiWindowClass::DockingAlwaysTabBar);
        WindowClass.def_readwrite("docking_allow_unclassed", &ImGuiWindowClass::DockingAllowUnclassed);
        WindowClass.def(py::init<>());
    PYCLASS_END(_imgui, ImGuiWindowClass, WindowClass)
    PYCLASS_BEGIN(_imgui, ImGuiPayload, Payload)
        Payload.def_readwrite("data", &ImGuiPayload::Data);
        Payload.def_readwrite("data_size", &ImGuiPayload::DataSize);
        Payload.def_readwrite("source_id", &ImGuiPayload::SourceId);
        Payload.def_readwrite("source_parent_id", &ImGuiPayload::SourceParentId);
        Payload.def_readwrite("data_frame_count", &ImGuiPayload::DataFrameCount);
        Payload.def_readonly("data_type", &ImGuiPayload::DataType);
        Payload.def_readwrite("preview", &ImGuiPayload::Preview);
        Payload.def_readwrite("delivery", &ImGuiPayload::Delivery);
        Payload.def(py::init<>());
        Payload.def("clear", &ImGuiPayload::Clear
        , py::return_value_policy::automatic_reference);
        
        Payload.def("is_data_type", &ImGuiPayload::IsDataType
        , py::arg("type")
        , py::return_value_policy::automatic_reference);
        
        Payload.def("is_preview", &ImGuiPayload::IsPreview
        , py::return_value_policy::automatic_reference);
        
        Payload.def("is_delivery", &ImGuiPayload::IsDelivery
        , py::return_value_policy::automatic_reference);
        
    PYCLASS_END(_imgui, ImGuiPayload, Payload)
    PYCLASS_BEGIN(_imgui, ImGuiTableColumnSortSpecs, TableColumnSortSpecs)
        TableColumnSortSpecs.def_readwrite("column_user_id", &ImGuiTableColumnSortSpecs::ColumnUserID);
        TableColumnSortSpecs.def_readwrite("column_index", &ImGuiTableColumnSortSpecs::ColumnIndex);
        TableColumnSortSpecs.def_readwrite("sort_order", &ImGuiTableColumnSortSpecs::SortOrder);
        TableColumnSortSpecs.def(py::init<>());
    PYCLASS_END(_imgui, ImGuiTableColumnSortSpecs, TableColumnSortSpecs)
    PYCLASS_BEGIN(_imgui, ImGuiTableSortSpecs, TableSortSpecs)
        TableSortSpecs.def_readwrite("specs", &ImGuiTableSortSpecs::Specs);
        TableSortSpecs.def_readwrite("specs_count", &ImGuiTableSortSpecs::SpecsCount);
        TableSortSpecs.def_readwrite("specs_dirty", &ImGuiTableSortSpecs::SpecsDirty);
        TableSortSpecs.def(py::init<>());
    PYCLASS_END(_imgui, ImGuiTableSortSpecs, TableSortSpecs)
    PYCLASS_BEGIN(_imgui, ImGuiOnceUponAFrame, OnceUponAFrame)
        OnceUponAFrame.def(py::init<>());
        OnceUponAFrame.def_readwrite("ref_frame", &ImGuiOnceUponAFrame::RefFrame);
    PYCLASS_END(_imgui, ImGuiOnceUponAFrame, OnceUponAFrame)
    PYCLASS_BEGIN(_imgui, ImGuiTextFilter, TextFilter)
        TextFilter.def(py::init<const char *>()
        , py::arg("default_filter") = nullptr
        );
        TextFilter.def("draw", &ImGuiTextFilter::Draw
        , py::arg("label") = nullptr
        , py::arg("width") = 0.0f
        , py::return_value_policy::automatic_reference);
        
        TextFilter.def("pass_filter", &ImGuiTextFilter::PassFilter
        , py::arg("text")
        , py::arg("text_end") = nullptr
        , py::return_value_policy::automatic_reference);
        
        TextFilter.def("build", &ImGuiTextFilter::Build
        , py::return_value_policy::automatic_reference);
        
        TextFilter.def("clear", &ImGuiTextFilter::Clear
        , py::return_value_policy::automatic_reference);
        
        TextFilter.def("is_active", &ImGuiTextFilter::IsActive
        , py::return_value_policy::automatic_reference);
        
        PYCLASS_BEGIN(_imgui, ImGuiTextFilter::ImGuiTextRange, TextFilterTextRange)
            TextFilterTextRange.def_property("b",
                [](const ImGuiTextFilter::ImGuiTextRange& self){ return self.b; },
                [](ImGuiTextFilter::ImGuiTextRange& self, const char* source){ self.b = strdup(source); }
            );
            TextFilterTextRange.def_property("e",
                [](const ImGuiTextFilter::ImGuiTextRange& self){ return self.e; },
                [](ImGuiTextFilter::ImGuiTextRange& self, const char* source){ self.e = strdup(source); }
            );
            TextFilterTextRange.def(py::init<>());
            TextFilterTextRange.def("empty", &ImGuiTextFilter::ImGuiTextRange::empty
            , py::return_value_policy::automatic_reference);
            
            TextFilterTextRange.def("split", &ImGuiTextFilter::ImGuiTextRange::split
            , py::arg("separator")
            , py::arg("out")
            , py::return_value_policy::automatic_reference);
            
        PYCLASS_END(_imgui, ImGuiTextFilter::ImGuiTextRange, TextFilterTextRange)
        TextFilter.def_readonly("input_buf", &ImGuiTextFilter::InputBuf);
        TextFilter.def_readwrite("count_grep", &ImGuiTextFilter::CountGrep);
    PYCLASS_END(_imgui, ImGuiTextFilter, TextFilter)
    PYCLASS_BEGIN(_imgui, ImGuiStorage, Storage)
        PYCLASS_BEGIN(_imgui, ImGuiStorage::ImGuiStoragePair, StorageStoragePair)
            StorageStoragePair.def_readwrite("key", &ImGuiStorage::ImGuiStoragePair::key);
            StorageStoragePair.def(py::init<unsigned int, int>()
            , py::arg("_key")
            , py::arg("_val_i")
            );
        PYCLASS_END(_imgui, ImGuiStorage::ImGuiStoragePair, StorageStoragePair)
        Storage.def("clear", &ImGuiStorage::Clear
        , py::return_value_policy::automatic_reference);
        
        Storage.def("get_int", &ImGuiStorage::GetInt
        , py::arg("key")
        , py::arg("default_val") = 0
        , py::return_value_policy::automatic_reference);
        
        Storage.def("set_int", &ImGuiStorage::SetInt
        , py::arg("key")
        , py::arg("val")
        , py::return_value_policy::automatic_reference);
        
        Storage.def("get_bool", &ImGuiStorage::GetBool
        , py::arg("key")
        , py::arg("default_val") = false
        , py::return_value_policy::automatic_reference);
        
        Storage.def("set_bool", &ImGuiStorage::SetBool
        , py::arg("key")
        , py::arg("val")
        , py::return_value_policy::automatic_reference);
        
        Storage.def("get_float", &ImGuiStorage::GetFloat
        , py::arg("key")
        , py::arg("default_val") = 0.0f
        , py::return_value_policy::automatic_reference);
        
        Storage.def("set_float", &ImGuiStorage::SetFloat
        , py::arg("key")
        , py::arg("val")
        , py::return_value_policy::automatic_reference);
        
        Storage.def("get_void_ptr", &ImGuiStorage::GetVoidPtr
        , py::arg("key")
        , py::return_value_policy::automatic_reference);
        
        Storage.def("set_void_ptr", &ImGuiStorage::SetVoidPtr
        , py::arg("key")
        , py::arg("val")
        , py::return_value_policy::automatic_reference);
        
        Storage.def("get_int_ref", &ImGuiStorage::GetIntRef
        , py::arg("key")
        , py::arg("default_val") = 0
        , py::return_value_policy::automatic_reference);
        
        Storage.def("get_bool_ref", &ImGuiStorage::GetBoolRef
        , py::arg("key")
        , py::arg("default_val") = false
        , py::return_value_policy::automatic_reference);
        
        Storage.def("get_float_ref", &ImGuiStorage::GetFloatRef
        , py::arg("key")
        , py::arg("default_val") = 0.0f
        , py::return_value_policy::automatic_reference);
        
        Storage.def("get_void_ptr_ref", &ImGuiStorage::GetVoidPtrRef
        , py::arg("key")
        , py::arg("default_val") = nullptr
        , py::return_value_policy::automatic_reference);
        
        Storage.def("set_all_int", &ImGuiStorage::SetAllInt
        , py::arg("val")
        , py::return_value_policy::automatic_reference);
        
        Storage.def("build_sort_by_key", &ImGuiStorage::BuildSortByKey
        , py::return_value_policy::automatic_reference);
        
    PYCLASS_END(_imgui, ImGuiStorage, Storage)
    PYCLASS_BEGIN(_imgui, ImColor, Color)
        Color.def_readwrite("value", &ImColor::Value);
        Color.def(py::init<>());
        Color.def("set_hsv", &ImColor::SetHSV
        , py::arg("h")
        , py::arg("s")
        , py::arg("v")
        , py::arg("a") = 1.0f
        , py::return_value_policy::automatic_reference);
        
    PYCLASS_END(_imgui, ImColor, Color)
    PYCLASS_BEGIN(_imgui, ImDrawCmd, DrawCmd)
        DrawCmd.def_readwrite("clip_rect", &ImDrawCmd::ClipRect);
        DrawCmd.def_readwrite("texture_id", &ImDrawCmd::TextureId);
        DrawCmd.def_readwrite("vtx_offset", &ImDrawCmd::VtxOffset);
        DrawCmd.def_readwrite("idx_offset", &ImDrawCmd::IdxOffset);
        DrawCmd.def_readwrite("elem_count", &ImDrawCmd::ElemCount);
        DrawCmd.def_readwrite("user_callback_data", &ImDrawCmd::UserCallbackData);
        DrawCmd.def(py::init<>());
        DrawCmd.def("get_tex_id", &ImDrawCmd::GetTexID
        , py::return_value_policy::automatic_reference);
        
    PYCLASS_END(_imgui, ImDrawCmd, DrawCmd)
    PYCLASS_BEGIN(_imgui, ImDrawVert, DrawVert)
        DrawVert.def_readwrite("pos", &ImDrawVert::pos);
        DrawVert.def_readwrite("uv", &ImDrawVert::uv);
        DrawVert.def_readwrite("col", &ImDrawVert::col);
    PYCLASS_END(_imgui, ImDrawVert, DrawVert)
    PYCLASS_BEGIN(_imgui, ImDrawCmdHeader, DrawCmdHeader)
        DrawCmdHeader.def_readwrite("clip_rect", &ImDrawCmdHeader::ClipRect);
        DrawCmdHeader.def_readwrite("texture_id", &ImDrawCmdHeader::TextureId);
        DrawCmdHeader.def_readwrite("vtx_offset", &ImDrawCmdHeader::VtxOffset);
    PYCLASS_END(_imgui, ImDrawCmdHeader, DrawCmdHeader)
    PYCLASS_BEGIN(_imgui, ImDrawChannel, DrawChannel)
    PYCLASS_END(_imgui, ImDrawChannel, DrawChannel)
    PYCLASS_BEGIN(_imgui, ImDrawListSplitter, DrawListSplitter)
        DrawListSplitter.def(py::init<>());
        DrawListSplitter.def("clear", &ImDrawListSplitter::Clear
        , py::return_value_policy::automatic_reference);
        
        DrawListSplitter.def("clear_free_memory", &ImDrawListSplitter::ClearFreeMemory
        , py::return_value_policy::automatic_reference);
        
        DrawListSplitter.def("split", &ImDrawListSplitter::Split
        , py::arg("draw_list")
        , py::arg("count")
        , py::return_value_policy::automatic_reference);
        
        DrawListSplitter.def("merge", &ImDrawListSplitter::Merge
        , py::arg("draw_list")
        , py::return_value_policy::automatic_reference);
        
        DrawListSplitter.def("set_current_channel", &ImDrawListSplitter::SetCurrentChannel
        , py::arg("draw_list")
        , py::arg("channel_idx")
        , py::return_value_policy::automatic_reference);
        
    PYCLASS_END(_imgui, ImDrawListSplitter, DrawListSplitter)
    py::enum_<ImDrawFlags_>(_imgui, "DrawFlags", py::arithmetic())
        .value("DRAW_FLAGS_NONE", ImDrawFlags_::ImDrawFlags_None)
        .value("DRAW_FLAGS_CLOSED", ImDrawFlags_::ImDrawFlags_Closed)
        .value("DRAW_FLAGS_ROUND_CORNERS_TOP_LEFT", ImDrawFlags_::ImDrawFlags_RoundCornersTopLeft)
        .value("DRAW_FLAGS_ROUND_CORNERS_TOP_RIGHT", ImDrawFlags_::ImDrawFlags_RoundCornersTopRight)
        .value("DRAW_FLAGS_ROUND_CORNERS_BOTTOM_LEFT", ImDrawFlags_::ImDrawFlags_RoundCornersBottomLeft)
        .value("DRAW_FLAGS_ROUND_CORNERS_BOTTOM_RIGHT", ImDrawFlags_::ImDrawFlags_RoundCornersBottomRight)
        .value("DRAW_FLAGS_ROUND_CORNERS_NONE", ImDrawFlags_::ImDrawFlags_RoundCornersNone)
        .value("DRAW_FLAGS_ROUND_CORNERS_TOP", ImDrawFlags_::ImDrawFlags_RoundCornersTop)
        .value("DRAW_FLAGS_ROUND_CORNERS_BOTTOM", ImDrawFlags_::ImDrawFlags_RoundCornersBottom)
        .value("DRAW_FLAGS_ROUND_CORNERS_LEFT", ImDrawFlags_::ImDrawFlags_RoundCornersLeft)
        .value("DRAW_FLAGS_ROUND_CORNERS_RIGHT", ImDrawFlags_::ImDrawFlags_RoundCornersRight)
        .value("DRAW_FLAGS_ROUND_CORNERS_ALL", ImDrawFlags_::ImDrawFlags_RoundCornersAll)
        .value("DRAW_FLAGS_ROUND_CORNERS_DEFAULT", ImDrawFlags_::ImDrawFlags_RoundCornersDefault_)
        .value("DRAW_FLAGS_ROUND_CORNERS_MASK", ImDrawFlags_::ImDrawFlags_RoundCornersMask_)
        .export_values();
    py::enum_<ImDrawListFlags_>(_imgui, "DrawListFlags", py::arithmetic())
        .value("DRAW_LIST_FLAGS_NONE", ImDrawListFlags_::ImDrawListFlags_None)
        .value("DRAW_LIST_FLAGS_ANTI_ALIASED_LINES", ImDrawListFlags_::ImDrawListFlags_AntiAliasedLines)
        .value("DRAW_LIST_FLAGS_ANTI_ALIASED_LINES_USE_TEX", ImDrawListFlags_::ImDrawListFlags_AntiAliasedLinesUseTex)
        .value("DRAW_LIST_FLAGS_ANTI_ALIASED_FILL", ImDrawListFlags_::ImDrawListFlags_AntiAliasedFill)
        .value("DRAW_LIST_FLAGS_ALLOW_VTX_OFFSET", ImDrawListFlags_::ImDrawListFlags_AllowVtxOffset)
        .export_values();
    PYCLASS_BEGIN(_imgui, ImDrawList, DrawList)
        DrawList.def_readwrite("cmd_buffer", &ImDrawList::CmdBuffer);
        DrawList.def_readwrite("idx_buffer", &ImDrawList::IdxBuffer);
        DrawList.def_readwrite("vtx_buffer", &ImDrawList::VtxBuffer);
        DrawList.def_readwrite("flags", &ImDrawList::Flags);
        DrawList.def(py::init<ImDrawListSharedData *>()
        , py::arg("shared_data")
        );
        DrawList.def("push_clip_rect", &ImDrawList::PushClipRect
        , py::arg("clip_rect_min")
        , py::arg("clip_rect_max")
        , py::arg("intersect_with_current_clip_rect") = false
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("push_clip_rect_full_screen", &ImDrawList::PushClipRectFullScreen
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("pop_clip_rect", &ImDrawList::PopClipRect
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("push_texture_id", &ImDrawList::PushTextureID
        , py::arg("texture_id")
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("pop_texture_id", &ImDrawList::PopTextureID
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("get_clip_rect_min", &ImDrawList::GetClipRectMin
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("get_clip_rect_max", &ImDrawList::GetClipRectMax
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("add_line", &ImDrawList::AddLine
        , py::arg("p1")
        , py::arg("p2")
        , py::arg("col")
        , py::arg("thickness") = 1.0f
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("add_rect", &ImDrawList::AddRect
        , py::arg("p_min")
        , py::arg("p_max")
        , py::arg("col")
        , py::arg("rounding") = 0.0f
        , py::arg("flags") = 0
        , py::arg("thickness") = 1.0f
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("add_rect_filled", &ImDrawList::AddRectFilled
        , py::arg("p_min")
        , py::arg("p_max")
        , py::arg("col")
        , py::arg("rounding") = 0.0f
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("add_rect_filled_multi_color", &ImDrawList::AddRectFilledMultiColor
        , py::arg("p_min")
        , py::arg("p_max")
        , py::arg("col_upr_left")
        , py::arg("col_upr_right")
        , py::arg("col_bot_right")
        , py::arg("col_bot_left")
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("add_quad", &ImDrawList::AddQuad
        , py::arg("p1")
        , py::arg("p2")
        , py::arg("p3")
        , py::arg("p4")
        , py::arg("col")
        , py::arg("thickness") = 1.0f
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("add_quad_filled", &ImDrawList::AddQuadFilled
        , py::arg("p1")
        , py::arg("p2")
        , py::arg("p3")
        , py::arg("p4")
        , py::arg("col")
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("add_triangle", &ImDrawList::AddTriangle
        , py::arg("p1")
        , py::arg("p2")
        , py::arg("p3")
        , py::arg("col")
        , py::arg("thickness") = 1.0f
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("add_triangle_filled", &ImDrawList::AddTriangleFilled
        , py::arg("p1")
        , py::arg("p2")
        , py::arg("p3")
        , py::arg("col")
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("add_circle", &ImDrawList::AddCircle
        , py::arg("center")
        , py::arg("radius")
        , py::arg("col")
        , py::arg("num_segments") = 0
        , py::arg("thickness") = 1.0f
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("add_circle_filled", &ImDrawList::AddCircleFilled
        , py::arg("center")
        , py::arg("radius")
        , py::arg("col")
        , py::arg("num_segments") = 0
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("add_ngon", &ImDrawList::AddNgon
        , py::arg("center")
        , py::arg("radius")
        , py::arg("col")
        , py::arg("num_segments")
        , py::arg("thickness") = 1.0f
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("add_ngon_filled", &ImDrawList::AddNgonFilled
        , py::arg("center")
        , py::arg("radius")
        , py::arg("col")
        , py::arg("num_segments")
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("add_ellipse", &ImDrawList::AddEllipse
        , py::arg("center")
        , py::arg("radius_x")
        , py::arg("radius_y")
        , py::arg("col")
        , py::arg("rot") = 0.0f
        , py::arg("num_segments") = 0
        , py::arg("thickness") = 1.0f
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("add_ellipse_filled", &ImDrawList::AddEllipseFilled
        , py::arg("center")
        , py::arg("radius_x")
        , py::arg("radius_y")
        , py::arg("col")
        , py::arg("rot") = 0.0f
        , py::arg("num_segments") = 0
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("add_text", py::overload_cast<const ImVec2 &, unsigned int, const char *, const char *>(&ImDrawList::AddText)
        , py::arg("pos")
        , py::arg("col")
        , py::arg("text_begin")
        , py::arg("text_end") = nullptr
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("add_polyline", &ImDrawList::AddPolyline
        , py::arg("points")
        , py::arg("num_points")
        , py::arg("col")
        , py::arg("flags")
        , py::arg("thickness")
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("add_convex_poly_filled", &ImDrawList::AddConvexPolyFilled
        , py::arg("points")
        , py::arg("num_points")
        , py::arg("col")
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("add_bezier_cubic", &ImDrawList::AddBezierCubic
        , py::arg("p1")
        , py::arg("p2")
        , py::arg("p3")
        , py::arg("p4")
        , py::arg("col")
        , py::arg("thickness")
        , py::arg("num_segments") = 0
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("add_bezier_quadratic", &ImDrawList::AddBezierQuadratic
        , py::arg("p1")
        , py::arg("p2")
        , py::arg("p3")
        , py::arg("col")
        , py::arg("thickness")
        , py::arg("num_segments") = 0
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("add_image", &ImDrawList::AddImage
        , py::arg("user_texture_id")
        , py::arg("p_min")
        , py::arg("p_max")
        , py::arg("uv_min") = ImVec2(0,0)
        , py::arg("uv_max") = ImVec2(1,1)
        , py::arg("col") = IM_COL32_WHITE
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("add_image_quad", &ImDrawList::AddImageQuad
        , py::arg("user_texture_id")
        , py::arg("p1")
        , py::arg("p2")
        , py::arg("p3")
        , py::arg("p4")
        , py::arg("uv1") = ImVec2(0,0)
        , py::arg("uv2") = ImVec2(1,0)
        , py::arg("uv3") = ImVec2(1,1)
        , py::arg("uv4") = ImVec2(0,1)
        , py::arg("col") = IM_COL32_WHITE
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("add_image_rounded", &ImDrawList::AddImageRounded
        , py::arg("user_texture_id")
        , py::arg("p_min")
        , py::arg("p_max")
        , py::arg("uv_min")
        , py::arg("uv_max")
        , py::arg("col")
        , py::arg("rounding")
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("path_clear", &ImDrawList::PathClear
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("path_line_to", &ImDrawList::PathLineTo
        , py::arg("pos")
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("path_line_to_merge_duplicate", &ImDrawList::PathLineToMergeDuplicate
        , py::arg("pos")
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("path_fill_convex", &ImDrawList::PathFillConvex
        , py::arg("col")
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("path_stroke", &ImDrawList::PathStroke
        , py::arg("col")
        , py::arg("flags") = 0
        , py::arg("thickness") = 1.0f
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("path_arc_to", &ImDrawList::PathArcTo
        , py::arg("center")
        , py::arg("radius")
        , py::arg("a_min")
        , py::arg("a_max")
        , py::arg("num_segments") = 0
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("path_arc_to_fast", &ImDrawList::PathArcToFast
        , py::arg("center")
        , py::arg("radius")
        , py::arg("a_min_of_12")
        , py::arg("a_max_of_12")
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("path_elliptical_arc_to", &ImDrawList::PathEllipticalArcTo
        , py::arg("center")
        , py::arg("radius_x")
        , py::arg("radius_y")
        , py::arg("rot")
        , py::arg("a_min")
        , py::arg("a_max")
        , py::arg("num_segments") = 0
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("path_bezier_cubic_curve_to", &ImDrawList::PathBezierCubicCurveTo
        , py::arg("p2")
        , py::arg("p3")
        , py::arg("p4")
        , py::arg("num_segments") = 0
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("path_bezier_quadratic_curve_to", &ImDrawList::PathBezierQuadraticCurveTo
        , py::arg("p2")
        , py::arg("p3")
        , py::arg("num_segments") = 0
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("path_rect", &ImDrawList::PathRect
        , py::arg("rect_min")
        , py::arg("rect_max")
        , py::arg("rounding") = 0.0f
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("add_callback", &ImDrawList::AddCallback
        , py::arg("callback")
        , py::arg("callback_data")
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("add_draw_cmd", &ImDrawList::AddDrawCmd
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("clone_output", &ImDrawList::CloneOutput
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("channels_split", &ImDrawList::ChannelsSplit
        , py::arg("count")
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("channels_merge", &ImDrawList::ChannelsMerge
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("channels_set_current", &ImDrawList::ChannelsSetCurrent
        , py::arg("n")
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("prim_reserve", &ImDrawList::PrimReserve
        , py::arg("idx_count")
        , py::arg("vtx_count")
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("prim_unreserve", &ImDrawList::PrimUnreserve
        , py::arg("idx_count")
        , py::arg("vtx_count")
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("prim_rect", &ImDrawList::PrimRect
        , py::arg("a")
        , py::arg("b")
        , py::arg("col")
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("prim_rect_uv", &ImDrawList::PrimRectUV
        , py::arg("a")
        , py::arg("b")
        , py::arg("uv_a")
        , py::arg("uv_b")
        , py::arg("col")
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("prim_quad_uv", &ImDrawList::PrimQuadUV
        , py::arg("a")
        , py::arg("b")
        , py::arg("c")
        , py::arg("d")
        , py::arg("uv_a")
        , py::arg("uv_b")
        , py::arg("uv_c")
        , py::arg("uv_d")
        , py::arg("col")
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("prim_write_vtx", &ImDrawList::PrimWriteVtx
        , py::arg("pos")
        , py::arg("uv")
        , py::arg("col")
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("prim_write_idx", &ImDrawList::PrimWriteIdx
        , py::arg("idx")
        , py::return_value_policy::automatic_reference);
        
        DrawList.def("prim_vtx", &ImDrawList::PrimVtx
        , py::arg("pos")
        , py::arg("uv")
        , py::arg("col")
        , py::return_value_policy::automatic_reference);
        
    PYCLASS_END(_imgui, ImDrawList, DrawList)
    PYCLASS_BEGIN(_imgui, ImDrawData, DrawData)
        DrawData.def_readwrite("valid", &ImDrawData::Valid);
        DrawData.def_readwrite("cmd_lists_count", &ImDrawData::CmdListsCount);
        DrawData.def_readwrite("total_idx_count", &ImDrawData::TotalIdxCount);
        DrawData.def_readwrite("total_vtx_count", &ImDrawData::TotalVtxCount);
        DrawData.def_readwrite("display_pos", &ImDrawData::DisplayPos);
        DrawData.def_readwrite("display_size", &ImDrawData::DisplaySize);
        DrawData.def_readwrite("framebuffer_scale", &ImDrawData::FramebufferScale);
        DrawData.def_readwrite("owner_viewport", &ImDrawData::OwnerViewport);
        DrawData.def(py::init<>());
        DrawData.def("clear", &ImDrawData::Clear
        , py::return_value_policy::automatic_reference);
        
        DrawData.def("add_draw_list", &ImDrawData::AddDrawList
        , py::arg("draw_list")
        , py::return_value_policy::automatic_reference);
        
        DrawData.def("de_index_all_buffers", &ImDrawData::DeIndexAllBuffers
        , py::return_value_policy::automatic_reference);
        
        DrawData.def("scale_clip_rects", &ImDrawData::ScaleClipRects
        , py::arg("fb_scale")
        , py::return_value_policy::automatic_reference);
        
    PYCLASS_END(_imgui, ImDrawData, DrawData)
    PYCLASS_BEGIN(_imgui, ImFontConfig, FontConfig)
        FontConfig.def_readwrite("font_data", &ImFontConfig::FontData);
        FontConfig.def_readwrite("font_data_size", &ImFontConfig::FontDataSize);
        FontConfig.def_readwrite("font_data_owned_by_atlas", &ImFontConfig::FontDataOwnedByAtlas);
        FontConfig.def_readwrite("font_no", &ImFontConfig::FontNo);
        FontConfig.def_readwrite("size_pixels", &ImFontConfig::SizePixels);
        FontConfig.def_readwrite("oversample_h", &ImFontConfig::OversampleH);
        FontConfig.def_readwrite("oversample_v", &ImFontConfig::OversampleV);
        FontConfig.def_readwrite("pixel_snap_h", &ImFontConfig::PixelSnapH);
        FontConfig.def_readwrite("glyph_extra_spacing", &ImFontConfig::GlyphExtraSpacing);
        FontConfig.def_readwrite("glyph_offset", &ImFontConfig::GlyphOffset);
        FontConfig.def_readwrite("glyph_ranges", &ImFontConfig::GlyphRanges);
        FontConfig.def_readwrite("glyph_min_advance_x", &ImFontConfig::GlyphMinAdvanceX);
        FontConfig.def_readwrite("glyph_max_advance_x", &ImFontConfig::GlyphMaxAdvanceX);
        FontConfig.def_readwrite("merge_mode", &ImFontConfig::MergeMode);
        FontConfig.def_readwrite("font_builder_flags", &ImFontConfig::FontBuilderFlags);
        FontConfig.def_readwrite("rasterizer_multiply", &ImFontConfig::RasterizerMultiply);
        FontConfig.def_readwrite("ellipsis_char", &ImFontConfig::EllipsisChar);
        FontConfig.def_readonly("name", &ImFontConfig::Name);
        FontConfig.def_readwrite("dst_font", &ImFontConfig::DstFont);
        FontConfig.def(py::init<>());
    PYCLASS_END(_imgui, ImFontConfig, FontConfig)
    PYCLASS_BEGIN(_imgui, ImFontGlyph, FontGlyph)
        FontGlyph.def_readwrite("advance_x", &ImFontGlyph::AdvanceX);
        FontGlyph.def_readwrite("x0", &ImFontGlyph::X0);
        FontGlyph.def_readwrite("y0", &ImFontGlyph::Y0);
        FontGlyph.def_readwrite("x1", &ImFontGlyph::X1);
        FontGlyph.def_readwrite("y1", &ImFontGlyph::Y1);
        FontGlyph.def_readwrite("u0", &ImFontGlyph::U0);
        FontGlyph.def_readwrite("v0", &ImFontGlyph::V0);
        FontGlyph.def_readwrite("u1", &ImFontGlyph::U1);
        FontGlyph.def_readwrite("v1", &ImFontGlyph::V1);
    PYCLASS_END(_imgui, ImFontGlyph, FontGlyph)
    PYCLASS_BEGIN(_imgui, ImFontGlyphRangesBuilder, FontGlyphRangesBuilder)
        FontGlyphRangesBuilder.def_readwrite("used_chars", &ImFontGlyphRangesBuilder::UsedChars);
        FontGlyphRangesBuilder.def(py::init<>());
        FontGlyphRangesBuilder.def("clear", &ImFontGlyphRangesBuilder::Clear
        , py::return_value_policy::automatic_reference);
        
        FontGlyphRangesBuilder.def("get_bit", &ImFontGlyphRangesBuilder::GetBit
        , py::arg("n")
        , py::return_value_policy::automatic_reference);
        
        FontGlyphRangesBuilder.def("set_bit", &ImFontGlyphRangesBuilder::SetBit
        , py::arg("n")
        , py::return_value_policy::automatic_reference);
        
        FontGlyphRangesBuilder.def("add_char", &ImFontGlyphRangesBuilder::AddChar
        , py::arg("c")
        , py::return_value_policy::automatic_reference);
        
        FontGlyphRangesBuilder.def("add_text", &ImFontGlyphRangesBuilder::AddText
        , py::arg("text")
        , py::arg("text_end") = nullptr
        , py::return_value_policy::automatic_reference);
        
        FontGlyphRangesBuilder.def("add_ranges", &ImFontGlyphRangesBuilder::AddRanges
        , py::arg("ranges")
        , py::return_value_policy::automatic_reference);
        
        FontGlyphRangesBuilder.def("build_ranges", &ImFontGlyphRangesBuilder::BuildRanges
        , py::arg("out_ranges")
        , py::return_value_policy::automatic_reference);
        
    PYCLASS_END(_imgui, ImFontGlyphRangesBuilder, FontGlyphRangesBuilder)
    PYCLASS_BEGIN(_imgui, ImFontAtlasCustomRect, FontAtlasCustomRect)
        FontAtlasCustomRect.def_readwrite("width", &ImFontAtlasCustomRect::Width);
        FontAtlasCustomRect.def_readwrite("height", &ImFontAtlasCustomRect::Height);
        FontAtlasCustomRect.def_readwrite("x", &ImFontAtlasCustomRect::X);
        FontAtlasCustomRect.def_readwrite("y", &ImFontAtlasCustomRect::Y);
        FontAtlasCustomRect.def_readwrite("glyph_id", &ImFontAtlasCustomRect::GlyphID);
        FontAtlasCustomRect.def_readwrite("glyph_advance_x", &ImFontAtlasCustomRect::GlyphAdvanceX);
        FontAtlasCustomRect.def_readwrite("glyph_offset", &ImFontAtlasCustomRect::GlyphOffset);
        FontAtlasCustomRect.def_readwrite("font", &ImFontAtlasCustomRect::Font);
        FontAtlasCustomRect.def(py::init<>());
        FontAtlasCustomRect.def("is_packed", &ImFontAtlasCustomRect::IsPacked
        , py::return_value_policy::automatic_reference);
        
    PYCLASS_END(_imgui, ImFontAtlasCustomRect, FontAtlasCustomRect)
    py::enum_<ImFontAtlasFlags_>(_imgui, "FontAtlasFlags", py::arithmetic())
        .value("FONT_ATLAS_FLAGS_NONE", ImFontAtlasFlags_::ImFontAtlasFlags_None)
        .value("FONT_ATLAS_FLAGS_NO_POWER_OF_TWO_HEIGHT", ImFontAtlasFlags_::ImFontAtlasFlags_NoPowerOfTwoHeight)
        .value("FONT_ATLAS_FLAGS_NO_MOUSE_CURSORS", ImFontAtlasFlags_::ImFontAtlasFlags_NoMouseCursors)
        .value("FONT_ATLAS_FLAGS_NO_BAKED_LINES", ImFontAtlasFlags_::ImFontAtlasFlags_NoBakedLines)
        .export_values();
    PYCLASS_BEGIN(_imgui, ImFontAtlas, FontAtlas)
        FontAtlas.def(py::init<>());
        FontAtlas.def("add_font", &ImFontAtlas::AddFont
        , py::arg("font_cfg")
        , py::return_value_policy::automatic_reference);
        
        FontAtlas.def("add_font_default", &ImFontAtlas::AddFontDefault
        , py::arg("font_cfg") = nullptr
        , py::return_value_policy::automatic_reference);
        
        FontAtlas.def("add_font_from_memory_ttf", &ImFontAtlas::AddFontFromMemoryTTF
        , py::arg("font_data")
        , py::arg("font_data_size")
        , py::arg("size_pixels")
        , py::arg("font_cfg") = nullptr
        , py::arg("glyph_ranges") = nullptr
        , py::return_value_policy::automatic_reference);
        
        FontAtlas.def("add_font_from_memory_compressed_ttf", &ImFontAtlas::AddFontFromMemoryCompressedTTF
        , py::arg("compressed_font_data")
        , py::arg("compressed_font_data_size")
        , py::arg("size_pixels")
        , py::arg("font_cfg") = nullptr
        , py::arg("glyph_ranges") = nullptr
        , py::return_value_policy::automatic_reference);
        
        FontAtlas.def("add_font_from_memory_compressed_base85ttf", &ImFontAtlas::AddFontFromMemoryCompressedBase85TTF
        , py::arg("compressed_font_data_base85")
        , py::arg("size_pixels")
        , py::arg("font_cfg") = nullptr
        , py::arg("glyph_ranges") = nullptr
        , py::return_value_policy::automatic_reference);
        
        FontAtlas.def("clear_input_data", &ImFontAtlas::ClearInputData
        , py::return_value_policy::automatic_reference);
        
        FontAtlas.def("clear_tex_data", &ImFontAtlas::ClearTexData
        , py::return_value_policy::automatic_reference);
        
        FontAtlas.def("clear_fonts", &ImFontAtlas::ClearFonts
        , py::return_value_policy::automatic_reference);
        
        FontAtlas.def("clear", &ImFontAtlas::Clear
        , py::return_value_policy::automatic_reference);
        
        FontAtlas.def("build", &ImFontAtlas::Build
        , py::return_value_policy::automatic_reference);
        
        FontAtlas.def("is_built", &ImFontAtlas::IsBuilt
        , py::return_value_policy::automatic_reference);
        
        FontAtlas.def("set_tex_id", &ImFontAtlas::SetTexID
        , py::arg("id")
        , py::return_value_policy::automatic_reference);
        
        FontAtlas.def("get_glyph_ranges_default", &ImFontAtlas::GetGlyphRangesDefault
        , py::return_value_policy::automatic_reference);
        
        FontAtlas.def("get_glyph_ranges_greek", &ImFontAtlas::GetGlyphRangesGreek
        , py::return_value_policy::automatic_reference);
        
        FontAtlas.def("get_glyph_ranges_korean", &ImFontAtlas::GetGlyphRangesKorean
        , py::return_value_policy::automatic_reference);
        
        FontAtlas.def("get_glyph_ranges_japanese", &ImFontAtlas::GetGlyphRangesJapanese
        , py::return_value_policy::automatic_reference);
        
        FontAtlas.def("get_glyph_ranges_chinese_full", &ImFontAtlas::GetGlyphRangesChineseFull
        , py::return_value_policy::automatic_reference);
        
        FontAtlas.def("get_glyph_ranges_chinese_simplified_common", &ImFontAtlas::GetGlyphRangesChineseSimplifiedCommon
        , py::return_value_policy::automatic_reference);
        
        FontAtlas.def("get_glyph_ranges_cyrillic", &ImFontAtlas::GetGlyphRangesCyrillic
        , py::return_value_policy::automatic_reference);
        
        FontAtlas.def("get_glyph_ranges_thai", &ImFontAtlas::GetGlyphRangesThai
        , py::return_value_policy::automatic_reference);
        
        FontAtlas.def("get_glyph_ranges_vietnamese", &ImFontAtlas::GetGlyphRangesVietnamese
        , py::return_value_policy::automatic_reference);
        
        FontAtlas.def_readwrite("flags", &ImFontAtlas::Flags);
        FontAtlas.def_readwrite("tex_id", &ImFontAtlas::TexID);
        FontAtlas.def_readwrite("tex_desired_width", &ImFontAtlas::TexDesiredWidth);
        FontAtlas.def_readwrite("tex_glyph_padding", &ImFontAtlas::TexGlyphPadding);
        FontAtlas.def_readwrite("locked", &ImFontAtlas::Locked);
        FontAtlas.def_readwrite("user_data", &ImFontAtlas::UserData);
        FontAtlas.def_readwrite("tex_ready", &ImFontAtlas::TexReady);
        FontAtlas.def_readwrite("tex_pixels_use_colors", &ImFontAtlas::TexPixelsUseColors);
        FontAtlas.def_readwrite("tex_width", &ImFontAtlas::TexWidth);
        FontAtlas.def_readwrite("tex_height", &ImFontAtlas::TexHeight);
        FontAtlas.def_readwrite("tex_uv_scale", &ImFontAtlas::TexUvScale);
        FontAtlas.def_readwrite("tex_uv_white_pixel", &ImFontAtlas::TexUvWhitePixel);
        FontAtlas.def_readonly("tex_uv_lines", &ImFontAtlas::TexUvLines);
        FontAtlas.def_readwrite("font_builder_io", &ImFontAtlas::FontBuilderIO);
        FontAtlas.def_readwrite("font_builder_flags", &ImFontAtlas::FontBuilderFlags);
        FontAtlas.def_readwrite("pack_id_mouse_cursors", &ImFontAtlas::PackIdMouseCursors);
        FontAtlas.def_readwrite("pack_id_lines", &ImFontAtlas::PackIdLines);
    PYCLASS_END(_imgui, ImFontAtlas, FontAtlas)
    PYCLASS_BEGIN(_imgui, ImFont, Font)
        Font.def_readwrite("index_advance_x", &ImFont::IndexAdvanceX);
        Font.def_readwrite("fallback_advance_x", &ImFont::FallbackAdvanceX);
        Font.def_readwrite("font_size", &ImFont::FontSize);
        Font.def_readwrite("index_lookup", &ImFont::IndexLookup);
        Font.def_readwrite("glyphs", &ImFont::Glyphs);
        Font.def_readwrite("fallback_glyph", &ImFont::FallbackGlyph);
        Font.def_readwrite("container_atlas", &ImFont::ContainerAtlas);
        Font.def_readwrite("config_data", &ImFont::ConfigData);
        Font.def_readwrite("config_data_count", &ImFont::ConfigDataCount);
        Font.def_readwrite("fallback_char", &ImFont::FallbackChar);
        Font.def_readwrite("ellipsis_char", &ImFont::EllipsisChar);
        Font.def_readwrite("ellipsis_char_count", &ImFont::EllipsisCharCount);
        Font.def_readwrite("ellipsis_width", &ImFont::EllipsisWidth);
        Font.def_readwrite("ellipsis_char_step", &ImFont::EllipsisCharStep);
        Font.def_readwrite("dirty_lookup_tables", &ImFont::DirtyLookupTables);
        Font.def_readwrite("scale", &ImFont::Scale);
        Font.def_readwrite("ascent", &ImFont::Ascent);
        Font.def_readwrite("descent", &ImFont::Descent);
        Font.def_readwrite("metrics_total_surface", &ImFont::MetricsTotalSurface);
        Font.def_readonly("used4k_pages_map", &ImFont::Used4kPagesMap);
        Font.def(py::init<>());
        Font.def("find_glyph", &ImFont::FindGlyph
        , py::arg("c")
        , py::return_value_policy::automatic_reference);
        
        Font.def("find_glyph_no_fallback", &ImFont::FindGlyphNoFallback
        , py::arg("c")
        , py::return_value_policy::automatic_reference);
        
        Font.def("get_char_advance", &ImFont::GetCharAdvance
        , py::arg("c")
        , py::return_value_policy::automatic_reference);
        
        Font.def("is_loaded", &ImFont::IsLoaded
        , py::return_value_policy::automatic_reference);
        
        Font.def("get_debug_name", &ImFont::GetDebugName
        , py::return_value_policy::automatic_reference);
        
        Font.def("calc_word_wrap_position_a", &ImFont::CalcWordWrapPositionA
        , py::arg("scale")
        , py::arg("text")
        , py::arg("text_end")
        , py::arg("wrap_width")
        , py::return_value_policy::automatic_reference);
        
        Font.def("render_char", &ImFont::RenderChar
        , py::arg("draw_list")
        , py::arg("size")
        , py::arg("pos")
        , py::arg("col")
        , py::arg("c")
        , py::return_value_policy::automatic_reference);
        
        Font.def("render_text", &ImFont::RenderText
        , py::arg("draw_list")
        , py::arg("size")
        , py::arg("pos")
        , py::arg("col")
        , py::arg("clip_rect")
        , py::arg("text_begin")
        , py::arg("text_end")
        , py::arg("wrap_width") = 0.0f
        , py::arg("cpu_fine_clip") = false
        , py::return_value_policy::automatic_reference);
        
        Font.def("build_lookup_table", &ImFont::BuildLookupTable
        , py::return_value_policy::automatic_reference);
        
        Font.def("clear_output_data", &ImFont::ClearOutputData
        , py::return_value_policy::automatic_reference);
        
        Font.def("grow_index", &ImFont::GrowIndex
        , py::arg("new_size")
        , py::return_value_policy::automatic_reference);
        
        Font.def("add_glyph", &ImFont::AddGlyph
        , py::arg("src_cfg")
        , py::arg("c")
        , py::arg("x0")
        , py::arg("y0")
        , py::arg("x1")
        , py::arg("y1")
        , py::arg("u0")
        , py::arg("v0")
        , py::arg("u1")
        , py::arg("v1")
        , py::arg("advance_x")
        , py::return_value_policy::automatic_reference);
        
        Font.def("add_remap_char", &ImFont::AddRemapChar
        , py::arg("dst")
        , py::arg("src")
        , py::arg("overwrite_dst") = true
        , py::return_value_policy::automatic_reference);
        
        Font.def("set_glyph_visible", &ImFont::SetGlyphVisible
        , py::arg("c")
        , py::arg("visible")
        , py::return_value_policy::automatic_reference);
        
        Font.def("is_glyph_range_unused", &ImFont::IsGlyphRangeUnused
        , py::arg("c_begin")
        , py::arg("c_last")
        , py::return_value_policy::automatic_reference);
        
    PYCLASS_END(_imgui, ImFont, Font)
    py::enum_<ImGuiViewportFlags_>(_imgui, "ViewportFlags", py::arithmetic())
        .value("VIEWPORT_FLAGS_NONE", ImGuiViewportFlags_::ImGuiViewportFlags_None)
        .value("VIEWPORT_FLAGS_IS_PLATFORM_WINDOW", ImGuiViewportFlags_::ImGuiViewportFlags_IsPlatformWindow)
        .value("VIEWPORT_FLAGS_IS_PLATFORM_MONITOR", ImGuiViewportFlags_::ImGuiViewportFlags_IsPlatformMonitor)
        .value("VIEWPORT_FLAGS_OWNED_BY_APP", ImGuiViewportFlags_::ImGuiViewportFlags_OwnedByApp)
        .value("VIEWPORT_FLAGS_NO_DECORATION", ImGuiViewportFlags_::ImGuiViewportFlags_NoDecoration)
        .value("VIEWPORT_FLAGS_NO_TASK_BAR_ICON", ImGuiViewportFlags_::ImGuiViewportFlags_NoTaskBarIcon)
        .value("VIEWPORT_FLAGS_NO_FOCUS_ON_APPEARING", ImGuiViewportFlags_::ImGuiViewportFlags_NoFocusOnAppearing)
        .value("VIEWPORT_FLAGS_NO_FOCUS_ON_CLICK", ImGuiViewportFlags_::ImGuiViewportFlags_NoFocusOnClick)
        .value("VIEWPORT_FLAGS_NO_INPUTS", ImGuiViewportFlags_::ImGuiViewportFlags_NoInputs)
        .value("VIEWPORT_FLAGS_NO_RENDERER_CLEAR", ImGuiViewportFlags_::ImGuiViewportFlags_NoRendererClear)
        .value("VIEWPORT_FLAGS_NO_AUTO_MERGE", ImGuiViewportFlags_::ImGuiViewportFlags_NoAutoMerge)
        .value("VIEWPORT_FLAGS_TOP_MOST", ImGuiViewportFlags_::ImGuiViewportFlags_TopMost)
        .value("VIEWPORT_FLAGS_CAN_HOST_OTHER_WINDOWS", ImGuiViewportFlags_::ImGuiViewportFlags_CanHostOtherWindows)
        .value("VIEWPORT_FLAGS_IS_MINIMIZED", ImGuiViewportFlags_::ImGuiViewportFlags_IsMinimized)
        .value("VIEWPORT_FLAGS_IS_FOCUSED", ImGuiViewportFlags_::ImGuiViewportFlags_IsFocused)
        .export_values();
    PYCLASS_BEGIN(_imgui, ImGuiViewport, Viewport)
        Viewport.def_readwrite("id", &ImGuiViewport::ID);
        Viewport.def_readwrite("flags", &ImGuiViewport::Flags);
        Viewport.def_readwrite("pos", &ImGuiViewport::Pos);
        Viewport.def_readwrite("size", &ImGuiViewport::Size);
        Viewport.def_readwrite("work_pos", &ImGuiViewport::WorkPos);
        Viewport.def_readwrite("work_size", &ImGuiViewport::WorkSize);
        Viewport.def_readwrite("dpi_scale", &ImGuiViewport::DpiScale);
        Viewport.def_readwrite("parent_viewport_id", &ImGuiViewport::ParentViewportId);
        Viewport.def_readwrite("draw_data", &ImGuiViewport::DrawData);
        Viewport.def_readwrite("renderer_user_data", &ImGuiViewport::RendererUserData);
        Viewport.def_readwrite("platform_user_data", &ImGuiViewport::PlatformUserData);
        Viewport.def_readwrite("platform_handle", &ImGuiViewport::PlatformHandle);
        Viewport.def_readwrite("platform_handle_raw", &ImGuiViewport::PlatformHandleRaw);
        Viewport.def_readwrite("platform_window_created", &ImGuiViewport::PlatformWindowCreated);
        Viewport.def_readwrite("platform_request_move", &ImGuiViewport::PlatformRequestMove);
        Viewport.def_readwrite("platform_request_resize", &ImGuiViewport::PlatformRequestResize);
        Viewport.def_readwrite("platform_request_close", &ImGuiViewport::PlatformRequestClose);
        Viewport.def(py::init<>());
        Viewport.def("get_center", &ImGuiViewport::GetCenter
        , py::return_value_policy::automatic_reference);
        
        Viewport.def("get_work_center", &ImGuiViewport::GetWorkCenter
        , py::return_value_policy::automatic_reference);
        
    PYCLASS_END(_imgui, ImGuiViewport, Viewport)
    PYCLASS_BEGIN(_imgui, ImGuiPlatformImeData, PlatformImeData)
        PlatformImeData.def_readwrite("want_visible", &ImGuiPlatformImeData::WantVisible);
        PlatformImeData.def_readwrite("input_pos", &ImGuiPlatformImeData::InputPos);
        PlatformImeData.def_readwrite("input_line_height", &ImGuiPlatformImeData::InputLineHeight);
        PlatformImeData.def(py::init<>());
    PYCLASS_END(_imgui, ImGuiPlatformImeData, PlatformImeData)
    _imgui.def("get_key_index", &ImGui::GetKeyIndex
    , py::arg("key")
    , py::return_value_policy::automatic_reference);
    

}