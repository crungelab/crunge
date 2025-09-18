#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <limits>

#include "imgui.h"

#include <cxbind/cxbind.h>
#include <crunge/imgui/conversions.h>

namespace py = pybind11;

void init_imgui_py_auto(py::module &_imgui, Registry &registry) {
    py::class_<ImVec2> _Vec2(_imgui, "Vec2");
    registry.on(_imgui, "Vec2", _Vec2);
        _Vec2
        .def_readwrite("x", &ImVec2::x)
        .def_readwrite("y", &ImVec2::y)
        .def(py::init<>())
        .def(py::init<float, float>()
        , py::arg("_x")
        , py::arg("_y")
        )
    ;

    py::class_<ImVec4> _Vec4(_imgui, "Vec4");
    registry.on(_imgui, "Vec4", _Vec4);
        _Vec4
        .def_readwrite("x", &ImVec4::x)
        .def_readwrite("y", &ImVec4::y)
        .def_readwrite("z", &ImVec4::z)
        .def_readwrite("w", &ImVec4::w)
        .def(py::init<>())
        .def(py::init<float, float, float, float>()
        , py::arg("_x")
        , py::arg("_y")
        , py::arg("_z")
        , py::arg("_w")
        )
    ;

    py::class_<ImTextureRef> _TextureRef(_imgui, "TextureRef");
    registry.on(_imgui, "TextureRef", _TextureRef);
        _TextureRef
        .def(py::init<>())
        .def(py::init<unsigned long long>()
        , py::arg("tex_id")
        )
    ;

    _imgui
    .def("create_context", [](ImFontAtlas * shared_font_atlas)
        {
            auto ret = py::capsule(ImGui::CreateContext(shared_font_atlas), "ImGuiContext");
            return ret;
        }
        , py::arg("shared_font_atlas") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("destroy_context", [](const py::capsule& ctx)
        {
            ImGui::DestroyContext(ctx);
            return ;
        }
        , py::arg("ctx") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("get_current_context", []()
        {
            auto ret = py::capsule(ImGui::GetCurrentContext(), "ImGuiContext");
            return ret;
        }
        , py::return_value_policy::automatic_reference)
    .def("set_current_context", [](const py::capsule& ctx)
        {
            ImGui::SetCurrentContext(ctx);
            return ;
        }
        , py::arg("ctx")
        , py::return_value_policy::automatic_reference)
    .def("get_io", &ImGui::GetIO
        , py::return_value_policy::reference)
    .def("get_platform_io", &ImGui::GetPlatformIO
        , py::return_value_policy::reference)
    .def("get_style", &ImGui::GetStyle
        , py::return_value_policy::reference)
    .def("new_frame", &ImGui::NewFrame
        , py::return_value_policy::automatic_reference)
    .def("end_frame", &ImGui::EndFrame
        , py::return_value_policy::automatic_reference)
    .def("render", &ImGui::Render
        , py::return_value_policy::automatic_reference)
    .def("get_draw_data", &ImGui::GetDrawData
        , py::return_value_policy::automatic_reference)
    .def("show_demo_window", [](bool * p_open)
        {
            ImGui::ShowDemoWindow(p_open);
            return p_open;
        }
        , py::arg("p_open") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("show_metrics_window", [](bool * p_open)
        {
            ImGui::ShowMetricsWindow(p_open);
            return p_open;
        }
        , py::arg("p_open") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("show_debug_log_window", [](bool * p_open)
        {
            ImGui::ShowDebugLogWindow(p_open);
            return p_open;
        }
        , py::arg("p_open") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("show_id_stack_tool_window", [](bool * p_open)
        {
            ImGui::ShowIDStackToolWindow(p_open);
            return p_open;
        }
        , py::arg("p_open") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("show_about_window", [](bool * p_open)
        {
            ImGui::ShowAboutWindow(p_open);
            return p_open;
        }
        , py::arg("p_open") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("show_style_editor", &ImGui::ShowStyleEditor
        , py::arg("ref") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("show_style_selector", &ImGui::ShowStyleSelector
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    .def("show_font_selector", &ImGui::ShowFontSelector
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    .def("show_user_guide", &ImGui::ShowUserGuide
        , py::return_value_policy::automatic_reference)
    .def("get_version", &ImGui::GetVersion
        , py::return_value_policy::automatic_reference)
    .def("style_colors_dark", &ImGui::StyleColorsDark
        , py::arg("dst") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("style_colors_light", &ImGui::StyleColorsLight
        , py::arg("dst") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("style_colors_classic", &ImGui::StyleColorsClassic
        , py::arg("dst") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("begin", [](const char * name, bool * p_open, int flags)
        {
            auto ret = ImGui::Begin(name, p_open, flags);
            return std::make_tuple(ret, p_open);
        }
        , py::arg("name")
        , py::arg("p_open") = nullptr
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("end", &ImGui::End
        , py::return_value_policy::automatic_reference)
    .def("begin_child", py::overload_cast<const char *, const ImVec2 &, int, int>(&ImGui::BeginChild)
        , py::arg("str_id")
        , py::arg("size") = ImVec2(0,0)
        , py::arg("child_flags") = 0
        , py::arg("window_flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("begin_child", py::overload_cast<unsigned int, const ImVec2 &, int, int>(&ImGui::BeginChild)
        , py::arg("id")
        , py::arg("size") = ImVec2(0,0)
        , py::arg("child_flags") = 0
        , py::arg("window_flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("end_child", &ImGui::EndChild
        , py::return_value_policy::automatic_reference)
    .def("is_window_appearing", &ImGui::IsWindowAppearing
        , py::return_value_policy::automatic_reference)
    .def("is_window_collapsed", &ImGui::IsWindowCollapsed
        , py::return_value_policy::automatic_reference)
    .def("is_window_focused", &ImGui::IsWindowFocused
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("is_window_hovered", &ImGui::IsWindowHovered
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("get_window_draw_list", &ImGui::GetWindowDrawList
        , py::return_value_policy::automatic_reference)
    .def("get_window_dpi_scale", &ImGui::GetWindowDpiScale
        , py::return_value_policy::automatic_reference)
    .def("get_window_pos", &ImGui::GetWindowPos
        , py::return_value_policy::automatic_reference)
    .def("get_window_size", &ImGui::GetWindowSize
        , py::return_value_policy::automatic_reference)
    .def("get_window_width", &ImGui::GetWindowWidth
        , py::return_value_policy::automatic_reference)
    .def("get_window_height", &ImGui::GetWindowHeight
        , py::return_value_policy::automatic_reference)
    .def("get_window_viewport", &ImGui::GetWindowViewport
        , py::return_value_policy::automatic_reference)
    .def("set_next_window_pos", &ImGui::SetNextWindowPos
        , py::arg("pos")
        , py::arg("cond") = 0
        , py::arg("pivot") = ImVec2(0,0)
        , py::return_value_policy::automatic_reference)
    .def("set_next_window_size", &ImGui::SetNextWindowSize
        , py::arg("size")
        , py::arg("cond") = 0
        , py::return_value_policy::automatic_reference)
    .def("set_next_window_content_size", &ImGui::SetNextWindowContentSize
        , py::arg("size")
        , py::return_value_policy::automatic_reference)
    .def("set_next_window_collapsed", &ImGui::SetNextWindowCollapsed
        , py::arg("collapsed")
        , py::arg("cond") = 0
        , py::return_value_policy::automatic_reference)
    .def("set_next_window_focus", &ImGui::SetNextWindowFocus
        , py::return_value_policy::automatic_reference)
    .def("set_next_window_scroll", &ImGui::SetNextWindowScroll
        , py::arg("scroll")
        , py::return_value_policy::automatic_reference)
    .def("set_next_window_bg_alpha", &ImGui::SetNextWindowBgAlpha
        , py::arg("alpha")
        , py::return_value_policy::automatic_reference)
    .def("set_next_window_viewport", &ImGui::SetNextWindowViewport
        , py::arg("viewport_id")
        , py::return_value_policy::automatic_reference)
    .def("set_window_pos", py::overload_cast<const ImVec2 &, int>(&ImGui::SetWindowPos)
        , py::arg("pos")
        , py::arg("cond") = 0
        , py::return_value_policy::automatic_reference)
    .def("set_window_size", py::overload_cast<const ImVec2 &, int>(&ImGui::SetWindowSize)
        , py::arg("size")
        , py::arg("cond") = 0
        , py::return_value_policy::automatic_reference)
    .def("set_window_collapsed", py::overload_cast<bool, int>(&ImGui::SetWindowCollapsed)
        , py::arg("collapsed")
        , py::arg("cond") = 0
        , py::return_value_policy::automatic_reference)
    .def("set_window_focus", py::overload_cast<>(&ImGui::SetWindowFocus)
        , py::return_value_policy::automatic_reference)
    .def("set_window_pos", py::overload_cast<const char *, const ImVec2 &, int>(&ImGui::SetWindowPos)
        , py::arg("name")
        , py::arg("pos")
        , py::arg("cond") = 0
        , py::return_value_policy::automatic_reference)
    .def("set_window_size", py::overload_cast<const char *, const ImVec2 &, int>(&ImGui::SetWindowSize)
        , py::arg("name")
        , py::arg("size")
        , py::arg("cond") = 0
        , py::return_value_policy::automatic_reference)
    .def("set_window_collapsed", py::overload_cast<const char *, bool, int>(&ImGui::SetWindowCollapsed)
        , py::arg("name")
        , py::arg("collapsed")
        , py::arg("cond") = 0
        , py::return_value_policy::automatic_reference)
    .def("set_window_focus", py::overload_cast<const char *>(&ImGui::SetWindowFocus)
        , py::arg("name")
        , py::return_value_policy::automatic_reference)
    .def("get_scroll_x", &ImGui::GetScrollX
        , py::return_value_policy::automatic_reference)
    .def("get_scroll_y", &ImGui::GetScrollY
        , py::return_value_policy::automatic_reference)
    .def("set_scroll_x", &ImGui::SetScrollX
        , py::arg("scroll_x")
        , py::return_value_policy::automatic_reference)
    .def("set_scroll_y", &ImGui::SetScrollY
        , py::arg("scroll_y")
        , py::return_value_policy::automatic_reference)
    .def("get_scroll_max_x", &ImGui::GetScrollMaxX
        , py::return_value_policy::automatic_reference)
    .def("get_scroll_max_y", &ImGui::GetScrollMaxY
        , py::return_value_policy::automatic_reference)
    .def("set_scroll_here_x", &ImGui::SetScrollHereX
        , py::arg("center_x_ratio") = 0.5f
        , py::return_value_policy::automatic_reference)
    .def("set_scroll_here_y", &ImGui::SetScrollHereY
        , py::arg("center_y_ratio") = 0.5f
        , py::return_value_policy::automatic_reference)
    .def("set_scroll_from_pos_x", &ImGui::SetScrollFromPosX
        , py::arg("local_x")
        , py::arg("center_x_ratio") = 0.5f
        , py::return_value_policy::automatic_reference)
    .def("set_scroll_from_pos_y", &ImGui::SetScrollFromPosY
        , py::arg("local_y")
        , py::arg("center_y_ratio") = 0.5f
        , py::return_value_policy::automatic_reference)
    .def("push_font", &ImGui::PushFont
        , py::arg("font")
        , py::arg("font_size_base_unscaled")
        , py::return_value_policy::automatic_reference)
    .def("pop_font", &ImGui::PopFont
        , py::return_value_policy::automatic_reference)
    .def("get_font", &ImGui::GetFont
        , py::return_value_policy::automatic_reference)
    .def("get_font_size", &ImGui::GetFontSize
        , py::return_value_policy::automatic_reference)
    .def("get_font_baked", &ImGui::GetFontBaked
        , py::return_value_policy::automatic_reference)
    .def("push_style_color", py::overload_cast<int, unsigned int>(&ImGui::PushStyleColor)
        , py::arg("idx")
        , py::arg("col")
        , py::return_value_policy::automatic_reference)
    .def("push_style_color", py::overload_cast<int, const ImVec4 &>(&ImGui::PushStyleColor)
        , py::arg("idx")
        , py::arg("col")
        , py::return_value_policy::automatic_reference)
    .def("pop_style_color", &ImGui::PopStyleColor
        , py::arg("count") = 1
        , py::return_value_policy::automatic_reference)
    .def("push_style_var", py::overload_cast<int, float>(&ImGui::PushStyleVar)
        , py::arg("idx")
        , py::arg("val")
        , py::return_value_policy::automatic_reference)
    .def("push_style_var", py::overload_cast<int, const ImVec2 &>(&ImGui::PushStyleVar)
        , py::arg("idx")
        , py::arg("val")
        , py::return_value_policy::automatic_reference)
    .def("push_style_var_x", &ImGui::PushStyleVarX
        , py::arg("idx")
        , py::arg("val_x")
        , py::return_value_policy::automatic_reference)
    .def("push_style_var_y", &ImGui::PushStyleVarY
        , py::arg("idx")
        , py::arg("val_y")
        , py::return_value_policy::automatic_reference)
    .def("pop_style_var", &ImGui::PopStyleVar
        , py::arg("count") = 1
        , py::return_value_policy::automatic_reference)
    .def("push_item_flag", &ImGui::PushItemFlag
        , py::arg("option")
        , py::arg("enabled")
        , py::return_value_policy::automatic_reference)
    .def("pop_item_flag", &ImGui::PopItemFlag
        , py::return_value_policy::automatic_reference)
    .def("push_item_width", &ImGui::PushItemWidth
        , py::arg("item_width")
        , py::return_value_policy::automatic_reference)
    .def("pop_item_width", &ImGui::PopItemWidth
        , py::return_value_policy::automatic_reference)
    .def("set_next_item_width", &ImGui::SetNextItemWidth
        , py::arg("item_width")
        , py::return_value_policy::automatic_reference)
    .def("calc_item_width", &ImGui::CalcItemWidth
        , py::return_value_policy::automatic_reference)
    .def("push_text_wrap_pos", &ImGui::PushTextWrapPos
        , py::arg("wrap_local_pos_x") = 0.0f
        , py::return_value_policy::automatic_reference)
    .def("pop_text_wrap_pos", &ImGui::PopTextWrapPos
        , py::return_value_policy::automatic_reference)
    .def("get_font_tex_uv_white_pixel", &ImGui::GetFontTexUvWhitePixel
        , py::return_value_policy::automatic_reference)
    .def("get_color_u32", py::overload_cast<int, float>(&ImGui::GetColorU32)
        , py::arg("idx")
        , py::arg("alpha_mul") = 1.0f
        , py::return_value_policy::automatic_reference)
    .def("get_color_u32", py::overload_cast<const ImVec4 &>(&ImGui::GetColorU32)
        , py::arg("col")
        , py::return_value_policy::automatic_reference)
    .def("get_color_u32", py::overload_cast<unsigned int, float>(&ImGui::GetColorU32)
        , py::arg("col")
        , py::arg("alpha_mul") = 1.0f
        , py::return_value_policy::automatic_reference)
    .def("get_style_color_vec4", &ImGui::GetStyleColorVec4
        , py::arg("idx")
        , py::return_value_policy::reference)
    .def("get_cursor_screen_pos", &ImGui::GetCursorScreenPos
        , py::return_value_policy::automatic_reference)
    .def("set_cursor_screen_pos", &ImGui::SetCursorScreenPos
        , py::arg("pos")
        , py::return_value_policy::automatic_reference)
    .def("get_content_region_avail", &ImGui::GetContentRegionAvail
        , py::return_value_policy::automatic_reference)
    .def("get_cursor_pos", &ImGui::GetCursorPos
        , py::return_value_policy::automatic_reference)
    .def("get_cursor_pos_x", &ImGui::GetCursorPosX
        , py::return_value_policy::automatic_reference)
    .def("get_cursor_pos_y", &ImGui::GetCursorPosY
        , py::return_value_policy::automatic_reference)
    .def("set_cursor_pos", &ImGui::SetCursorPos
        , py::arg("local_pos")
        , py::return_value_policy::automatic_reference)
    .def("set_cursor_pos_x", &ImGui::SetCursorPosX
        , py::arg("local_x")
        , py::return_value_policy::automatic_reference)
    .def("set_cursor_pos_y", &ImGui::SetCursorPosY
        , py::arg("local_y")
        , py::return_value_policy::automatic_reference)
    .def("get_cursor_start_pos", &ImGui::GetCursorStartPos
        , py::return_value_policy::automatic_reference)
    .def("separator", &ImGui::Separator
        , py::return_value_policy::automatic_reference)
    .def("same_line", &ImGui::SameLine
        , py::arg("offset_from_start_x") = 0.0f
        , py::arg("spacing") = -1.0f
        , py::return_value_policy::automatic_reference)
    .def("new_line", &ImGui::NewLine
        , py::return_value_policy::automatic_reference)
    .def("spacing", &ImGui::Spacing
        , py::return_value_policy::automatic_reference)
    .def("dummy", &ImGui::Dummy
        , py::arg("size")
        , py::return_value_policy::automatic_reference)
    .def("indent", &ImGui::Indent
        , py::arg("indent_w") = 0.0f
        , py::return_value_policy::automatic_reference)
    .def("unindent", &ImGui::Unindent
        , py::arg("indent_w") = 0.0f
        , py::return_value_policy::automatic_reference)
    .def("begin_group", &ImGui::BeginGroup
        , py::return_value_policy::automatic_reference)
    .def("end_group", &ImGui::EndGroup
        , py::return_value_policy::automatic_reference)
    .def("align_text_to_frame_padding", &ImGui::AlignTextToFramePadding
        , py::return_value_policy::automatic_reference)
    .def("get_text_line_height", &ImGui::GetTextLineHeight
        , py::return_value_policy::automatic_reference)
    .def("get_text_line_height_with_spacing", &ImGui::GetTextLineHeightWithSpacing
        , py::return_value_policy::automatic_reference)
    .def("get_frame_height", &ImGui::GetFrameHeight
        , py::return_value_policy::automatic_reference)
    .def("get_frame_height_with_spacing", &ImGui::GetFrameHeightWithSpacing
        , py::return_value_policy::automatic_reference)
    .def("push_id", py::overload_cast<const char *>(&ImGui::PushID)
        , py::arg("str_id")
        , py::return_value_policy::automatic_reference)
    .def("push_id", py::overload_cast<const char *, const char *>(&ImGui::PushID)
        , py::arg("str_id_begin")
        , py::arg("str_id_end")
        , py::return_value_policy::automatic_reference)
    .def("push_id", py::overload_cast<const void *>(&ImGui::PushID)
        , py::arg("ptr_id")
        , py::return_value_policy::automatic_reference)
    .def("push_id", py::overload_cast<int>(&ImGui::PushID)
        , py::arg("int_id")
        , py::return_value_policy::automatic_reference)
    .def("pop_id", &ImGui::PopID
        , py::return_value_policy::automatic_reference)
    .def("get_id", py::overload_cast<const char *>(&ImGui::GetID)
        , py::arg("str_id")
        , py::return_value_policy::automatic_reference)
    .def("get_id", py::overload_cast<const char *, const char *>(&ImGui::GetID)
        , py::arg("str_id_begin")
        , py::arg("str_id_end")
        , py::return_value_policy::automatic_reference)
    .def("get_id", py::overload_cast<const void *>(&ImGui::GetID)
        , py::arg("ptr_id")
        , py::return_value_policy::automatic_reference)
    .def("get_id", py::overload_cast<int>(&ImGui::GetID)
        , py::arg("int_id")
        , py::return_value_policy::automatic_reference)
    .def("text_unformatted", &ImGui::TextUnformatted
        , py::arg("text")
        , py::arg("text_end") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("text", [](const char * fmt)
        {
            ImGui::Text(fmt);
            return ;
        }
        , py::arg("fmt")
        , py::return_value_policy::automatic_reference)
    .def("text_colored", [](const ImVec4 & col, const char * fmt)
        {
            ImGui::TextColored(col, fmt);
            return ;
        }
        , py::arg("col")
        , py::arg("fmt")
        , py::return_value_policy::automatic_reference)
    .def("text_disabled", [](const char * fmt)
        {
            ImGui::TextDisabled(fmt);
            return ;
        }
        , py::arg("fmt")
        , py::return_value_policy::automatic_reference)
    .def("text_wrapped", [](const char * fmt)
        {
            ImGui::TextWrapped(fmt);
            return ;
        }
        , py::arg("fmt")
        , py::return_value_policy::automatic_reference)
    .def("label_text", [](const char * label, const char * fmt)
        {
            ImGui::LabelText(label, fmt);
            return ;
        }
        , py::arg("label")
        , py::arg("fmt")
        , py::return_value_policy::automatic_reference)
    .def("bullet_text", [](const char * fmt)
        {
            ImGui::BulletText(fmt);
            return ;
        }
        , py::arg("fmt")
        , py::return_value_policy::automatic_reference)
    .def("separator_text", &ImGui::SeparatorText
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    .def("button", &ImGui::Button
        , py::arg("label")
        , py::arg("size") = ImVec2(0,0)
        , py::return_value_policy::automatic_reference)
    .def("small_button", &ImGui::SmallButton
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    .def("invisible_button", &ImGui::InvisibleButton
        , py::arg("str_id")
        , py::arg("size")
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("arrow_button", &ImGui::ArrowButton
        , py::arg("str_id")
        , py::arg("dir")
        , py::return_value_policy::automatic_reference)
    .def("checkbox", [](const char * label, bool * v)
        {
            auto ret = ImGui::Checkbox(label, v);
            return std::make_tuple(ret, v);
        }
        , py::arg("label")
        , py::arg("v")
        , py::return_value_policy::automatic_reference)
    .def("checkbox_flags", [](const char * label, int * flags, int flags_value)
        {
            auto ret = ImGui::CheckboxFlags(label, flags, flags_value);
            return std::make_tuple(ret, flags);
        }
        , py::arg("label")
        , py::arg("flags")
        , py::arg("flags_value")
        , py::return_value_policy::automatic_reference)
    .def("checkbox_flags", [](const char * label, unsigned int * flags, unsigned int flags_value)
        {
            auto ret = ImGui::CheckboxFlags(label, flags, flags_value);
            return std::make_tuple(ret, flags);
        }
        , py::arg("label")
        , py::arg("flags")
        , py::arg("flags_value")
        , py::return_value_policy::automatic_reference)
    .def("radio_button", py::overload_cast<const char *, bool>(&ImGui::RadioButton)
        , py::arg("label")
        , py::arg("active")
        , py::return_value_policy::automatic_reference)
    .def("radio_button", [](const char * label, int * v, int v_button)
        {
            auto ret = ImGui::RadioButton(label, v, v_button);
            return std::make_tuple(ret, v);
        }
        , py::arg("label")
        , py::arg("v")
        , py::arg("v_button")
        , py::return_value_policy::automatic_reference)
    .def("progress_bar", &ImGui::ProgressBar
        , py::arg("fraction")
        , py::arg("size_arg") = ImVec2(-FLT_MIN,0)
        , py::arg("overlay") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("bullet", &ImGui::Bullet
        , py::return_value_policy::automatic_reference)
    .def("text_link", &ImGui::TextLink
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    .def("text_link_open_url", &ImGui::TextLinkOpenURL
        , py::arg("label")
        , py::arg("url") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("image", &ImGui::Image
        , py::arg("tex_ref")
        , py::arg("image_size")
        , py::arg("uv0") = ImVec2(0,0)
        , py::arg("uv1") = ImVec2(1,1)
        , py::return_value_policy::automatic_reference)
    .def("image_with_bg", &ImGui::ImageWithBg
        , py::arg("tex_ref")
        , py::arg("image_size")
        , py::arg("uv0") = ImVec2(0,0)
        , py::arg("uv1") = ImVec2(1,1)
        , py::arg("bg_col") = ImVec4(0,0,0,0)
        , py::arg("tint_col") = ImVec4(1,1,1,1)
        , py::return_value_policy::automatic_reference)
    .def("image_button", &ImGui::ImageButton
        , py::arg("str_id")
        , py::arg("tex_ref")
        , py::arg("image_size")
        , py::arg("uv0") = ImVec2(0,0)
        , py::arg("uv1") = ImVec2(1,1)
        , py::arg("bg_col") = ImVec4(0,0,0,0)
        , py::arg("tint_col") = ImVec4(1,1,1,1)
        , py::return_value_policy::automatic_reference)
    .def("begin_combo", &ImGui::BeginCombo
        , py::arg("label")
        , py::arg("preview_value")
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("end_combo", &ImGui::EndCombo
        , py::return_value_policy::automatic_reference)
    .def("drag_float", [](const char * label, float * v, float v_speed, float v_min, float v_max, const char * format, int flags)
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
        , py::return_value_policy::automatic_reference)
    .def("drag_float2", [](const char * label, std::array<float, 2>& v, float v_speed, float v_min, float v_max, const char * format, int flags)
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
        , py::return_value_policy::automatic_reference)
    .def("drag_float3", [](const char * label, std::array<float, 3>& v, float v_speed, float v_min, float v_max, const char * format, int flags)
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
        , py::return_value_policy::automatic_reference)
    .def("drag_float4", [](const char * label, std::array<float, 4>& v, float v_speed, float v_min, float v_max, const char * format, int flags)
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
        , py::return_value_policy::automatic_reference)
    .def("drag_float_range2", [](const char * label, float * v_current_min, float * v_current_max, float v_speed, float v_min, float v_max, const char * format, const char * format_max, int flags)
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
        , py::return_value_policy::automatic_reference)
    .def("drag_int", [](const char * label, int * v, float v_speed, int v_min, int v_max, const char * format, int flags)
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
        , py::return_value_policy::automatic_reference)
    .def("drag_int2", [](const char * label, std::array<int, 2>& v, float v_speed, int v_min, int v_max, const char * format, int flags)
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
        , py::return_value_policy::automatic_reference)
    .def("drag_int3", [](const char * label, std::array<int, 3>& v, float v_speed, int v_min, int v_max, const char * format, int flags)
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
        , py::return_value_policy::automatic_reference)
    .def("drag_int4", [](const char * label, std::array<int, 4>& v, float v_speed, int v_min, int v_max, const char * format, int flags)
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
        , py::return_value_policy::automatic_reference)
    .def("drag_int_range2", [](const char * label, int * v_current_min, int * v_current_max, float v_speed, int v_min, int v_max, const char * format, const char * format_max, int flags)
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
        , py::return_value_policy::automatic_reference)
    .def("drag_scalar", &ImGui::DragScalar
        , py::arg("label")
        , py::arg("data_type")
        , py::arg("p_data")
        , py::arg("v_speed") = 1.0f
        , py::arg("p_min") = nullptr
        , py::arg("p_max") = nullptr
        , py::arg("format") = nullptr
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("drag_scalar_n", &ImGui::DragScalarN
        , py::arg("label")
        , py::arg("data_type")
        , py::arg("p_data")
        , py::arg("components")
        , py::arg("v_speed") = 1.0f
        , py::arg("p_min") = nullptr
        , py::arg("p_max") = nullptr
        , py::arg("format") = nullptr
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("slider_float", [](const char * label, float * v, float v_min, float v_max, const char * format, int flags)
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
        , py::return_value_policy::automatic_reference)
    .def("slider_float2", [](const char * label, std::array<float, 2>& v, float v_min, float v_max, const char * format, int flags)
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
        , py::return_value_policy::automatic_reference)
    .def("slider_float3", [](const char * label, std::array<float, 3>& v, float v_min, float v_max, const char * format, int flags)
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
        , py::return_value_policy::automatic_reference)
    .def("slider_float4", [](const char * label, std::array<float, 4>& v, float v_min, float v_max, const char * format, int flags)
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
        , py::return_value_policy::automatic_reference)
    .def("slider_angle", [](const char * label, float * v_rad, float v_degrees_min, float v_degrees_max, const char * format, int flags)
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
        , py::return_value_policy::automatic_reference)
    .def("slider_int", [](const char * label, int * v, int v_min, int v_max, const char * format, int flags)
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
        , py::return_value_policy::automatic_reference)
    .def("slider_int2", [](const char * label, std::array<int, 2>& v, int v_min, int v_max, const char * format, int flags)
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
        , py::return_value_policy::automatic_reference)
    .def("slider_int3", [](const char * label, std::array<int, 3>& v, int v_min, int v_max, const char * format, int flags)
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
        , py::return_value_policy::automatic_reference)
    .def("slider_int4", [](const char * label, std::array<int, 4>& v, int v_min, int v_max, const char * format, int flags)
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
        , py::return_value_policy::automatic_reference)
    .def("slider_scalar", &ImGui::SliderScalar
        , py::arg("label")
        , py::arg("data_type")
        , py::arg("p_data")
        , py::arg("p_min")
        , py::arg("p_max")
        , py::arg("format") = nullptr
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("slider_scalar_n", &ImGui::SliderScalarN
        , py::arg("label")
        , py::arg("data_type")
        , py::arg("p_data")
        , py::arg("components")
        , py::arg("p_min")
        , py::arg("p_max")
        , py::arg("format") = nullptr
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("v_slider_float", [](const char * label, const ImVec2 & size, float * v, float v_min, float v_max, const char * format, int flags)
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
        , py::return_value_policy::automatic_reference)
    .def("v_slider_int", [](const char * label, const ImVec2 & size, int * v, int v_min, int v_max, const char * format, int flags)
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
        , py::return_value_policy::automatic_reference)
    .def("v_slider_scalar", &ImGui::VSliderScalar
        , py::arg("label")
        , py::arg("size")
        , py::arg("data_type")
        , py::arg("p_data")
        , py::arg("p_min")
        , py::arg("p_max")
        , py::arg("format") = nullptr
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("input_text_with_hint", &ImGui::InputTextWithHint
        , py::arg("label")
        , py::arg("hint")
        , py::arg("buf")
        , py::arg("buf_size")
        , py::arg("flags") = 0
        , py::arg("callback") = NULL
        , py::arg("user_data") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("input_float", [](const char * label, float * v, float step, float step_fast, const char * format, int flags)
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
        , py::return_value_policy::automatic_reference)
    .def("input_float2", [](const char * label, std::array<float, 2>& v, const char * format, int flags)
        {
            auto ret = ImGui::InputFloat2(label, &v[0], format, flags);
            return std::make_tuple(ret, v);
        }
        , py::arg("label")
        , py::arg("v")
        , py::arg("format") = nullptr
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("input_float3", [](const char * label, std::array<float, 3>& v, const char * format, int flags)
        {
            auto ret = ImGui::InputFloat3(label, &v[0], format, flags);
            return std::make_tuple(ret, v);
        }
        , py::arg("label")
        , py::arg("v")
        , py::arg("format") = nullptr
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("input_float4", [](const char * label, std::array<float, 4>& v, const char * format, int flags)
        {
            auto ret = ImGui::InputFloat4(label, &v[0], format, flags);
            return std::make_tuple(ret, v);
        }
        , py::arg("label")
        , py::arg("v")
        , py::arg("format") = nullptr
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("input_int", [](const char * label, int * v, int step, int step_fast, int flags)
        {
            auto ret = ImGui::InputInt(label, v, step, step_fast, flags);
            return std::make_tuple(ret, v);
        }
        , py::arg("label")
        , py::arg("v")
        , py::arg("step") = 1
        , py::arg("step_fast") = 100
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("input_int2", [](const char * label, std::array<int, 2>& v, int flags)
        {
            auto ret = ImGui::InputInt2(label, &v[0], flags);
            return std::make_tuple(ret, v);
        }
        , py::arg("label")
        , py::arg("v")
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("input_int3", [](const char * label, std::array<int, 3>& v, int flags)
        {
            auto ret = ImGui::InputInt3(label, &v[0], flags);
            return std::make_tuple(ret, v);
        }
        , py::arg("label")
        , py::arg("v")
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("input_int4", [](const char * label, std::array<int, 4>& v, int flags)
        {
            auto ret = ImGui::InputInt4(label, &v[0], flags);
            return std::make_tuple(ret, v);
        }
        , py::arg("label")
        , py::arg("v")
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("input_double", [](const char * label, double * v, double step, double step_fast, const char * format, int flags)
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
        , py::return_value_policy::automatic_reference)
    .def("input_scalar", &ImGui::InputScalar
        , py::arg("label")
        , py::arg("data_type")
        , py::arg("p_data")
        , py::arg("p_step") = nullptr
        , py::arg("p_step_fast") = nullptr
        , py::arg("format") = nullptr
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("input_scalar_n", &ImGui::InputScalarN
        , py::arg("label")
        , py::arg("data_type")
        , py::arg("p_data")
        , py::arg("components")
        , py::arg("p_step") = nullptr
        , py::arg("p_step_fast") = nullptr
        , py::arg("format") = nullptr
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("color_edit3", [](const char * label, std::array<float, 3>& col, int flags)
        {
            auto ret = ImGui::ColorEdit3(label, &col[0], flags);
            return std::make_tuple(ret, col);
        }
        , py::arg("label")
        , py::arg("col")
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("color_edit4", [](const char * label, std::array<float, 4>& col, int flags)
        {
            auto ret = ImGui::ColorEdit4(label, &col[0], flags);
            return std::make_tuple(ret, col);
        }
        , py::arg("label")
        , py::arg("col")
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("color_picker3", [](const char * label, std::array<float, 3>& col, int flags)
        {
            auto ret = ImGui::ColorPicker3(label, &col[0], flags);
            return std::make_tuple(ret, col);
        }
        , py::arg("label")
        , py::arg("col")
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("color_picker4", [](const char * label, std::array<float, 4>& col, int flags, const float * ref_col)
        {
            auto ret = ImGui::ColorPicker4(label, &col[0], flags, ref_col);
            return std::make_tuple(ret, col);
        }
        , py::arg("label")
        , py::arg("col")
        , py::arg("flags") = 0
        , py::arg("ref_col") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("color_button", &ImGui::ColorButton
        , py::arg("desc_id")
        , py::arg("col")
        , py::arg("flags") = 0
        , py::arg("size") = ImVec2(0,0)
        , py::return_value_policy::automatic_reference)
    .def("set_color_edit_options", &ImGui::SetColorEditOptions
        , py::arg("flags")
        , py::return_value_policy::automatic_reference)
    .def("tree_node", py::overload_cast<const char *>(&ImGui::TreeNode)
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    .def("tree_node", [](const char * str_id, const char * fmt)
        {
            auto ret = ImGui::TreeNode(str_id, fmt);
            return ret;
        }
        , py::arg("str_id")
        , py::arg("fmt")
        , py::return_value_policy::automatic_reference)
    .def("tree_node", [](const void * ptr_id, const char * fmt)
        {
            auto ret = ImGui::TreeNode(ptr_id, fmt);
            return ret;
        }
        , py::arg("ptr_id")
        , py::arg("fmt")
        , py::return_value_policy::automatic_reference)
    .def("tree_node_ex", py::overload_cast<const char *, int>(&ImGui::TreeNodeEx)
        , py::arg("label")
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("tree_node_ex", [](const char * str_id, int flags, const char * fmt)
        {
            auto ret = ImGui::TreeNodeEx(str_id, flags, fmt);
            return ret;
        }
        , py::arg("str_id")
        , py::arg("flags")
        , py::arg("fmt")
        , py::return_value_policy::automatic_reference)
    .def("tree_node_ex", [](const void * ptr_id, int flags, const char * fmt)
        {
            auto ret = ImGui::TreeNodeEx(ptr_id, flags, fmt);
            return ret;
        }
        , py::arg("ptr_id")
        , py::arg("flags")
        , py::arg("fmt")
        , py::return_value_policy::automatic_reference)
    .def("tree_push", py::overload_cast<const char *>(&ImGui::TreePush)
        , py::arg("str_id")
        , py::return_value_policy::automatic_reference)
    .def("tree_push", py::overload_cast<const void *>(&ImGui::TreePush)
        , py::arg("ptr_id")
        , py::return_value_policy::automatic_reference)
    .def("tree_pop", &ImGui::TreePop
        , py::return_value_policy::automatic_reference)
    .def("get_tree_node_to_label_spacing", &ImGui::GetTreeNodeToLabelSpacing
        , py::return_value_policy::automatic_reference)
    .def("set_next_item_open", &ImGui::SetNextItemOpen
        , py::arg("is_open")
        , py::arg("cond") = 0
        , py::return_value_policy::automatic_reference)
    .def("set_next_item_storage_id", &ImGui::SetNextItemStorageID
        , py::arg("storage_id")
        , py::return_value_policy::automatic_reference)
    .def("begin_multi_select", &ImGui::BeginMultiSelect
        , py::arg("flags")
        , py::arg("selection_size") = -1
        , py::arg("items_count") = -1
        , py::return_value_policy::automatic_reference)
    .def("end_multi_select", &ImGui::EndMultiSelect
        , py::return_value_policy::automatic_reference)
    .def("set_next_item_selection_user_data", &ImGui::SetNextItemSelectionUserData
        , py::arg("selection_user_data")
        , py::return_value_policy::automatic_reference)
    .def("is_item_toggled_selection", &ImGui::IsItemToggledSelection
        , py::return_value_policy::automatic_reference)
    .def("begin_list_box", &ImGui::BeginListBox
        , py::arg("label")
        , py::arg("size") = ImVec2(0,0)
        , py::return_value_policy::automatic_reference)
    .def("end_list_box", &ImGui::EndListBox
        , py::return_value_policy::automatic_reference)
    .def("value", py::overload_cast<const char *, bool>(&ImGui::Value)
        , py::arg("prefix")
        , py::arg("b")
        , py::return_value_policy::automatic_reference)
    .def("value", py::overload_cast<const char *, int>(&ImGui::Value)
        , py::arg("prefix")
        , py::arg("v")
        , py::return_value_policy::automatic_reference)
    .def("value", py::overload_cast<const char *, unsigned int>(&ImGui::Value)
        , py::arg("prefix")
        , py::arg("v")
        , py::return_value_policy::automatic_reference)
    .def("value", py::overload_cast<const char *, float, const char *>(&ImGui::Value)
        , py::arg("prefix")
        , py::arg("v")
        , py::arg("float_format") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("begin_menu_bar", &ImGui::BeginMenuBar
        , py::return_value_policy::automatic_reference)
    .def("end_menu_bar", &ImGui::EndMenuBar
        , py::return_value_policy::automatic_reference)
    .def("begin_main_menu_bar", &ImGui::BeginMainMenuBar
        , py::return_value_policy::automatic_reference)
    .def("end_main_menu_bar", &ImGui::EndMainMenuBar
        , py::return_value_policy::automatic_reference)
    .def("begin_menu", &ImGui::BeginMenu
        , py::arg("label")
        , py::arg("enabled") = true
        , py::return_value_policy::automatic_reference)
    .def("end_menu", &ImGui::EndMenu
        , py::return_value_policy::automatic_reference)
    .def("begin_tooltip", &ImGui::BeginTooltip
        , py::return_value_policy::automatic_reference)
    .def("end_tooltip", &ImGui::EndTooltip
        , py::return_value_policy::automatic_reference)
    .def("set_tooltip", [](const char * fmt)
        {
            ImGui::SetTooltip(fmt);
            return ;
        }
        , py::arg("fmt")
        , py::return_value_policy::automatic_reference)
    .def("begin_item_tooltip", &ImGui::BeginItemTooltip
        , py::return_value_policy::automatic_reference)
    .def("set_item_tooltip", [](const char * fmt)
        {
            ImGui::SetItemTooltip(fmt);
            return ;
        }
        , py::arg("fmt")
        , py::return_value_policy::automatic_reference)
    .def("begin_popup", &ImGui::BeginPopup
        , py::arg("str_id")
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("begin_popup_modal", [](const char * name, bool * p_open, int flags)
        {
            auto ret = ImGui::BeginPopupModal(name, p_open, flags);
            return std::make_tuple(ret, p_open);
        }
        , py::arg("name")
        , py::arg("p_open") = nullptr
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("end_popup", &ImGui::EndPopup
        , py::return_value_policy::automatic_reference)
    .def("open_popup", py::overload_cast<const char *, int>(&ImGui::OpenPopup)
        , py::arg("str_id")
        , py::arg("popup_flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("open_popup", py::overload_cast<unsigned int, int>(&ImGui::OpenPopup)
        , py::arg("id")
        , py::arg("popup_flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("open_popup_on_item_click", &ImGui::OpenPopupOnItemClick
        , py::arg("str_id") = nullptr
        , py::arg("popup_flags") = 1
        , py::return_value_policy::automatic_reference)
    .def("close_current_popup", &ImGui::CloseCurrentPopup
        , py::return_value_policy::automatic_reference)
    .def("begin_popup_context_item", &ImGui::BeginPopupContextItem
        , py::arg("str_id") = nullptr
        , py::arg("popup_flags") = 1
        , py::return_value_policy::automatic_reference)
    .def("begin_popup_context_window", &ImGui::BeginPopupContextWindow
        , py::arg("str_id") = nullptr
        , py::arg("popup_flags") = 1
        , py::return_value_policy::automatic_reference)
    .def("begin_popup_context_void", &ImGui::BeginPopupContextVoid
        , py::arg("str_id") = nullptr
        , py::arg("popup_flags") = 1
        , py::return_value_policy::automatic_reference)
    .def("is_popup_open", &ImGui::IsPopupOpen
        , py::arg("str_id")
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("begin_table", &ImGui::BeginTable
        , py::arg("str_id")
        , py::arg("columns")
        , py::arg("flags") = 0
        , py::arg("outer_size") = ImVec2(0.0f,0.0f)
        , py::arg("inner_width") = 0.0f
        , py::return_value_policy::automatic_reference)
    .def("end_table", &ImGui::EndTable
        , py::return_value_policy::automatic_reference)
    .def("table_next_row", &ImGui::TableNextRow
        , py::arg("row_flags") = 0
        , py::arg("min_row_height") = 0.0f
        , py::return_value_policy::automatic_reference)
    .def("table_next_column", &ImGui::TableNextColumn
        , py::return_value_policy::automatic_reference)
    .def("table_set_column_index", &ImGui::TableSetColumnIndex
        , py::arg("column_n")
        , py::return_value_policy::automatic_reference)
    .def("table_setup_column", &ImGui::TableSetupColumn
        , py::arg("label")
        , py::arg("flags") = 0
        , py::arg("init_width_or_weight") = 0.0f
        , py::arg("user_id") = 0
        , py::return_value_policy::automatic_reference)
    .def("table_setup_scroll_freeze", &ImGui::TableSetupScrollFreeze
        , py::arg("cols")
        , py::arg("rows")
        , py::return_value_policy::automatic_reference)
    .def("table_header", &ImGui::TableHeader
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    .def("table_headers_row", &ImGui::TableHeadersRow
        , py::return_value_policy::automatic_reference)
    .def("table_angled_headers_row", &ImGui::TableAngledHeadersRow
        , py::return_value_policy::automatic_reference)
    .def("table_get_sort_specs", &ImGui::TableGetSortSpecs
        , py::return_value_policy::automatic_reference)
    .def("table_get_column_count", &ImGui::TableGetColumnCount
        , py::return_value_policy::automatic_reference)
    .def("table_get_column_index", &ImGui::TableGetColumnIndex
        , py::return_value_policy::automatic_reference)
    .def("table_get_row_index", &ImGui::TableGetRowIndex
        , py::return_value_policy::automatic_reference)
    .def("table_get_column_flags", &ImGui::TableGetColumnFlags
        , py::arg("column_n") = -1
        , py::return_value_policy::automatic_reference)
    .def("table_set_column_enabled", &ImGui::TableSetColumnEnabled
        , py::arg("column_n")
        , py::arg("v")
        , py::return_value_policy::automatic_reference)
    .def("table_get_hovered_column", &ImGui::TableGetHoveredColumn
        , py::return_value_policy::automatic_reference)
    .def("table_set_bg_color", &ImGui::TableSetBgColor
        , py::arg("target")
        , py::arg("color")
        , py::arg("column_n") = -1
        , py::return_value_policy::automatic_reference)
    .def("columns", &ImGui::Columns
        , py::arg("count") = 1
        , py::arg("id") = nullptr
        , py::arg("borders") = true
        , py::return_value_policy::automatic_reference)
    .def("next_column", &ImGui::NextColumn
        , py::return_value_policy::automatic_reference)
    .def("get_column_index", &ImGui::GetColumnIndex
        , py::return_value_policy::automatic_reference)
    .def("get_column_width", &ImGui::GetColumnWidth
        , py::arg("column_index") = -1
        , py::return_value_policy::automatic_reference)
    .def("set_column_width", &ImGui::SetColumnWidth
        , py::arg("column_index")
        , py::arg("width")
        , py::return_value_policy::automatic_reference)
    .def("get_column_offset", &ImGui::GetColumnOffset
        , py::arg("column_index") = -1
        , py::return_value_policy::automatic_reference)
    .def("set_column_offset", &ImGui::SetColumnOffset
        , py::arg("column_index")
        , py::arg("offset_x")
        , py::return_value_policy::automatic_reference)
    .def("get_columns_count", &ImGui::GetColumnsCount
        , py::return_value_policy::automatic_reference)
    .def("begin_tab_bar", &ImGui::BeginTabBar
        , py::arg("str_id")
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("end_tab_bar", &ImGui::EndTabBar
        , py::return_value_policy::automatic_reference)
    .def("begin_tab_item", [](const char * label, bool * p_open, int flags)
        {
            auto ret = ImGui::BeginTabItem(label, p_open, flags);
            return std::make_tuple(ret, p_open);
        }
        , py::arg("label")
        , py::arg("p_open") = nullptr
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("end_tab_item", &ImGui::EndTabItem
        , py::return_value_policy::automatic_reference)
    .def("tab_item_button", &ImGui::TabItemButton
        , py::arg("label")
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("set_tab_item_closed", &ImGui::SetTabItemClosed
        , py::arg("tab_or_docked_window_label")
        , py::return_value_policy::automatic_reference)
    .def("dock_space", &ImGui::DockSpace
        , py::arg("dockspace_id")
        , py::arg("size") = ImVec2(0,0)
        , py::arg("flags") = 0
        , py::arg("window_class") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("dock_space_over_viewport", &ImGui::DockSpaceOverViewport
        , py::arg("dockspace_id") = 0
        , py::arg("viewport") = nullptr
        , py::arg("flags") = 0
        , py::arg("window_class") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("set_next_window_dock_id", &ImGui::SetNextWindowDockID
        , py::arg("dock_id")
        , py::arg("cond") = 0
        , py::return_value_policy::automatic_reference)
    .def("set_next_window_class", &ImGui::SetNextWindowClass
        , py::arg("window_class")
        , py::return_value_policy::automatic_reference)
    .def("get_window_dock_id", &ImGui::GetWindowDockID
        , py::return_value_policy::automatic_reference)
    .def("is_window_docked", &ImGui::IsWindowDocked
        , py::return_value_policy::automatic_reference)
    .def("log_to_tty", &ImGui::LogToTTY
        , py::arg("auto_open_depth") = -1
        , py::return_value_policy::automatic_reference)
    .def("log_to_file", &ImGui::LogToFile
        , py::arg("auto_open_depth") = -1
        , py::arg("filename") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("log_to_clipboard", &ImGui::LogToClipboard
        , py::arg("auto_open_depth") = -1
        , py::return_value_policy::automatic_reference)
    .def("log_finish", &ImGui::LogFinish
        , py::return_value_policy::automatic_reference)
    .def("log_buttons", &ImGui::LogButtons
        , py::return_value_policy::automatic_reference)
    .def("log_text", [](const char * fmt)
        {
            ImGui::LogText(fmt);
            return ;
        }
        , py::arg("fmt")
        , py::return_value_policy::automatic_reference)
    .def("begin_drag_drop_source", &ImGui::BeginDragDropSource
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("end_drag_drop_source", &ImGui::EndDragDropSource
        , py::return_value_policy::automatic_reference)
    .def("begin_drag_drop_target", &ImGui::BeginDragDropTarget
        , py::return_value_policy::automatic_reference)
    .def("accept_drag_drop_payload", &ImGui::AcceptDragDropPayload
        , py::arg("type")
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("end_drag_drop_target", &ImGui::EndDragDropTarget
        , py::return_value_policy::automatic_reference)
    .def("get_drag_drop_payload", &ImGui::GetDragDropPayload
        , py::return_value_policy::automatic_reference)
    .def("begin_disabled", &ImGui::BeginDisabled
        , py::arg("disabled") = true
        , py::return_value_policy::automatic_reference)
    .def("end_disabled", &ImGui::EndDisabled
        , py::return_value_policy::automatic_reference)
    .def("push_clip_rect", &ImGui::PushClipRect
        , py::arg("clip_rect_min")
        , py::arg("clip_rect_max")
        , py::arg("intersect_with_current_clip_rect")
        , py::return_value_policy::automatic_reference)
    .def("pop_clip_rect", &ImGui::PopClipRect
        , py::return_value_policy::automatic_reference)
    .def("set_item_default_focus", &ImGui::SetItemDefaultFocus
        , py::return_value_policy::automatic_reference)
    .def("set_keyboard_focus_here", &ImGui::SetKeyboardFocusHere
        , py::arg("offset") = 0
        , py::return_value_policy::automatic_reference)
    .def("set_nav_cursor_visible", &ImGui::SetNavCursorVisible
        , py::arg("visible")
        , py::return_value_policy::automatic_reference)
    .def("set_next_item_allow_overlap", &ImGui::SetNextItemAllowOverlap
        , py::return_value_policy::automatic_reference)
    .def("is_item_hovered", &ImGui::IsItemHovered
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("is_item_active", &ImGui::IsItemActive
        , py::return_value_policy::automatic_reference)
    .def("is_item_focused", &ImGui::IsItemFocused
        , py::return_value_policy::automatic_reference)
    .def("is_item_clicked", &ImGui::IsItemClicked
        , py::arg("mouse_button") = 0
        , py::return_value_policy::automatic_reference)
    .def("is_item_visible", &ImGui::IsItemVisible
        , py::return_value_policy::automatic_reference)
    .def("is_item_edited", &ImGui::IsItemEdited
        , py::return_value_policy::automatic_reference)
    .def("is_item_activated", &ImGui::IsItemActivated
        , py::return_value_policy::automatic_reference)
    .def("is_item_deactivated", &ImGui::IsItemDeactivated
        , py::return_value_policy::automatic_reference)
    .def("is_item_deactivated_after_edit", &ImGui::IsItemDeactivatedAfterEdit
        , py::return_value_policy::automatic_reference)
    .def("is_item_toggled_open", &ImGui::IsItemToggledOpen
        , py::return_value_policy::automatic_reference)
    .def("is_any_item_hovered", &ImGui::IsAnyItemHovered
        , py::return_value_policy::automatic_reference)
    .def("is_any_item_active", &ImGui::IsAnyItemActive
        , py::return_value_policy::automatic_reference)
    .def("is_any_item_focused", &ImGui::IsAnyItemFocused
        , py::return_value_policy::automatic_reference)
    .def("get_item_id", &ImGui::GetItemID
        , py::return_value_policy::automatic_reference)
    .def("get_item_rect_min", &ImGui::GetItemRectMin
        , py::return_value_policy::automatic_reference)
    .def("get_item_rect_max", &ImGui::GetItemRectMax
        , py::return_value_policy::automatic_reference)
    .def("get_item_rect_size", &ImGui::GetItemRectSize
        , py::return_value_policy::automatic_reference)
    .def("get_main_viewport", &ImGui::GetMainViewport
        , py::return_value_policy::automatic_reference)
    .def("get_background_draw_list", &ImGui::GetBackgroundDrawList
        , py::arg("viewport") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("get_foreground_draw_list", &ImGui::GetForegroundDrawList
        , py::arg("viewport") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("is_rect_visible", py::overload_cast<const ImVec2 &>(&ImGui::IsRectVisible)
        , py::arg("size")
        , py::return_value_policy::automatic_reference)
    .def("is_rect_visible", py::overload_cast<const ImVec2 &, const ImVec2 &>(&ImGui::IsRectVisible)
        , py::arg("rect_min")
        , py::arg("rect_max")
        , py::return_value_policy::automatic_reference)
    .def("get_time", &ImGui::GetTime
        , py::return_value_policy::automatic_reference)
    .def("get_frame_count", &ImGui::GetFrameCount
        , py::return_value_policy::automatic_reference)
    .def("get_style_color_name", &ImGui::GetStyleColorName
        , py::arg("idx")
        , py::return_value_policy::automatic_reference)
    .def("set_state_storage", &ImGui::SetStateStorage
        , py::arg("storage")
        , py::return_value_policy::automatic_reference)
    .def("get_state_storage", &ImGui::GetStateStorage
        , py::return_value_policy::automatic_reference)
    .def("calc_text_size", &ImGui::CalcTextSize
        , py::arg("text")
        , py::arg("text_end") = nullptr
        , py::arg("hide_text_after_double_hash") = false
        , py::arg("wrap_width") = -1.0f
        , py::return_value_policy::automatic_reference)
    .def("color_convert_u32_to_float4", &ImGui::ColorConvertU32ToFloat4
        , py::arg("in")
        , py::return_value_policy::automatic_reference)
    .def("color_convert_float4_to_u32", &ImGui::ColorConvertFloat4ToU32
        , py::arg("in")
        , py::return_value_policy::automatic_reference)
    .def("color_convert_rg_bto_hsv", [](float r, float g, float b, float & out_h, float & out_s, float & out_v)
        {
            ImGui::ColorConvertRGBtoHSV(r, g, b, out_h, out_s, out_v);
            return std::make_tuple(out_h, out_s, out_v);
        }
        , py::arg("r")
        , py::arg("g")
        , py::arg("b")
        , py::arg("out_h")
        , py::arg("out_s")
        , py::arg("out_v")
        , py::return_value_policy::automatic_reference)
    .def("color_convert_hs_vto_rgb", [](float h, float s, float v, float & out_r, float & out_g, float & out_b)
        {
            ImGui::ColorConvertHSVtoRGB(h, s, v, out_r, out_g, out_b);
            return std::make_tuple(out_r, out_g, out_b);
        }
        , py::arg("h")
        , py::arg("s")
        , py::arg("v")
        , py::arg("out_r")
        , py::arg("out_g")
        , py::arg("out_b")
        , py::return_value_policy::automatic_reference)
    .def("is_key_down", &ImGui::IsKeyDown
        , py::arg("key")
        , py::return_value_policy::automatic_reference)
    .def("is_key_pressed", &ImGui::IsKeyPressed
        , py::arg("key")
        , py::arg("repeat") = true
        , py::return_value_policy::automatic_reference)
    .def("is_key_released", &ImGui::IsKeyReleased
        , py::arg("key")
        , py::return_value_policy::automatic_reference)
    .def("is_key_chord_pressed", &ImGui::IsKeyChordPressed
        , py::arg("key_chord")
        , py::return_value_policy::automatic_reference)
    .def("get_key_pressed_amount", &ImGui::GetKeyPressedAmount
        , py::arg("key")
        , py::arg("repeat_delay")
        , py::arg("rate")
        , py::return_value_policy::automatic_reference)
    .def("get_key_name", &ImGui::GetKeyName
        , py::arg("key")
        , py::return_value_policy::automatic_reference)
    .def("set_next_frame_want_capture_keyboard", &ImGui::SetNextFrameWantCaptureKeyboard
        , py::arg("want_capture_keyboard")
        , py::return_value_policy::automatic_reference)
    .def("shortcut", &ImGui::Shortcut
        , py::arg("key_chord")
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("set_next_item_shortcut", &ImGui::SetNextItemShortcut
        , py::arg("key_chord")
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("set_item_key_owner", &ImGui::SetItemKeyOwner
        , py::arg("key")
        , py::return_value_policy::automatic_reference)
    .def("is_mouse_down", &ImGui::IsMouseDown
        , py::arg("button")
        , py::return_value_policy::automatic_reference)
    .def("is_mouse_clicked", &ImGui::IsMouseClicked
        , py::arg("button")
        , py::arg("repeat") = false
        , py::return_value_policy::automatic_reference)
    .def("is_mouse_released", &ImGui::IsMouseReleased
        , py::arg("button")
        , py::return_value_policy::automatic_reference)
    .def("is_mouse_double_clicked", &ImGui::IsMouseDoubleClicked
        , py::arg("button")
        , py::return_value_policy::automatic_reference)
    .def("is_mouse_released_with_delay", &ImGui::IsMouseReleasedWithDelay
        , py::arg("button")
        , py::arg("delay")
        , py::return_value_policy::automatic_reference)
    .def("get_mouse_clicked_count", &ImGui::GetMouseClickedCount
        , py::arg("button")
        , py::return_value_policy::automatic_reference)
    .def("is_mouse_hovering_rect", &ImGui::IsMouseHoveringRect
        , py::arg("r_min")
        , py::arg("r_max")
        , py::arg("clip") = true
        , py::return_value_policy::automatic_reference)
    .def("is_mouse_pos_valid", &ImGui::IsMousePosValid
        , py::arg("mouse_pos") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("is_any_mouse_down", &ImGui::IsAnyMouseDown
        , py::return_value_policy::automatic_reference)
    .def("get_mouse_pos", &ImGui::GetMousePos
        , py::return_value_policy::automatic_reference)
    .def("get_mouse_pos_on_opening_current_popup", &ImGui::GetMousePosOnOpeningCurrentPopup
        , py::return_value_policy::automatic_reference)
    .def("is_mouse_dragging", &ImGui::IsMouseDragging
        , py::arg("button")
        , py::arg("lock_threshold") = -1.0f
        , py::return_value_policy::automatic_reference)
    .def("get_mouse_drag_delta", &ImGui::GetMouseDragDelta
        , py::arg("button") = 0
        , py::arg("lock_threshold") = -1.0f
        , py::return_value_policy::automatic_reference)
    .def("reset_mouse_drag_delta", &ImGui::ResetMouseDragDelta
        , py::arg("button") = 0
        , py::return_value_policy::automatic_reference)
    .def("get_mouse_cursor", &ImGui::GetMouseCursor
        , py::return_value_policy::automatic_reference)
    .def("set_mouse_cursor", &ImGui::SetMouseCursor
        , py::arg("cursor_type")
        , py::return_value_policy::automatic_reference)
    .def("set_next_frame_want_capture_mouse", &ImGui::SetNextFrameWantCaptureMouse
        , py::arg("want_capture_mouse")
        , py::return_value_policy::automatic_reference)
    .def("get_clipboard_text", &ImGui::GetClipboardText
        , py::return_value_policy::automatic_reference)
    .def("set_clipboard_text", &ImGui::SetClipboardText
        , py::arg("text")
        , py::return_value_policy::automatic_reference)
    .def("load_ini_settings_from_disk", &ImGui::LoadIniSettingsFromDisk
        , py::arg("ini_filename")
        , py::return_value_policy::automatic_reference)
    .def("load_ini_settings_from_memory", &ImGui::LoadIniSettingsFromMemory
        , py::arg("ini_data")
        , py::arg("ini_size") = 0
        , py::return_value_policy::automatic_reference)
    .def("save_ini_settings_to_disk", &ImGui::SaveIniSettingsToDisk
        , py::arg("ini_filename")
        , py::return_value_policy::automatic_reference)
    .def("save_ini_settings_to_memory", [](unsigned long * out_ini_size)
        {
            auto ret = ImGui::SaveIniSettingsToMemory(out_ini_size);
            return std::make_tuple(ret, out_ini_size);
        }
        , py::arg("out_ini_size") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("debug_text_encoding", &ImGui::DebugTextEncoding
        , py::arg("text")
        , py::return_value_policy::automatic_reference)
    .def("debug_flash_style_color", &ImGui::DebugFlashStyleColor
        , py::arg("idx")
        , py::return_value_policy::automatic_reference)
    .def("debug_start_item_picker", &ImGui::DebugStartItemPicker
        , py::return_value_policy::automatic_reference)
    .def("debug_check_version_and_data_layout", &ImGui::DebugCheckVersionAndDataLayout
        , py::arg("version_str")
        , py::arg("sz_io")
        , py::arg("sz_style")
        , py::arg("sz_vec2")
        , py::arg("sz_vec4")
        , py::arg("sz_drawvert")
        , py::arg("sz_drawidx")
        , py::return_value_policy::automatic_reference)
    .def("debug_log", [](const char * fmt)
        {
            ImGui::DebugLog(fmt);
            return ;
        }
        , py::arg("fmt")
        , py::return_value_policy::automatic_reference)
    .def("update_platform_windows", &ImGui::UpdatePlatformWindows
        , py::return_value_policy::automatic_reference)
    .def("render_platform_windows_default", &ImGui::RenderPlatformWindowsDefault
        , py::arg("platform_render_arg") = nullptr
        , py::arg("renderer_render_arg") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("destroy_platform_windows", &ImGui::DestroyPlatformWindows
        , py::return_value_policy::automatic_reference)
    .def("find_viewport_by_id", &ImGui::FindViewportByID
        , py::arg("id")
        , py::return_value_policy::automatic_reference)
    .def("find_viewport_by_platform_handle", &ImGui::FindViewportByPlatformHandle
        , py::arg("platform_handle")
        , py::return_value_policy::automatic_reference)
    ;

    py::enum_<ImGuiWindowFlags_>(_imgui, "WindowFlags", py::arithmetic())
        .value("NONE", ImGuiWindowFlags_::ImGuiWindowFlags_None)
        .value("NO_TITLE_BAR", ImGuiWindowFlags_::ImGuiWindowFlags_NoTitleBar)
        .value("NO_RESIZE", ImGuiWindowFlags_::ImGuiWindowFlags_NoResize)
        .value("NO_MOVE", ImGuiWindowFlags_::ImGuiWindowFlags_NoMove)
        .value("NO_SCROLLBAR", ImGuiWindowFlags_::ImGuiWindowFlags_NoScrollbar)
        .value("NO_SCROLL_WITH_MOUSE", ImGuiWindowFlags_::ImGuiWindowFlags_NoScrollWithMouse)
        .value("NO_COLLAPSE", ImGuiWindowFlags_::ImGuiWindowFlags_NoCollapse)
        .value("ALWAYS_AUTO_RESIZE", ImGuiWindowFlags_::ImGuiWindowFlags_AlwaysAutoResize)
        .value("NO_BACKGROUND", ImGuiWindowFlags_::ImGuiWindowFlags_NoBackground)
        .value("NO_SAVED_SETTINGS", ImGuiWindowFlags_::ImGuiWindowFlags_NoSavedSettings)
        .value("NO_MOUSE_INPUTS", ImGuiWindowFlags_::ImGuiWindowFlags_NoMouseInputs)
        .value("MENU_BAR", ImGuiWindowFlags_::ImGuiWindowFlags_MenuBar)
        .value("HORIZONTAL_SCROLLBAR", ImGuiWindowFlags_::ImGuiWindowFlags_HorizontalScrollbar)
        .value("NO_FOCUS_ON_APPEARING", ImGuiWindowFlags_::ImGuiWindowFlags_NoFocusOnAppearing)
        .value("NO_BRING_TO_FRONT_ON_FOCUS", ImGuiWindowFlags_::ImGuiWindowFlags_NoBringToFrontOnFocus)
        .value("ALWAYS_VERTICAL_SCROLLBAR", ImGuiWindowFlags_::ImGuiWindowFlags_AlwaysVerticalScrollbar)
        .value("ALWAYS_HORIZONTAL_SCROLLBAR", ImGuiWindowFlags_::ImGuiWindowFlags_AlwaysHorizontalScrollbar)
        .value("NO_NAV_INPUTS", ImGuiWindowFlags_::ImGuiWindowFlags_NoNavInputs)
        .value("NO_NAV_FOCUS", ImGuiWindowFlags_::ImGuiWindowFlags_NoNavFocus)
        .value("UNSAVED_DOCUMENT", ImGuiWindowFlags_::ImGuiWindowFlags_UnsavedDocument)
        .value("NO_DOCKING", ImGuiWindowFlags_::ImGuiWindowFlags_NoDocking)
        .value("NO_NAV", ImGuiWindowFlags_::ImGuiWindowFlags_NoNav)
        .value("NO_DECORATION", ImGuiWindowFlags_::ImGuiWindowFlags_NoDecoration)
        .value("NO_INPUTS", ImGuiWindowFlags_::ImGuiWindowFlags_NoInputs)
        .value("DOCK_NODE_HOST", ImGuiWindowFlags_::ImGuiWindowFlags_DockNodeHost)
        .value("CHILD_WINDOW", ImGuiWindowFlags_::ImGuiWindowFlags_ChildWindow)
        .value("TOOLTIP", ImGuiWindowFlags_::ImGuiWindowFlags_Tooltip)
        .value("POPUP", ImGuiWindowFlags_::ImGuiWindowFlags_Popup)
        .value("MODAL", ImGuiWindowFlags_::ImGuiWindowFlags_Modal)
        .value("CHILD_MENU", ImGuiWindowFlags_::ImGuiWindowFlags_ChildMenu)
        .export_values()
    ;
    py::enum_<ImGuiChildFlags_>(_imgui, "ChildFlags", py::arithmetic())
        .value("NONE", ImGuiChildFlags_::ImGuiChildFlags_None)
        .value("BORDERS", ImGuiChildFlags_::ImGuiChildFlags_Borders)
        .value("ALWAYS_USE_WINDOW_PADDING", ImGuiChildFlags_::ImGuiChildFlags_AlwaysUseWindowPadding)
        .value("RESIZE_X", ImGuiChildFlags_::ImGuiChildFlags_ResizeX)
        .value("RESIZE_Y", ImGuiChildFlags_::ImGuiChildFlags_ResizeY)
        .value("AUTO_RESIZE_X", ImGuiChildFlags_::ImGuiChildFlags_AutoResizeX)
        .value("AUTO_RESIZE_Y", ImGuiChildFlags_::ImGuiChildFlags_AutoResizeY)
        .value("ALWAYS_AUTO_RESIZE", ImGuiChildFlags_::ImGuiChildFlags_AlwaysAutoResize)
        .value("FRAME_STYLE", ImGuiChildFlags_::ImGuiChildFlags_FrameStyle)
        .value("NAV_FLATTENED", ImGuiChildFlags_::ImGuiChildFlags_NavFlattened)
        .export_values()
    ;
    py::enum_<ImGuiItemFlags_>(_imgui, "ItemFlags", py::arithmetic())
        .value("NONE", ImGuiItemFlags_::ImGuiItemFlags_None)
        .value("NO_TAB_STOP", ImGuiItemFlags_::ImGuiItemFlags_NoTabStop)
        .value("NO_NAV", ImGuiItemFlags_::ImGuiItemFlags_NoNav)
        .value("NO_NAV_DEFAULT_FOCUS", ImGuiItemFlags_::ImGuiItemFlags_NoNavDefaultFocus)
        .value("BUTTON_REPEAT", ImGuiItemFlags_::ImGuiItemFlags_ButtonRepeat)
        .value("AUTO_CLOSE_POPUPS", ImGuiItemFlags_::ImGuiItemFlags_AutoClosePopups)
        .value("ALLOW_DUPLICATE_ID", ImGuiItemFlags_::ImGuiItemFlags_AllowDuplicateId)
        .export_values()
    ;
    py::enum_<ImGuiInputTextFlags_>(_imgui, "InputTextFlags", py::arithmetic())
        .value("NONE", ImGuiInputTextFlags_::ImGuiInputTextFlags_None)
        .value("CHARS_DECIMAL", ImGuiInputTextFlags_::ImGuiInputTextFlags_CharsDecimal)
        .value("CHARS_HEXADECIMAL", ImGuiInputTextFlags_::ImGuiInputTextFlags_CharsHexadecimal)
        .value("CHARS_SCIENTIFIC", ImGuiInputTextFlags_::ImGuiInputTextFlags_CharsScientific)
        .value("CHARS_UPPERCASE", ImGuiInputTextFlags_::ImGuiInputTextFlags_CharsUppercase)
        .value("CHARS_NO_BLANK", ImGuiInputTextFlags_::ImGuiInputTextFlags_CharsNoBlank)
        .value("ALLOW_TAB_INPUT", ImGuiInputTextFlags_::ImGuiInputTextFlags_AllowTabInput)
        .value("ENTER_RETURNS_TRUE", ImGuiInputTextFlags_::ImGuiInputTextFlags_EnterReturnsTrue)
        .value("ESCAPE_CLEARS_ALL", ImGuiInputTextFlags_::ImGuiInputTextFlags_EscapeClearsAll)
        .value("CTRL_ENTER_FOR_NEW_LINE", ImGuiInputTextFlags_::ImGuiInputTextFlags_CtrlEnterForNewLine)
        .value("READ_ONLY", ImGuiInputTextFlags_::ImGuiInputTextFlags_ReadOnly)
        .value("PASSWORD", ImGuiInputTextFlags_::ImGuiInputTextFlags_Password)
        .value("ALWAYS_OVERWRITE", ImGuiInputTextFlags_::ImGuiInputTextFlags_AlwaysOverwrite)
        .value("AUTO_SELECT_ALL", ImGuiInputTextFlags_::ImGuiInputTextFlags_AutoSelectAll)
        .value("PARSE_EMPTY_REF_VAL", ImGuiInputTextFlags_::ImGuiInputTextFlags_ParseEmptyRefVal)
        .value("DISPLAY_EMPTY_REF_VAL", ImGuiInputTextFlags_::ImGuiInputTextFlags_DisplayEmptyRefVal)
        .value("NO_HORIZONTAL_SCROLL", ImGuiInputTextFlags_::ImGuiInputTextFlags_NoHorizontalScroll)
        .value("NO_UNDO_REDO", ImGuiInputTextFlags_::ImGuiInputTextFlags_NoUndoRedo)
        .value("ELIDE_LEFT", ImGuiInputTextFlags_::ImGuiInputTextFlags_ElideLeft)
        .value("CALLBACK_COMPLETION", ImGuiInputTextFlags_::ImGuiInputTextFlags_CallbackCompletion)
        .value("CALLBACK_HISTORY", ImGuiInputTextFlags_::ImGuiInputTextFlags_CallbackHistory)
        .value("CALLBACK_ALWAYS", ImGuiInputTextFlags_::ImGuiInputTextFlags_CallbackAlways)
        .value("CALLBACK_CHAR_FILTER", ImGuiInputTextFlags_::ImGuiInputTextFlags_CallbackCharFilter)
        .value("CALLBACK_RESIZE", ImGuiInputTextFlags_::ImGuiInputTextFlags_CallbackResize)
        .value("CALLBACK_EDIT", ImGuiInputTextFlags_::ImGuiInputTextFlags_CallbackEdit)
        .value("WORD_WRAP", ImGuiInputTextFlags_::ImGuiInputTextFlags_WordWrap)
        .export_values()
    ;
    py::enum_<ImGuiTreeNodeFlags_>(_imgui, "TreeNodeFlags", py::arithmetic())
        .value("NONE", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_None)
        .value("SELECTED", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_Selected)
        .value("FRAMED", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_Framed)
        .value("ALLOW_OVERLAP", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_AllowOverlap)
        .value("NO_TREE_PUSH_ON_OPEN", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_NoTreePushOnOpen)
        .value("NO_AUTO_OPEN_ON_LOG", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_NoAutoOpenOnLog)
        .value("DEFAULT_OPEN", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_DefaultOpen)
        .value("OPEN_ON_DOUBLE_CLICK", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_OpenOnDoubleClick)
        .value("OPEN_ON_ARROW", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_OpenOnArrow)
        .value("LEAF", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_Leaf)
        .value("BULLET", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_Bullet)
        .value("FRAME_PADDING", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_FramePadding)
        .value("SPAN_AVAIL_WIDTH", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_SpanAvailWidth)
        .value("SPAN_FULL_WIDTH", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_SpanFullWidth)
        .value("SPAN_LABEL_WIDTH", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_SpanLabelWidth)
        .value("SPAN_ALL_COLUMNS", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_SpanAllColumns)
        .value("LABEL_SPAN_ALL_COLUMNS", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_LabelSpanAllColumns)
        .value("NAV_LEFT_JUMPS_TO_PARENT", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_NavLeftJumpsToParent)
        .value("COLLAPSING_HEADER", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_CollapsingHeader)
        .value("DRAW_LINES_NONE", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_DrawLinesNone)
        .value("DRAW_LINES_FULL", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_DrawLinesFull)
        .value("DRAW_LINES_TO_NODES", ImGuiTreeNodeFlags_::ImGuiTreeNodeFlags_DrawLinesToNodes)
        .export_values()
    ;
    py::enum_<ImGuiPopupFlags_>(_imgui, "PopupFlags", py::arithmetic())
        .value("NONE", ImGuiPopupFlags_::ImGuiPopupFlags_None)
        .value("MOUSE_BUTTON_LEFT", ImGuiPopupFlags_::ImGuiPopupFlags_MouseButtonLeft)
        .value("MOUSE_BUTTON_RIGHT", ImGuiPopupFlags_::ImGuiPopupFlags_MouseButtonRight)
        .value("MOUSE_BUTTON_MIDDLE", ImGuiPopupFlags_::ImGuiPopupFlags_MouseButtonMiddle)
        .value("MOUSE_BUTTON_MASK", ImGuiPopupFlags_::ImGuiPopupFlags_MouseButtonMask_)
        .value("MOUSE_BUTTON_DEFAULT", ImGuiPopupFlags_::ImGuiPopupFlags_MouseButtonDefault_)
        .value("NO_REOPEN", ImGuiPopupFlags_::ImGuiPopupFlags_NoReopen)
        .value("NO_OPEN_OVER_EXISTING_POPUP", ImGuiPopupFlags_::ImGuiPopupFlags_NoOpenOverExistingPopup)
        .value("NO_OPEN_OVER_ITEMS", ImGuiPopupFlags_::ImGuiPopupFlags_NoOpenOverItems)
        .value("ANY_POPUP_ID", ImGuiPopupFlags_::ImGuiPopupFlags_AnyPopupId)
        .value("ANY_POPUP_LEVEL", ImGuiPopupFlags_::ImGuiPopupFlags_AnyPopupLevel)
        .value("ANY_POPUP", ImGuiPopupFlags_::ImGuiPopupFlags_AnyPopup)
        .export_values()
    ;
    py::enum_<ImGuiSelectableFlags_>(_imgui, "SelectableFlags", py::arithmetic())
        .value("NONE", ImGuiSelectableFlags_::ImGuiSelectableFlags_None)
        .value("NO_AUTO_CLOSE_POPUPS", ImGuiSelectableFlags_::ImGuiSelectableFlags_NoAutoClosePopups)
        .value("SPAN_ALL_COLUMNS", ImGuiSelectableFlags_::ImGuiSelectableFlags_SpanAllColumns)
        .value("ALLOW_DOUBLE_CLICK", ImGuiSelectableFlags_::ImGuiSelectableFlags_AllowDoubleClick)
        .value("DISABLED", ImGuiSelectableFlags_::ImGuiSelectableFlags_Disabled)
        .value("ALLOW_OVERLAP", ImGuiSelectableFlags_::ImGuiSelectableFlags_AllowOverlap)
        .value("HIGHLIGHT", ImGuiSelectableFlags_::ImGuiSelectableFlags_Highlight)
        .value("SELECT_ON_NAV", ImGuiSelectableFlags_::ImGuiSelectableFlags_SelectOnNav)
        .export_values()
    ;
    py::enum_<ImGuiComboFlags_>(_imgui, "ComboFlags", py::arithmetic())
        .value("NONE", ImGuiComboFlags_::ImGuiComboFlags_None)
        .value("POPUP_ALIGN_LEFT", ImGuiComboFlags_::ImGuiComboFlags_PopupAlignLeft)
        .value("HEIGHT_SMALL", ImGuiComboFlags_::ImGuiComboFlags_HeightSmall)
        .value("HEIGHT_REGULAR", ImGuiComboFlags_::ImGuiComboFlags_HeightRegular)
        .value("HEIGHT_LARGE", ImGuiComboFlags_::ImGuiComboFlags_HeightLarge)
        .value("HEIGHT_LARGEST", ImGuiComboFlags_::ImGuiComboFlags_HeightLargest)
        .value("NO_ARROW_BUTTON", ImGuiComboFlags_::ImGuiComboFlags_NoArrowButton)
        .value("NO_PREVIEW", ImGuiComboFlags_::ImGuiComboFlags_NoPreview)
        .value("WIDTH_FIT_PREVIEW", ImGuiComboFlags_::ImGuiComboFlags_WidthFitPreview)
        .value("HEIGHT_MASK", ImGuiComboFlags_::ImGuiComboFlags_HeightMask_)
        .export_values()
    ;
    py::enum_<ImGuiTabBarFlags_>(_imgui, "TabBarFlags", py::arithmetic())
        .value("NONE", ImGuiTabBarFlags_::ImGuiTabBarFlags_None)
        .value("REORDERABLE", ImGuiTabBarFlags_::ImGuiTabBarFlags_Reorderable)
        .value("AUTO_SELECT_NEW_TABS", ImGuiTabBarFlags_::ImGuiTabBarFlags_AutoSelectNewTabs)
        .value("TAB_LIST_POPUP_BUTTON", ImGuiTabBarFlags_::ImGuiTabBarFlags_TabListPopupButton)
        .value("NO_CLOSE_WITH_MIDDLE_MOUSE_BUTTON", ImGuiTabBarFlags_::ImGuiTabBarFlags_NoCloseWithMiddleMouseButton)
        .value("NO_TAB_LIST_SCROLLING_BUTTONS", ImGuiTabBarFlags_::ImGuiTabBarFlags_NoTabListScrollingButtons)
        .value("NO_TOOLTIP", ImGuiTabBarFlags_::ImGuiTabBarFlags_NoTooltip)
        .value("DRAW_SELECTED_OVERLINE", ImGuiTabBarFlags_::ImGuiTabBarFlags_DrawSelectedOverline)
        .value("FITTING_POLICY_MIXED", ImGuiTabBarFlags_::ImGuiTabBarFlags_FittingPolicyMixed)
        .value("FITTING_POLICY_SHRINK", ImGuiTabBarFlags_::ImGuiTabBarFlags_FittingPolicyShrink)
        .value("FITTING_POLICY_SCROLL", ImGuiTabBarFlags_::ImGuiTabBarFlags_FittingPolicyScroll)
        .value("FITTING_POLICY_MASK", ImGuiTabBarFlags_::ImGuiTabBarFlags_FittingPolicyMask_)
        .value("FITTING_POLICY_DEFAULT", ImGuiTabBarFlags_::ImGuiTabBarFlags_FittingPolicyDefault_)
        .export_values()
    ;
    py::enum_<ImGuiTabItemFlags_>(_imgui, "TabItemFlags", py::arithmetic())
        .value("NONE", ImGuiTabItemFlags_::ImGuiTabItemFlags_None)
        .value("UNSAVED_DOCUMENT", ImGuiTabItemFlags_::ImGuiTabItemFlags_UnsavedDocument)
        .value("SET_SELECTED", ImGuiTabItemFlags_::ImGuiTabItemFlags_SetSelected)
        .value("NO_CLOSE_WITH_MIDDLE_MOUSE_BUTTON", ImGuiTabItemFlags_::ImGuiTabItemFlags_NoCloseWithMiddleMouseButton)
        .value("NO_PUSH_ID", ImGuiTabItemFlags_::ImGuiTabItemFlags_NoPushId)
        .value("NO_TOOLTIP", ImGuiTabItemFlags_::ImGuiTabItemFlags_NoTooltip)
        .value("NO_REORDER", ImGuiTabItemFlags_::ImGuiTabItemFlags_NoReorder)
        .value("LEADING", ImGuiTabItemFlags_::ImGuiTabItemFlags_Leading)
        .value("TRAILING", ImGuiTabItemFlags_::ImGuiTabItemFlags_Trailing)
        .value("NO_ASSUMED_CLOSURE", ImGuiTabItemFlags_::ImGuiTabItemFlags_NoAssumedClosure)
        .export_values()
    ;
    py::enum_<ImGuiFocusedFlags_>(_imgui, "FocusedFlags", py::arithmetic())
        .value("NONE", ImGuiFocusedFlags_::ImGuiFocusedFlags_None)
        .value("CHILD_WINDOWS", ImGuiFocusedFlags_::ImGuiFocusedFlags_ChildWindows)
        .value("ROOT_WINDOW", ImGuiFocusedFlags_::ImGuiFocusedFlags_RootWindow)
        .value("ANY_WINDOW", ImGuiFocusedFlags_::ImGuiFocusedFlags_AnyWindow)
        .value("NO_POPUP_HIERARCHY", ImGuiFocusedFlags_::ImGuiFocusedFlags_NoPopupHierarchy)
        .value("DOCK_HIERARCHY", ImGuiFocusedFlags_::ImGuiFocusedFlags_DockHierarchy)
        .value("ROOT_AND_CHILD_WINDOWS", ImGuiFocusedFlags_::ImGuiFocusedFlags_RootAndChildWindows)
        .export_values()
    ;
    py::enum_<ImGuiHoveredFlags_>(_imgui, "HoveredFlags", py::arithmetic())
        .value("NONE", ImGuiHoveredFlags_::ImGuiHoveredFlags_None)
        .value("CHILD_WINDOWS", ImGuiHoveredFlags_::ImGuiHoveredFlags_ChildWindows)
        .value("ROOT_WINDOW", ImGuiHoveredFlags_::ImGuiHoveredFlags_RootWindow)
        .value("ANY_WINDOW", ImGuiHoveredFlags_::ImGuiHoveredFlags_AnyWindow)
        .value("NO_POPUP_HIERARCHY", ImGuiHoveredFlags_::ImGuiHoveredFlags_NoPopupHierarchy)
        .value("DOCK_HIERARCHY", ImGuiHoveredFlags_::ImGuiHoveredFlags_DockHierarchy)
        .value("ALLOW_WHEN_BLOCKED_BY_POPUP", ImGuiHoveredFlags_::ImGuiHoveredFlags_AllowWhenBlockedByPopup)
        .value("ALLOW_WHEN_BLOCKED_BY_ACTIVE_ITEM", ImGuiHoveredFlags_::ImGuiHoveredFlags_AllowWhenBlockedByActiveItem)
        .value("ALLOW_WHEN_OVERLAPPED_BY_ITEM", ImGuiHoveredFlags_::ImGuiHoveredFlags_AllowWhenOverlappedByItem)
        .value("ALLOW_WHEN_OVERLAPPED_BY_WINDOW", ImGuiHoveredFlags_::ImGuiHoveredFlags_AllowWhenOverlappedByWindow)
        .value("ALLOW_WHEN_DISABLED", ImGuiHoveredFlags_::ImGuiHoveredFlags_AllowWhenDisabled)
        .value("NO_NAV_OVERRIDE", ImGuiHoveredFlags_::ImGuiHoveredFlags_NoNavOverride)
        .value("ALLOW_WHEN_OVERLAPPED", ImGuiHoveredFlags_::ImGuiHoveredFlags_AllowWhenOverlapped)
        .value("RECT_ONLY", ImGuiHoveredFlags_::ImGuiHoveredFlags_RectOnly)
        .value("ROOT_AND_CHILD_WINDOWS", ImGuiHoveredFlags_::ImGuiHoveredFlags_RootAndChildWindows)
        .value("FOR_TOOLTIP", ImGuiHoveredFlags_::ImGuiHoveredFlags_ForTooltip)
        .value("STATIONARY", ImGuiHoveredFlags_::ImGuiHoveredFlags_Stationary)
        .value("DELAY_NONE", ImGuiHoveredFlags_::ImGuiHoveredFlags_DelayNone)
        .value("DELAY_SHORT", ImGuiHoveredFlags_::ImGuiHoveredFlags_DelayShort)
        .value("DELAY_NORMAL", ImGuiHoveredFlags_::ImGuiHoveredFlags_DelayNormal)
        .value("NO_SHARED_DELAY", ImGuiHoveredFlags_::ImGuiHoveredFlags_NoSharedDelay)
        .export_values()
    ;
    py::enum_<ImGuiDockNodeFlags_>(_imgui, "DockNodeFlags", py::arithmetic())
        .value("NONE", ImGuiDockNodeFlags_::ImGuiDockNodeFlags_None)
        .value("KEEP_ALIVE_ONLY", ImGuiDockNodeFlags_::ImGuiDockNodeFlags_KeepAliveOnly)
        .value("NO_DOCKING_OVER_CENTRAL_NODE", ImGuiDockNodeFlags_::ImGuiDockNodeFlags_NoDockingOverCentralNode)
        .value("PASSTHRU_CENTRAL_NODE", ImGuiDockNodeFlags_::ImGuiDockNodeFlags_PassthruCentralNode)
        .value("NO_DOCKING_SPLIT", ImGuiDockNodeFlags_::ImGuiDockNodeFlags_NoDockingSplit)
        .value("NO_RESIZE", ImGuiDockNodeFlags_::ImGuiDockNodeFlags_NoResize)
        .value("AUTO_HIDE_TAB_BAR", ImGuiDockNodeFlags_::ImGuiDockNodeFlags_AutoHideTabBar)
        .value("NO_UNDOCKING", ImGuiDockNodeFlags_::ImGuiDockNodeFlags_NoUndocking)
        .export_values()
    ;
    py::enum_<ImGuiDragDropFlags_>(_imgui, "DragDropFlags", py::arithmetic())
        .value("NONE", ImGuiDragDropFlags_::ImGuiDragDropFlags_None)
        .value("SOURCE_NO_PREVIEW_TOOLTIP", ImGuiDragDropFlags_::ImGuiDragDropFlags_SourceNoPreviewTooltip)
        .value("SOURCE_NO_DISABLE_HOVER", ImGuiDragDropFlags_::ImGuiDragDropFlags_SourceNoDisableHover)
        .value("SOURCE_NO_HOLD_TO_OPEN_OTHERS", ImGuiDragDropFlags_::ImGuiDragDropFlags_SourceNoHoldToOpenOthers)
        .value("SOURCE_ALLOW_NULL_ID", ImGuiDragDropFlags_::ImGuiDragDropFlags_SourceAllowNullID)
        .value("SOURCE_EXTERN", ImGuiDragDropFlags_::ImGuiDragDropFlags_SourceExtern)
        .value("PAYLOAD_AUTO_EXPIRE", ImGuiDragDropFlags_::ImGuiDragDropFlags_PayloadAutoExpire)
        .value("PAYLOAD_NO_CROSS_CONTEXT", ImGuiDragDropFlags_::ImGuiDragDropFlags_PayloadNoCrossContext)
        .value("PAYLOAD_NO_CROSS_PROCESS", ImGuiDragDropFlags_::ImGuiDragDropFlags_PayloadNoCrossProcess)
        .value("ACCEPT_BEFORE_DELIVERY", ImGuiDragDropFlags_::ImGuiDragDropFlags_AcceptBeforeDelivery)
        .value("ACCEPT_NO_DRAW_DEFAULT_RECT", ImGuiDragDropFlags_::ImGuiDragDropFlags_AcceptNoDrawDefaultRect)
        .value("ACCEPT_NO_PREVIEW_TOOLTIP", ImGuiDragDropFlags_::ImGuiDragDropFlags_AcceptNoPreviewTooltip)
        .value("ACCEPT_PEEK_ONLY", ImGuiDragDropFlags_::ImGuiDragDropFlags_AcceptPeekOnly)
        .export_values()
    ;
    py::enum_<ImGuiDataType_>(_imgui, "DataType", py::arithmetic())
        .value("S8", ImGuiDataType_::ImGuiDataType_S8)
        .value("U8", ImGuiDataType_::ImGuiDataType_U8)
        .value("S16", ImGuiDataType_::ImGuiDataType_S16)
        .value("U16", ImGuiDataType_::ImGuiDataType_U16)
        .value("S32", ImGuiDataType_::ImGuiDataType_S32)
        .value("U32", ImGuiDataType_::ImGuiDataType_U32)
        .value("S64", ImGuiDataType_::ImGuiDataType_S64)
        .value("U64", ImGuiDataType_::ImGuiDataType_U64)
        .value("FLOAT", ImGuiDataType_::ImGuiDataType_Float)
        .value("DOUBLE", ImGuiDataType_::ImGuiDataType_Double)
        .value("BOOL", ImGuiDataType_::ImGuiDataType_Bool)
        .value("STRING", ImGuiDataType_::ImGuiDataType_String)
        .value("COUNT", ImGuiDataType_::ImGuiDataType_COUNT)
        .export_values()
    ;
    py::enum_<ImGuiDir>(_imgui, "Dir", py::arithmetic())
        .value("NONE", ImGuiDir::ImGuiDir_None)
        .value("LEFT", ImGuiDir::ImGuiDir_Left)
        .value("RIGHT", ImGuiDir::ImGuiDir_Right)
        .value("UP", ImGuiDir::ImGuiDir_Up)
        .value("DOWN", ImGuiDir::ImGuiDir_Down)
        .value("COUNT", ImGuiDir::ImGuiDir_COUNT)
        .export_values()
    ;
    py::enum_<ImGuiSortDirection>(_imgui, "SortDirection", py::arithmetic())
        .value("NONE", ImGuiSortDirection::ImGuiSortDirection_None)
        .value("ASCENDING", ImGuiSortDirection::ImGuiSortDirection_Ascending)
        .value("DESCENDING", ImGuiSortDirection::ImGuiSortDirection_Descending)
        .export_values()
    ;
    py::enum_<ImGuiKey>(_imgui, "Key", py::arithmetic())
        .value("NONE", ImGuiKey::ImGuiKey_None)
        .value("NAMED_KEY_BEGIN", ImGuiKey::ImGuiKey_NamedKey_BEGIN)
        .value("TAB", ImGuiKey::ImGuiKey_Tab)
        .value("LEFT_ARROW", ImGuiKey::ImGuiKey_LeftArrow)
        .value("RIGHT_ARROW", ImGuiKey::ImGuiKey_RightArrow)
        .value("UP_ARROW", ImGuiKey::ImGuiKey_UpArrow)
        .value("DOWN_ARROW", ImGuiKey::ImGuiKey_DownArrow)
        .value("PAGE_UP", ImGuiKey::ImGuiKey_PageUp)
        .value("PAGE_DOWN", ImGuiKey::ImGuiKey_PageDown)
        .value("HOME", ImGuiKey::ImGuiKey_Home)
        .value("END", ImGuiKey::ImGuiKey_End)
        .value("INSERT", ImGuiKey::ImGuiKey_Insert)
        .value("DELETE", ImGuiKey::ImGuiKey_Delete)
        .value("BACKSPACE", ImGuiKey::ImGuiKey_Backspace)
        .value("SPACE", ImGuiKey::ImGuiKey_Space)
        .value("ENTER", ImGuiKey::ImGuiKey_Enter)
        .value("ESCAPE", ImGuiKey::ImGuiKey_Escape)
        .value("LEFT_CTRL", ImGuiKey::ImGuiKey_LeftCtrl)
        .value("LEFT_SHIFT", ImGuiKey::ImGuiKey_LeftShift)
        .value("LEFT_ALT", ImGuiKey::ImGuiKey_LeftAlt)
        .value("LEFT_SUPER", ImGuiKey::ImGuiKey_LeftSuper)
        .value("RIGHT_CTRL", ImGuiKey::ImGuiKey_RightCtrl)
        .value("RIGHT_SHIFT", ImGuiKey::ImGuiKey_RightShift)
        .value("RIGHT_ALT", ImGuiKey::ImGuiKey_RightAlt)
        .value("RIGHT_SUPER", ImGuiKey::ImGuiKey_RightSuper)
        .value("MENU", ImGuiKey::ImGuiKey_Menu)
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
        .value("A", ImGuiKey::ImGuiKey_A)
        .value("B", ImGuiKey::ImGuiKey_B)
        .value("C", ImGuiKey::ImGuiKey_C)
        .value("D", ImGuiKey::ImGuiKey_D)
        .value("E", ImGuiKey::ImGuiKey_E)
        .value("F", ImGuiKey::ImGuiKey_F)
        .value("G", ImGuiKey::ImGuiKey_G)
        .value("H", ImGuiKey::ImGuiKey_H)
        .value("I", ImGuiKey::ImGuiKey_I)
        .value("J", ImGuiKey::ImGuiKey_J)
        .value("K", ImGuiKey::ImGuiKey_K)
        .value("L", ImGuiKey::ImGuiKey_L)
        .value("M", ImGuiKey::ImGuiKey_M)
        .value("N", ImGuiKey::ImGuiKey_N)
        .value("O", ImGuiKey::ImGuiKey_O)
        .value("P", ImGuiKey::ImGuiKey_P)
        .value("Q", ImGuiKey::ImGuiKey_Q)
        .value("R", ImGuiKey::ImGuiKey_R)
        .value("S", ImGuiKey::ImGuiKey_S)
        .value("T", ImGuiKey::ImGuiKey_T)
        .value("U", ImGuiKey::ImGuiKey_U)
        .value("V", ImGuiKey::ImGuiKey_V)
        .value("W", ImGuiKey::ImGuiKey_W)
        .value("X", ImGuiKey::ImGuiKey_X)
        .value("Y", ImGuiKey::ImGuiKey_Y)
        .value("Z", ImGuiKey::ImGuiKey_Z)
        .value("F1", ImGuiKey::ImGuiKey_F1)
        .value("F2", ImGuiKey::ImGuiKey_F2)
        .value("F3", ImGuiKey::ImGuiKey_F3)
        .value("F4", ImGuiKey::ImGuiKey_F4)
        .value("F5", ImGuiKey::ImGuiKey_F5)
        .value("F6", ImGuiKey::ImGuiKey_F6)
        .value("F7", ImGuiKey::ImGuiKey_F7)
        .value("F8", ImGuiKey::ImGuiKey_F8)
        .value("F9", ImGuiKey::ImGuiKey_F9)
        .value("F10", ImGuiKey::ImGuiKey_F10)
        .value("F11", ImGuiKey::ImGuiKey_F11)
        .value("F12", ImGuiKey::ImGuiKey_F12)
        .value("F13", ImGuiKey::ImGuiKey_F13)
        .value("F14", ImGuiKey::ImGuiKey_F14)
        .value("F15", ImGuiKey::ImGuiKey_F15)
        .value("F16", ImGuiKey::ImGuiKey_F16)
        .value("F17", ImGuiKey::ImGuiKey_F17)
        .value("F18", ImGuiKey::ImGuiKey_F18)
        .value("F19", ImGuiKey::ImGuiKey_F19)
        .value("F20", ImGuiKey::ImGuiKey_F20)
        .value("F21", ImGuiKey::ImGuiKey_F21)
        .value("F22", ImGuiKey::ImGuiKey_F22)
        .value("F23", ImGuiKey::ImGuiKey_F23)
        .value("F24", ImGuiKey::ImGuiKey_F24)
        .value("APOSTROPHE", ImGuiKey::ImGuiKey_Apostrophe)
        .value("COMMA", ImGuiKey::ImGuiKey_Comma)
        .value("MINUS", ImGuiKey::ImGuiKey_Minus)
        .value("PERIOD", ImGuiKey::ImGuiKey_Period)
        .value("SLASH", ImGuiKey::ImGuiKey_Slash)
        .value("SEMICOLON", ImGuiKey::ImGuiKey_Semicolon)
        .value("EQUAL", ImGuiKey::ImGuiKey_Equal)
        .value("LEFT_BRACKET", ImGuiKey::ImGuiKey_LeftBracket)
        .value("BACKSLASH", ImGuiKey::ImGuiKey_Backslash)
        .value("RIGHT_BRACKET", ImGuiKey::ImGuiKey_RightBracket)
        .value("GRAVE_ACCENT", ImGuiKey::ImGuiKey_GraveAccent)
        .value("CAPS_LOCK", ImGuiKey::ImGuiKey_CapsLock)
        .value("SCROLL_LOCK", ImGuiKey::ImGuiKey_ScrollLock)
        .value("NUM_LOCK", ImGuiKey::ImGuiKey_NumLock)
        .value("PRINT_SCREEN", ImGuiKey::ImGuiKey_PrintScreen)
        .value("PAUSE", ImGuiKey::ImGuiKey_Pause)
        .value("KEYPAD0", ImGuiKey::ImGuiKey_Keypad0)
        .value("KEYPAD1", ImGuiKey::ImGuiKey_Keypad1)
        .value("KEYPAD2", ImGuiKey::ImGuiKey_Keypad2)
        .value("KEYPAD3", ImGuiKey::ImGuiKey_Keypad3)
        .value("KEYPAD4", ImGuiKey::ImGuiKey_Keypad4)
        .value("KEYPAD5", ImGuiKey::ImGuiKey_Keypad5)
        .value("KEYPAD6", ImGuiKey::ImGuiKey_Keypad6)
        .value("KEYPAD7", ImGuiKey::ImGuiKey_Keypad7)
        .value("KEYPAD8", ImGuiKey::ImGuiKey_Keypad8)
        .value("KEYPAD9", ImGuiKey::ImGuiKey_Keypad9)
        .value("KEYPAD_DECIMAL", ImGuiKey::ImGuiKey_KeypadDecimal)
        .value("KEYPAD_DIVIDE", ImGuiKey::ImGuiKey_KeypadDivide)
        .value("KEYPAD_MULTIPLY", ImGuiKey::ImGuiKey_KeypadMultiply)
        .value("KEYPAD_SUBTRACT", ImGuiKey::ImGuiKey_KeypadSubtract)
        .value("KEYPAD_ADD", ImGuiKey::ImGuiKey_KeypadAdd)
        .value("KEYPAD_ENTER", ImGuiKey::ImGuiKey_KeypadEnter)
        .value("KEYPAD_EQUAL", ImGuiKey::ImGuiKey_KeypadEqual)
        .value("APP_BACK", ImGuiKey::ImGuiKey_AppBack)
        .value("APP_FORWARD", ImGuiKey::ImGuiKey_AppForward)
        .value("OEM102", ImGuiKey::ImGuiKey_Oem102)
        .value("GAMEPAD_START", ImGuiKey::ImGuiKey_GamepadStart)
        .value("GAMEPAD_BACK", ImGuiKey::ImGuiKey_GamepadBack)
        .value("GAMEPAD_FACE_LEFT", ImGuiKey::ImGuiKey_GamepadFaceLeft)
        .value("GAMEPAD_FACE_RIGHT", ImGuiKey::ImGuiKey_GamepadFaceRight)
        .value("GAMEPAD_FACE_UP", ImGuiKey::ImGuiKey_GamepadFaceUp)
        .value("GAMEPAD_FACE_DOWN", ImGuiKey::ImGuiKey_GamepadFaceDown)
        .value("GAMEPAD_DPAD_LEFT", ImGuiKey::ImGuiKey_GamepadDpadLeft)
        .value("GAMEPAD_DPAD_RIGHT", ImGuiKey::ImGuiKey_GamepadDpadRight)
        .value("GAMEPAD_DPAD_UP", ImGuiKey::ImGuiKey_GamepadDpadUp)
        .value("GAMEPAD_DPAD_DOWN", ImGuiKey::ImGuiKey_GamepadDpadDown)
        .value("GAMEPAD_L1", ImGuiKey::ImGuiKey_GamepadL1)
        .value("GAMEPAD_R1", ImGuiKey::ImGuiKey_GamepadR1)
        .value("GAMEPAD_L2", ImGuiKey::ImGuiKey_GamepadL2)
        .value("GAMEPAD_R2", ImGuiKey::ImGuiKey_GamepadR2)
        .value("GAMEPAD_L3", ImGuiKey::ImGuiKey_GamepadL3)
        .value("GAMEPAD_R3", ImGuiKey::ImGuiKey_GamepadR3)
        .value("GAMEPAD_L_STICK_LEFT", ImGuiKey::ImGuiKey_GamepadLStickLeft)
        .value("GAMEPAD_L_STICK_RIGHT", ImGuiKey::ImGuiKey_GamepadLStickRight)
        .value("GAMEPAD_L_STICK_UP", ImGuiKey::ImGuiKey_GamepadLStickUp)
        .value("GAMEPAD_L_STICK_DOWN", ImGuiKey::ImGuiKey_GamepadLStickDown)
        .value("GAMEPAD_R_STICK_LEFT", ImGuiKey::ImGuiKey_GamepadRStickLeft)
        .value("GAMEPAD_R_STICK_RIGHT", ImGuiKey::ImGuiKey_GamepadRStickRight)
        .value("GAMEPAD_R_STICK_UP", ImGuiKey::ImGuiKey_GamepadRStickUp)
        .value("GAMEPAD_R_STICK_DOWN", ImGuiKey::ImGuiKey_GamepadRStickDown)
        .value("MOUSE_LEFT", ImGuiKey::ImGuiKey_MouseLeft)
        .value("MOUSE_RIGHT", ImGuiKey::ImGuiKey_MouseRight)
        .value("MOUSE_MIDDLE", ImGuiKey::ImGuiKey_MouseMiddle)
        .value("MOUSE_X1", ImGuiKey::ImGuiKey_MouseX1)
        .value("MOUSE_X2", ImGuiKey::ImGuiKey_MouseX2)
        .value("MOUSE_WHEEL_X", ImGuiKey::ImGuiKey_MouseWheelX)
        .value("MOUSE_WHEEL_Y", ImGuiKey::ImGuiKey_MouseWheelY)
        .value("RESERVED_FOR_MOD_CTRL", ImGuiKey::ImGuiKey_ReservedForModCtrl)
        .value("RESERVED_FOR_MOD_SHIFT", ImGuiKey::ImGuiKey_ReservedForModShift)
        .value("RESERVED_FOR_MOD_ALT", ImGuiKey::ImGuiKey_ReservedForModAlt)
        .value("RESERVED_FOR_MOD_SUPER", ImGuiKey::ImGuiKey_ReservedForModSuper)
        .value("NAMED_KEY_END", ImGuiKey::ImGuiKey_NamedKey_END)
        .value("NAMED_KEY_COUNT", ImGuiKey::ImGuiKey_NamedKey_COUNT)
        .value("MOD_NONE", ImGuiKey::ImGuiMod_None)
        .value("MOD_CTRL", ImGuiKey::ImGuiMod_Ctrl)
        .value("MOD_SHIFT", ImGuiKey::ImGuiMod_Shift)
        .value("MOD_ALT", ImGuiKey::ImGuiMod_Alt)
        .value("MOD_SUPER", ImGuiKey::ImGuiMod_Super)
        .value("MOD_MASK", ImGuiKey::ImGuiMod_Mask_)
        .export_values()
    ;
    py::enum_<ImGuiInputFlags_>(_imgui, "InputFlags", py::arithmetic())
        .value("NONE", ImGuiInputFlags_::ImGuiInputFlags_None)
        .value("REPEAT", ImGuiInputFlags_::ImGuiInputFlags_Repeat)
        .value("ROUTE_ACTIVE", ImGuiInputFlags_::ImGuiInputFlags_RouteActive)
        .value("ROUTE_FOCUSED", ImGuiInputFlags_::ImGuiInputFlags_RouteFocused)
        .value("ROUTE_GLOBAL", ImGuiInputFlags_::ImGuiInputFlags_RouteGlobal)
        .value("ROUTE_ALWAYS", ImGuiInputFlags_::ImGuiInputFlags_RouteAlways)
        .value("ROUTE_OVER_FOCUSED", ImGuiInputFlags_::ImGuiInputFlags_RouteOverFocused)
        .value("ROUTE_OVER_ACTIVE", ImGuiInputFlags_::ImGuiInputFlags_RouteOverActive)
        .value("ROUTE_UNLESS_BG_FOCUSED", ImGuiInputFlags_::ImGuiInputFlags_RouteUnlessBgFocused)
        .value("ROUTE_FROM_ROOT_WINDOW", ImGuiInputFlags_::ImGuiInputFlags_RouteFromRootWindow)
        .value("TOOLTIP", ImGuiInputFlags_::ImGuiInputFlags_Tooltip)
        .export_values()
    ;
    py::enum_<ImGuiConfigFlags_>(_imgui, "ConfigFlags", py::arithmetic())
        .value("NONE", ImGuiConfigFlags_::ImGuiConfigFlags_None)
        .value("NAV_ENABLE_KEYBOARD", ImGuiConfigFlags_::ImGuiConfigFlags_NavEnableKeyboard)
        .value("NAV_ENABLE_GAMEPAD", ImGuiConfigFlags_::ImGuiConfigFlags_NavEnableGamepad)
        .value("NO_MOUSE", ImGuiConfigFlags_::ImGuiConfigFlags_NoMouse)
        .value("NO_MOUSE_CURSOR_CHANGE", ImGuiConfigFlags_::ImGuiConfigFlags_NoMouseCursorChange)
        .value("NO_KEYBOARD", ImGuiConfigFlags_::ImGuiConfigFlags_NoKeyboard)
        .value("DOCKING_ENABLE", ImGuiConfigFlags_::ImGuiConfigFlags_DockingEnable)
        .value("VIEWPORTS_ENABLE", ImGuiConfigFlags_::ImGuiConfigFlags_ViewportsEnable)
        .value("IS_SRGB", ImGuiConfigFlags_::ImGuiConfigFlags_IsSRGB)
        .value("IS_TOUCH_SCREEN", ImGuiConfigFlags_::ImGuiConfigFlags_IsTouchScreen)
        .export_values()
    ;
    py::enum_<ImGuiBackendFlags_>(_imgui, "BackendFlags", py::arithmetic())
        .value("NONE", ImGuiBackendFlags_::ImGuiBackendFlags_None)
        .value("HAS_GAMEPAD", ImGuiBackendFlags_::ImGuiBackendFlags_HasGamepad)
        .value("HAS_MOUSE_CURSORS", ImGuiBackendFlags_::ImGuiBackendFlags_HasMouseCursors)
        .value("HAS_SET_MOUSE_POS", ImGuiBackendFlags_::ImGuiBackendFlags_HasSetMousePos)
        .value("RENDERER_HAS_VTX_OFFSET", ImGuiBackendFlags_::ImGuiBackendFlags_RendererHasVtxOffset)
        .value("RENDERER_HAS_TEXTURES", ImGuiBackendFlags_::ImGuiBackendFlags_RendererHasTextures)
        .value("PLATFORM_HAS_VIEWPORTS", ImGuiBackendFlags_::ImGuiBackendFlags_PlatformHasViewports)
        .value("HAS_MOUSE_HOVERED_VIEWPORT", ImGuiBackendFlags_::ImGuiBackendFlags_HasMouseHoveredViewport)
        .value("RENDERER_HAS_VIEWPORTS", ImGuiBackendFlags_::ImGuiBackendFlags_RendererHasViewports)
        .export_values()
    ;
    py::enum_<ImGuiCol_>(_imgui, "Col", py::arithmetic())
        .value("TEXT", ImGuiCol_::ImGuiCol_Text)
        .value("TEXT_DISABLED", ImGuiCol_::ImGuiCol_TextDisabled)
        .value("WINDOW_BG", ImGuiCol_::ImGuiCol_WindowBg)
        .value("CHILD_BG", ImGuiCol_::ImGuiCol_ChildBg)
        .value("POPUP_BG", ImGuiCol_::ImGuiCol_PopupBg)
        .value("BORDER", ImGuiCol_::ImGuiCol_Border)
        .value("BORDER_SHADOW", ImGuiCol_::ImGuiCol_BorderShadow)
        .value("FRAME_BG", ImGuiCol_::ImGuiCol_FrameBg)
        .value("FRAME_BG_HOVERED", ImGuiCol_::ImGuiCol_FrameBgHovered)
        .value("FRAME_BG_ACTIVE", ImGuiCol_::ImGuiCol_FrameBgActive)
        .value("TITLE_BG", ImGuiCol_::ImGuiCol_TitleBg)
        .value("TITLE_BG_ACTIVE", ImGuiCol_::ImGuiCol_TitleBgActive)
        .value("TITLE_BG_COLLAPSED", ImGuiCol_::ImGuiCol_TitleBgCollapsed)
        .value("MENU_BAR_BG", ImGuiCol_::ImGuiCol_MenuBarBg)
        .value("SCROLLBAR_BG", ImGuiCol_::ImGuiCol_ScrollbarBg)
        .value("SCROLLBAR_GRAB", ImGuiCol_::ImGuiCol_ScrollbarGrab)
        .value("SCROLLBAR_GRAB_HOVERED", ImGuiCol_::ImGuiCol_ScrollbarGrabHovered)
        .value("SCROLLBAR_GRAB_ACTIVE", ImGuiCol_::ImGuiCol_ScrollbarGrabActive)
        .value("CHECK_MARK", ImGuiCol_::ImGuiCol_CheckMark)
        .value("SLIDER_GRAB", ImGuiCol_::ImGuiCol_SliderGrab)
        .value("SLIDER_GRAB_ACTIVE", ImGuiCol_::ImGuiCol_SliderGrabActive)
        .value("BUTTON", ImGuiCol_::ImGuiCol_Button)
        .value("BUTTON_HOVERED", ImGuiCol_::ImGuiCol_ButtonHovered)
        .value("BUTTON_ACTIVE", ImGuiCol_::ImGuiCol_ButtonActive)
        .value("HEADER", ImGuiCol_::ImGuiCol_Header)
        .value("HEADER_HOVERED", ImGuiCol_::ImGuiCol_HeaderHovered)
        .value("HEADER_ACTIVE", ImGuiCol_::ImGuiCol_HeaderActive)
        .value("SEPARATOR", ImGuiCol_::ImGuiCol_Separator)
        .value("SEPARATOR_HOVERED", ImGuiCol_::ImGuiCol_SeparatorHovered)
        .value("SEPARATOR_ACTIVE", ImGuiCol_::ImGuiCol_SeparatorActive)
        .value("RESIZE_GRIP", ImGuiCol_::ImGuiCol_ResizeGrip)
        .value("RESIZE_GRIP_HOVERED", ImGuiCol_::ImGuiCol_ResizeGripHovered)
        .value("RESIZE_GRIP_ACTIVE", ImGuiCol_::ImGuiCol_ResizeGripActive)
        .value("INPUT_TEXT_CURSOR", ImGuiCol_::ImGuiCol_InputTextCursor)
        .value("TAB_HOVERED", ImGuiCol_::ImGuiCol_TabHovered)
        .value("TAB", ImGuiCol_::ImGuiCol_Tab)
        .value("TAB_SELECTED", ImGuiCol_::ImGuiCol_TabSelected)
        .value("TAB_SELECTED_OVERLINE", ImGuiCol_::ImGuiCol_TabSelectedOverline)
        .value("TAB_DIMMED", ImGuiCol_::ImGuiCol_TabDimmed)
        .value("TAB_DIMMED_SELECTED", ImGuiCol_::ImGuiCol_TabDimmedSelected)
        .value("TAB_DIMMED_SELECTED_OVERLINE", ImGuiCol_::ImGuiCol_TabDimmedSelectedOverline)
        .value("DOCKING_PREVIEW", ImGuiCol_::ImGuiCol_DockingPreview)
        .value("DOCKING_EMPTY_BG", ImGuiCol_::ImGuiCol_DockingEmptyBg)
        .value("PLOT_LINES", ImGuiCol_::ImGuiCol_PlotLines)
        .value("PLOT_LINES_HOVERED", ImGuiCol_::ImGuiCol_PlotLinesHovered)
        .value("PLOT_HISTOGRAM", ImGuiCol_::ImGuiCol_PlotHistogram)
        .value("PLOT_HISTOGRAM_HOVERED", ImGuiCol_::ImGuiCol_PlotHistogramHovered)
        .value("TABLE_HEADER_BG", ImGuiCol_::ImGuiCol_TableHeaderBg)
        .value("TABLE_BORDER_STRONG", ImGuiCol_::ImGuiCol_TableBorderStrong)
        .value("TABLE_BORDER_LIGHT", ImGuiCol_::ImGuiCol_TableBorderLight)
        .value("TABLE_ROW_BG", ImGuiCol_::ImGuiCol_TableRowBg)
        .value("TABLE_ROW_BG_ALT", ImGuiCol_::ImGuiCol_TableRowBgAlt)
        .value("TEXT_LINK", ImGuiCol_::ImGuiCol_TextLink)
        .value("TEXT_SELECTED_BG", ImGuiCol_::ImGuiCol_TextSelectedBg)
        .value("TREE_LINES", ImGuiCol_::ImGuiCol_TreeLines)
        .value("DRAG_DROP_TARGET", ImGuiCol_::ImGuiCol_DragDropTarget)
        .value("NAV_CURSOR", ImGuiCol_::ImGuiCol_NavCursor)
        .value("NAV_WINDOWING_HIGHLIGHT", ImGuiCol_::ImGuiCol_NavWindowingHighlight)
        .value("NAV_WINDOWING_DIM_BG", ImGuiCol_::ImGuiCol_NavWindowingDimBg)
        .value("MODAL_WINDOW_DIM_BG", ImGuiCol_::ImGuiCol_ModalWindowDimBg)
        .value("COUNT", ImGuiCol_::ImGuiCol_COUNT)
        .export_values()
    ;
    py::enum_<ImGuiStyleVar_>(_imgui, "StyleVar", py::arithmetic())
        .value("ALPHA", ImGuiStyleVar_::ImGuiStyleVar_Alpha)
        .value("DISABLED_ALPHA", ImGuiStyleVar_::ImGuiStyleVar_DisabledAlpha)
        .value("WINDOW_PADDING", ImGuiStyleVar_::ImGuiStyleVar_WindowPadding)
        .value("WINDOW_ROUNDING", ImGuiStyleVar_::ImGuiStyleVar_WindowRounding)
        .value("WINDOW_BORDER_SIZE", ImGuiStyleVar_::ImGuiStyleVar_WindowBorderSize)
        .value("WINDOW_MIN_SIZE", ImGuiStyleVar_::ImGuiStyleVar_WindowMinSize)
        .value("WINDOW_TITLE_ALIGN", ImGuiStyleVar_::ImGuiStyleVar_WindowTitleAlign)
        .value("CHILD_ROUNDING", ImGuiStyleVar_::ImGuiStyleVar_ChildRounding)
        .value("CHILD_BORDER_SIZE", ImGuiStyleVar_::ImGuiStyleVar_ChildBorderSize)
        .value("POPUP_ROUNDING", ImGuiStyleVar_::ImGuiStyleVar_PopupRounding)
        .value("POPUP_BORDER_SIZE", ImGuiStyleVar_::ImGuiStyleVar_PopupBorderSize)
        .value("FRAME_PADDING", ImGuiStyleVar_::ImGuiStyleVar_FramePadding)
        .value("FRAME_ROUNDING", ImGuiStyleVar_::ImGuiStyleVar_FrameRounding)
        .value("FRAME_BORDER_SIZE", ImGuiStyleVar_::ImGuiStyleVar_FrameBorderSize)
        .value("ITEM_SPACING", ImGuiStyleVar_::ImGuiStyleVar_ItemSpacing)
        .value("ITEM_INNER_SPACING", ImGuiStyleVar_::ImGuiStyleVar_ItemInnerSpacing)
        .value("INDENT_SPACING", ImGuiStyleVar_::ImGuiStyleVar_IndentSpacing)
        .value("CELL_PADDING", ImGuiStyleVar_::ImGuiStyleVar_CellPadding)
        .value("SCROLLBAR_SIZE", ImGuiStyleVar_::ImGuiStyleVar_ScrollbarSize)
        .value("SCROLLBAR_ROUNDING", ImGuiStyleVar_::ImGuiStyleVar_ScrollbarRounding)
        .value("SCROLLBAR_PADDING", ImGuiStyleVar_::ImGuiStyleVar_ScrollbarPadding)
        .value("GRAB_MIN_SIZE", ImGuiStyleVar_::ImGuiStyleVar_GrabMinSize)
        .value("GRAB_ROUNDING", ImGuiStyleVar_::ImGuiStyleVar_GrabRounding)
        .value("IMAGE_BORDER_SIZE", ImGuiStyleVar_::ImGuiStyleVar_ImageBorderSize)
        .value("TAB_ROUNDING", ImGuiStyleVar_::ImGuiStyleVar_TabRounding)
        .value("TAB_BORDER_SIZE", ImGuiStyleVar_::ImGuiStyleVar_TabBorderSize)
        .value("TAB_MIN_WIDTH_BASE", ImGuiStyleVar_::ImGuiStyleVar_TabMinWidthBase)
        .value("TAB_MIN_WIDTH_SHRINK", ImGuiStyleVar_::ImGuiStyleVar_TabMinWidthShrink)
        .value("TAB_BAR_BORDER_SIZE", ImGuiStyleVar_::ImGuiStyleVar_TabBarBorderSize)
        .value("TAB_BAR_OVERLINE_SIZE", ImGuiStyleVar_::ImGuiStyleVar_TabBarOverlineSize)
        .value("TABLE_ANGLED_HEADERS_ANGLE", ImGuiStyleVar_::ImGuiStyleVar_TableAngledHeadersAngle)
        .value("TABLE_ANGLED_HEADERS_TEXT_ALIGN", ImGuiStyleVar_::ImGuiStyleVar_TableAngledHeadersTextAlign)
        .value("TREE_LINES_SIZE", ImGuiStyleVar_::ImGuiStyleVar_TreeLinesSize)
        .value("TREE_LINES_ROUNDING", ImGuiStyleVar_::ImGuiStyleVar_TreeLinesRounding)
        .value("BUTTON_TEXT_ALIGN", ImGuiStyleVar_::ImGuiStyleVar_ButtonTextAlign)
        .value("SELECTABLE_TEXT_ALIGN", ImGuiStyleVar_::ImGuiStyleVar_SelectableTextAlign)
        .value("SEPARATOR_TEXT_BORDER_SIZE", ImGuiStyleVar_::ImGuiStyleVar_SeparatorTextBorderSize)
        .value("SEPARATOR_TEXT_ALIGN", ImGuiStyleVar_::ImGuiStyleVar_SeparatorTextAlign)
        .value("SEPARATOR_TEXT_PADDING", ImGuiStyleVar_::ImGuiStyleVar_SeparatorTextPadding)
        .value("DOCKING_SEPARATOR_SIZE", ImGuiStyleVar_::ImGuiStyleVar_DockingSeparatorSize)
        .value("COUNT", ImGuiStyleVar_::ImGuiStyleVar_COUNT)
        .export_values()
    ;
    py::enum_<ImGuiButtonFlags_>(_imgui, "ButtonFlags", py::arithmetic())
        .value("NONE", ImGuiButtonFlags_::ImGuiButtonFlags_None)
        .value("MOUSE_BUTTON_LEFT", ImGuiButtonFlags_::ImGuiButtonFlags_MouseButtonLeft)
        .value("MOUSE_BUTTON_RIGHT", ImGuiButtonFlags_::ImGuiButtonFlags_MouseButtonRight)
        .value("MOUSE_BUTTON_MIDDLE", ImGuiButtonFlags_::ImGuiButtonFlags_MouseButtonMiddle)
        .value("MOUSE_BUTTON_MASK", ImGuiButtonFlags_::ImGuiButtonFlags_MouseButtonMask_)
        .value("ENABLE_NAV", ImGuiButtonFlags_::ImGuiButtonFlags_EnableNav)
        .export_values()
    ;
    py::enum_<ImGuiColorEditFlags_>(_imgui, "ColorEditFlags", py::arithmetic())
        .value("NONE", ImGuiColorEditFlags_::ImGuiColorEditFlags_None)
        .value("NO_ALPHA", ImGuiColorEditFlags_::ImGuiColorEditFlags_NoAlpha)
        .value("NO_PICKER", ImGuiColorEditFlags_::ImGuiColorEditFlags_NoPicker)
        .value("NO_OPTIONS", ImGuiColorEditFlags_::ImGuiColorEditFlags_NoOptions)
        .value("NO_SMALL_PREVIEW", ImGuiColorEditFlags_::ImGuiColorEditFlags_NoSmallPreview)
        .value("NO_INPUTS", ImGuiColorEditFlags_::ImGuiColorEditFlags_NoInputs)
        .value("NO_TOOLTIP", ImGuiColorEditFlags_::ImGuiColorEditFlags_NoTooltip)
        .value("NO_LABEL", ImGuiColorEditFlags_::ImGuiColorEditFlags_NoLabel)
        .value("NO_SIDE_PREVIEW", ImGuiColorEditFlags_::ImGuiColorEditFlags_NoSidePreview)
        .value("NO_DRAG_DROP", ImGuiColorEditFlags_::ImGuiColorEditFlags_NoDragDrop)
        .value("NO_BORDER", ImGuiColorEditFlags_::ImGuiColorEditFlags_NoBorder)
        .value("ALPHA_OPAQUE", ImGuiColorEditFlags_::ImGuiColorEditFlags_AlphaOpaque)
        .value("ALPHA_NO_BG", ImGuiColorEditFlags_::ImGuiColorEditFlags_AlphaNoBg)
        .value("ALPHA_PREVIEW_HALF", ImGuiColorEditFlags_::ImGuiColorEditFlags_AlphaPreviewHalf)
        .value("ALPHA_BAR", ImGuiColorEditFlags_::ImGuiColorEditFlags_AlphaBar)
        .value("HDR", ImGuiColorEditFlags_::ImGuiColorEditFlags_HDR)
        .value("DISPLAY_RGB", ImGuiColorEditFlags_::ImGuiColorEditFlags_DisplayRGB)
        .value("DISPLAY_HSV", ImGuiColorEditFlags_::ImGuiColorEditFlags_DisplayHSV)
        .value("DISPLAY_HEX", ImGuiColorEditFlags_::ImGuiColorEditFlags_DisplayHex)
        .value("UINT8", ImGuiColorEditFlags_::ImGuiColorEditFlags_Uint8)
        .value("FLOAT", ImGuiColorEditFlags_::ImGuiColorEditFlags_Float)
        .value("PICKER_HUE_BAR", ImGuiColorEditFlags_::ImGuiColorEditFlags_PickerHueBar)
        .value("PICKER_HUE_WHEEL", ImGuiColorEditFlags_::ImGuiColorEditFlags_PickerHueWheel)
        .value("INPUT_RGB", ImGuiColorEditFlags_::ImGuiColorEditFlags_InputRGB)
        .value("INPUT_HSV", ImGuiColorEditFlags_::ImGuiColorEditFlags_InputHSV)
        .value("DEFAULT_OPTIONS", ImGuiColorEditFlags_::ImGuiColorEditFlags_DefaultOptions_)
        .value("ALPHA_MASK", ImGuiColorEditFlags_::ImGuiColorEditFlags_AlphaMask_)
        .value("DISPLAY_MASK", ImGuiColorEditFlags_::ImGuiColorEditFlags_DisplayMask_)
        .value("DATA_TYPE_MASK", ImGuiColorEditFlags_::ImGuiColorEditFlags_DataTypeMask_)
        .value("PICKER_MASK", ImGuiColorEditFlags_::ImGuiColorEditFlags_PickerMask_)
        .value("INPUT_MASK", ImGuiColorEditFlags_::ImGuiColorEditFlags_InputMask_)
        .export_values()
    ;
    py::enum_<ImGuiSliderFlags_>(_imgui, "SliderFlags", py::arithmetic())
        .value("NONE", ImGuiSliderFlags_::ImGuiSliderFlags_None)
        .value("LOGARITHMIC", ImGuiSliderFlags_::ImGuiSliderFlags_Logarithmic)
        .value("NO_ROUND_TO_FORMAT", ImGuiSliderFlags_::ImGuiSliderFlags_NoRoundToFormat)
        .value("NO_INPUT", ImGuiSliderFlags_::ImGuiSliderFlags_NoInput)
        .value("WRAP_AROUND", ImGuiSliderFlags_::ImGuiSliderFlags_WrapAround)
        .value("CLAMP_ON_INPUT", ImGuiSliderFlags_::ImGuiSliderFlags_ClampOnInput)
        .value("CLAMP_ZERO_RANGE", ImGuiSliderFlags_::ImGuiSliderFlags_ClampZeroRange)
        .value("NO_SPEED_TWEAKS", ImGuiSliderFlags_::ImGuiSliderFlags_NoSpeedTweaks)
        .value("ALWAYS_CLAMP", ImGuiSliderFlags_::ImGuiSliderFlags_AlwaysClamp)
        .value("INVALID_MASK", ImGuiSliderFlags_::ImGuiSliderFlags_InvalidMask_)
        .export_values()
    ;
    py::enum_<ImGuiMouseButton_>(_imgui, "MouseButton", py::arithmetic())
        .value("LEFT", ImGuiMouseButton_::ImGuiMouseButton_Left)
        .value("RIGHT", ImGuiMouseButton_::ImGuiMouseButton_Right)
        .value("MIDDLE", ImGuiMouseButton_::ImGuiMouseButton_Middle)
        .value("COUNT", ImGuiMouseButton_::ImGuiMouseButton_COUNT)
        .export_values()
    ;
    py::enum_<ImGuiMouseCursor_>(_imgui, "MouseCursor", py::arithmetic())
        .value("NONE", ImGuiMouseCursor_::ImGuiMouseCursor_None)
        .value("ARROW", ImGuiMouseCursor_::ImGuiMouseCursor_Arrow)
        .value("TEXT_INPUT", ImGuiMouseCursor_::ImGuiMouseCursor_TextInput)
        .value("RESIZE_ALL", ImGuiMouseCursor_::ImGuiMouseCursor_ResizeAll)
        .value("RESIZE_NS", ImGuiMouseCursor_::ImGuiMouseCursor_ResizeNS)
        .value("RESIZE_EW", ImGuiMouseCursor_::ImGuiMouseCursor_ResizeEW)
        .value("RESIZE_NESW", ImGuiMouseCursor_::ImGuiMouseCursor_ResizeNESW)
        .value("RESIZE_NWSE", ImGuiMouseCursor_::ImGuiMouseCursor_ResizeNWSE)
        .value("HAND", ImGuiMouseCursor_::ImGuiMouseCursor_Hand)
        .value("WAIT", ImGuiMouseCursor_::ImGuiMouseCursor_Wait)
        .value("PROGRESS", ImGuiMouseCursor_::ImGuiMouseCursor_Progress)
        .value("NOT_ALLOWED", ImGuiMouseCursor_::ImGuiMouseCursor_NotAllowed)
        .value("COUNT", ImGuiMouseCursor_::ImGuiMouseCursor_COUNT)
        .export_values()
    ;
    py::enum_<ImGuiMouseSource>(_imgui, "MouseSource", py::arithmetic())
        .value("MOUSE", ImGuiMouseSource::ImGuiMouseSource_Mouse)
        .value("TOUCH_SCREEN", ImGuiMouseSource::ImGuiMouseSource_TouchScreen)
        .value("PEN", ImGuiMouseSource::ImGuiMouseSource_Pen)
        .value("COUNT", ImGuiMouseSource::ImGuiMouseSource_COUNT)
        .export_values()
    ;
    py::enum_<ImGuiCond_>(_imgui, "Cond", py::arithmetic())
        .value("NONE", ImGuiCond_::ImGuiCond_None)
        .value("ALWAYS", ImGuiCond_::ImGuiCond_Always)
        .value("ONCE", ImGuiCond_::ImGuiCond_Once)
        .value("FIRST_USE_EVER", ImGuiCond_::ImGuiCond_FirstUseEver)
        .value("APPEARING", ImGuiCond_::ImGuiCond_Appearing)
        .export_values()
    ;
    py::enum_<ImGuiTableFlags_>(_imgui, "TableFlags", py::arithmetic())
        .value("NONE", ImGuiTableFlags_::ImGuiTableFlags_None)
        .value("RESIZABLE", ImGuiTableFlags_::ImGuiTableFlags_Resizable)
        .value("REORDERABLE", ImGuiTableFlags_::ImGuiTableFlags_Reorderable)
        .value("HIDEABLE", ImGuiTableFlags_::ImGuiTableFlags_Hideable)
        .value("SORTABLE", ImGuiTableFlags_::ImGuiTableFlags_Sortable)
        .value("NO_SAVED_SETTINGS", ImGuiTableFlags_::ImGuiTableFlags_NoSavedSettings)
        .value("CONTEXT_MENU_IN_BODY", ImGuiTableFlags_::ImGuiTableFlags_ContextMenuInBody)
        .value("ROW_BG", ImGuiTableFlags_::ImGuiTableFlags_RowBg)
        .value("BORDERS_INNER_H", ImGuiTableFlags_::ImGuiTableFlags_BordersInnerH)
        .value("BORDERS_OUTER_H", ImGuiTableFlags_::ImGuiTableFlags_BordersOuterH)
        .value("BORDERS_INNER_V", ImGuiTableFlags_::ImGuiTableFlags_BordersInnerV)
        .value("BORDERS_OUTER_V", ImGuiTableFlags_::ImGuiTableFlags_BordersOuterV)
        .value("BORDERS_H", ImGuiTableFlags_::ImGuiTableFlags_BordersH)
        .value("BORDERS_V", ImGuiTableFlags_::ImGuiTableFlags_BordersV)
        .value("BORDERS_INNER", ImGuiTableFlags_::ImGuiTableFlags_BordersInner)
        .value("BORDERS_OUTER", ImGuiTableFlags_::ImGuiTableFlags_BordersOuter)
        .value("BORDERS", ImGuiTableFlags_::ImGuiTableFlags_Borders)
        .value("NO_BORDERS_IN_BODY", ImGuiTableFlags_::ImGuiTableFlags_NoBordersInBody)
        .value("NO_BORDERS_IN_BODY_UNTIL_RESIZE", ImGuiTableFlags_::ImGuiTableFlags_NoBordersInBodyUntilResize)
        .value("SIZING_FIXED_FIT", ImGuiTableFlags_::ImGuiTableFlags_SizingFixedFit)
        .value("SIZING_FIXED_SAME", ImGuiTableFlags_::ImGuiTableFlags_SizingFixedSame)
        .value("SIZING_STRETCH_PROP", ImGuiTableFlags_::ImGuiTableFlags_SizingStretchProp)
        .value("SIZING_STRETCH_SAME", ImGuiTableFlags_::ImGuiTableFlags_SizingStretchSame)
        .value("NO_HOST_EXTEND_X", ImGuiTableFlags_::ImGuiTableFlags_NoHostExtendX)
        .value("NO_HOST_EXTEND_Y", ImGuiTableFlags_::ImGuiTableFlags_NoHostExtendY)
        .value("NO_KEEP_COLUMNS_VISIBLE", ImGuiTableFlags_::ImGuiTableFlags_NoKeepColumnsVisible)
        .value("PRECISE_WIDTHS", ImGuiTableFlags_::ImGuiTableFlags_PreciseWidths)
        .value("NO_CLIP", ImGuiTableFlags_::ImGuiTableFlags_NoClip)
        .value("PAD_OUTER_X", ImGuiTableFlags_::ImGuiTableFlags_PadOuterX)
        .value("NO_PAD_OUTER_X", ImGuiTableFlags_::ImGuiTableFlags_NoPadOuterX)
        .value("NO_PAD_INNER_X", ImGuiTableFlags_::ImGuiTableFlags_NoPadInnerX)
        .value("SCROLL_X", ImGuiTableFlags_::ImGuiTableFlags_ScrollX)
        .value("SCROLL_Y", ImGuiTableFlags_::ImGuiTableFlags_ScrollY)
        .value("SORT_MULTI", ImGuiTableFlags_::ImGuiTableFlags_SortMulti)
        .value("SORT_TRISTATE", ImGuiTableFlags_::ImGuiTableFlags_SortTristate)
        .value("HIGHLIGHT_HOVERED_COLUMN", ImGuiTableFlags_::ImGuiTableFlags_HighlightHoveredColumn)
        .value("SIZING_MASK", ImGuiTableFlags_::ImGuiTableFlags_SizingMask_)
        .export_values()
    ;
    py::enum_<ImGuiTableColumnFlags_>(_imgui, "TableColumnFlags", py::arithmetic())
        .value("NONE", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_None)
        .value("DISABLED", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_Disabled)
        .value("DEFAULT_HIDE", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_DefaultHide)
        .value("DEFAULT_SORT", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_DefaultSort)
        .value("WIDTH_STRETCH", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_WidthStretch)
        .value("WIDTH_FIXED", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_WidthFixed)
        .value("NO_RESIZE", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_NoResize)
        .value("NO_REORDER", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_NoReorder)
        .value("NO_HIDE", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_NoHide)
        .value("NO_CLIP", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_NoClip)
        .value("NO_SORT", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_NoSort)
        .value("NO_SORT_ASCENDING", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_NoSortAscending)
        .value("NO_SORT_DESCENDING", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_NoSortDescending)
        .value("NO_HEADER_LABEL", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_NoHeaderLabel)
        .value("NO_HEADER_WIDTH", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_NoHeaderWidth)
        .value("PREFER_SORT_ASCENDING", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_PreferSortAscending)
        .value("PREFER_SORT_DESCENDING", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_PreferSortDescending)
        .value("INDENT_ENABLE", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_IndentEnable)
        .value("INDENT_DISABLE", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_IndentDisable)
        .value("ANGLED_HEADER", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_AngledHeader)
        .value("IS_ENABLED", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_IsEnabled)
        .value("IS_VISIBLE", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_IsVisible)
        .value("IS_SORTED", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_IsSorted)
        .value("IS_HOVERED", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_IsHovered)
        .value("WIDTH_MASK", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_WidthMask_)
        .value("INDENT_MASK", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_IndentMask_)
        .value("STATUS_MASK", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_StatusMask_)
        .value("NO_DIRECT_RESIZE", ImGuiTableColumnFlags_::ImGuiTableColumnFlags_NoDirectResize_)
        .export_values()
    ;
    py::enum_<ImGuiTableRowFlags_>(_imgui, "TableRowFlags", py::arithmetic())
        .value("NONE", ImGuiTableRowFlags_::ImGuiTableRowFlags_None)
        .value("HEADERS", ImGuiTableRowFlags_::ImGuiTableRowFlags_Headers)
        .export_values()
    ;
    py::enum_<ImGuiTableBgTarget_>(_imgui, "TableBgTarget", py::arithmetic())
        .value("NONE", ImGuiTableBgTarget_::ImGuiTableBgTarget_None)
        .value("ROW_BG0", ImGuiTableBgTarget_::ImGuiTableBgTarget_RowBg0)
        .value("ROW_BG1", ImGuiTableBgTarget_::ImGuiTableBgTarget_RowBg1)
        .value("CELL_BG", ImGuiTableBgTarget_::ImGuiTableBgTarget_CellBg)
        .export_values()
    ;
    py::class_<ImGuiTableSortSpecs> _TableSortSpecs(_imgui, "TableSortSpecs");
    registry.on(_imgui, "TableSortSpecs", _TableSortSpecs);
        _TableSortSpecs
        .def_readwrite("specs", &ImGuiTableSortSpecs::Specs)
        .def_readwrite("specs_count", &ImGuiTableSortSpecs::SpecsCount)
        .def_readwrite("specs_dirty", &ImGuiTableSortSpecs::SpecsDirty)
        .def(py::init<>())
    ;

    py::class_<ImGuiTableColumnSortSpecs> _TableColumnSortSpecs(_imgui, "TableColumnSortSpecs");
    registry.on(_imgui, "TableColumnSortSpecs", _TableColumnSortSpecs);
        _TableColumnSortSpecs
        .def_readwrite("column_user_id", &ImGuiTableColumnSortSpecs::ColumnUserID)
        .def_readwrite("column_index", &ImGuiTableColumnSortSpecs::ColumnIndex)
        .def_readwrite("sort_order", &ImGuiTableColumnSortSpecs::SortOrder)
        .def(py::init<>())
    ;

    py::class_<ImNewWrapper> _NewWrapper(_imgui, "NewWrapper");
    registry.on(_imgui, "NewWrapper", _NewWrapper);
    py::class_<ImGuiStyle> _Style(_imgui, "Style");
    registry.on(_imgui, "Style", _Style);
        _Style
        .def_readwrite("font_size_base", &ImGuiStyle::FontSizeBase)
        .def_readwrite("font_scale_main", &ImGuiStyle::FontScaleMain)
        .def_readwrite("font_scale_dpi", &ImGuiStyle::FontScaleDpi)
        .def_readwrite("alpha", &ImGuiStyle::Alpha)
        .def_readwrite("disabled_alpha", &ImGuiStyle::DisabledAlpha)
        .def_readwrite("window_padding", &ImGuiStyle::WindowPadding)
        .def_readwrite("window_rounding", &ImGuiStyle::WindowRounding)
        .def_readwrite("window_border_size", &ImGuiStyle::WindowBorderSize)
        .def_readwrite("window_border_hover_padding", &ImGuiStyle::WindowBorderHoverPadding)
        .def_readwrite("window_min_size", &ImGuiStyle::WindowMinSize)
        .def_readwrite("window_title_align", &ImGuiStyle::WindowTitleAlign)
        .def_readwrite("window_menu_button_position", &ImGuiStyle::WindowMenuButtonPosition)
        .def_readwrite("child_rounding", &ImGuiStyle::ChildRounding)
        .def_readwrite("child_border_size", &ImGuiStyle::ChildBorderSize)
        .def_readwrite("popup_rounding", &ImGuiStyle::PopupRounding)
        .def_readwrite("popup_border_size", &ImGuiStyle::PopupBorderSize)
        .def_readwrite("frame_padding", &ImGuiStyle::FramePadding)
        .def_readwrite("frame_rounding", &ImGuiStyle::FrameRounding)
        .def_readwrite("frame_border_size", &ImGuiStyle::FrameBorderSize)
        .def_readwrite("item_spacing", &ImGuiStyle::ItemSpacing)
        .def_readwrite("item_inner_spacing", &ImGuiStyle::ItemInnerSpacing)
        .def_readwrite("cell_padding", &ImGuiStyle::CellPadding)
        .def_readwrite("touch_extra_padding", &ImGuiStyle::TouchExtraPadding)
        .def_readwrite("indent_spacing", &ImGuiStyle::IndentSpacing)
        .def_readwrite("columns_min_spacing", &ImGuiStyle::ColumnsMinSpacing)
        .def_readwrite("scrollbar_size", &ImGuiStyle::ScrollbarSize)
        .def_readwrite("scrollbar_rounding", &ImGuiStyle::ScrollbarRounding)
        .def_readwrite("scrollbar_padding", &ImGuiStyle::ScrollbarPadding)
        .def_readwrite("grab_min_size", &ImGuiStyle::GrabMinSize)
        .def_readwrite("grab_rounding", &ImGuiStyle::GrabRounding)
        .def_readwrite("log_slider_deadzone", &ImGuiStyle::LogSliderDeadzone)
        .def_readwrite("image_border_size", &ImGuiStyle::ImageBorderSize)
        .def_readwrite("tab_rounding", &ImGuiStyle::TabRounding)
        .def_readwrite("tab_border_size", &ImGuiStyle::TabBorderSize)
        .def_readwrite("tab_min_width_base", &ImGuiStyle::TabMinWidthBase)
        .def_readwrite("tab_min_width_shrink", &ImGuiStyle::TabMinWidthShrink)
        .def_readwrite("tab_close_button_min_width_selected", &ImGuiStyle::TabCloseButtonMinWidthSelected)
        .def_readwrite("tab_close_button_min_width_unselected", &ImGuiStyle::TabCloseButtonMinWidthUnselected)
        .def_readwrite("tab_bar_border_size", &ImGuiStyle::TabBarBorderSize)
        .def_readwrite("tab_bar_overline_size", &ImGuiStyle::TabBarOverlineSize)
        .def_readwrite("table_angled_headers_angle", &ImGuiStyle::TableAngledHeadersAngle)
        .def_readwrite("table_angled_headers_text_align", &ImGuiStyle::TableAngledHeadersTextAlign)
        .def_readwrite("tree_lines_flags", &ImGuiStyle::TreeLinesFlags)
        .def_readwrite("tree_lines_size", &ImGuiStyle::TreeLinesSize)
        .def_readwrite("tree_lines_rounding", &ImGuiStyle::TreeLinesRounding)
        .def_readwrite("color_button_position", &ImGuiStyle::ColorButtonPosition)
        .def_readwrite("button_text_align", &ImGuiStyle::ButtonTextAlign)
        .def_readwrite("selectable_text_align", &ImGuiStyle::SelectableTextAlign)
        .def_readwrite("separator_text_border_size", &ImGuiStyle::SeparatorTextBorderSize)
        .def_readwrite("separator_text_align", &ImGuiStyle::SeparatorTextAlign)
        .def_readwrite("separator_text_padding", &ImGuiStyle::SeparatorTextPadding)
        .def_readwrite("display_window_padding", &ImGuiStyle::DisplayWindowPadding)
        .def_readwrite("display_safe_area_padding", &ImGuiStyle::DisplaySafeAreaPadding)
        .def_readwrite("docking_separator_size", &ImGuiStyle::DockingSeparatorSize)
        .def_readwrite("mouse_cursor_scale", &ImGuiStyle::MouseCursorScale)
        .def_readwrite("anti_aliased_lines", &ImGuiStyle::AntiAliasedLines)
        .def_readwrite("anti_aliased_lines_use_tex", &ImGuiStyle::AntiAliasedLinesUseTex)
        .def_readwrite("anti_aliased_fill", &ImGuiStyle::AntiAliasedFill)
        .def_readwrite("curve_tessellation_tol", &ImGuiStyle::CurveTessellationTol)
        .def_readwrite("circle_tessellation_max_error", &ImGuiStyle::CircleTessellationMaxError)
        .def_readwrite("hover_stationary_delay", &ImGuiStyle::HoverStationaryDelay)
        .def_readwrite("hover_delay_short", &ImGuiStyle::HoverDelayShort)
        .def_readwrite("hover_delay_normal", &ImGuiStyle::HoverDelayNormal)
        .def_readwrite("hover_flags_for_tooltip_mouse", &ImGuiStyle::HoverFlagsForTooltipMouse)
        .def_readwrite("hover_flags_for_tooltip_nav", &ImGuiStyle::HoverFlagsForTooltipNav)
        .def(py::init<>())
        .def("scale_all_sizes", &ImGuiStyle::ScaleAllSizes
            , py::arg("scale_factor")
            , py::return_value_policy::automatic_reference)
    ;

    py::class_<ImGuiKeyData> _KeyData(_imgui, "KeyData");
    registry.on(_imgui, "KeyData", _KeyData);
        _KeyData
        .def_readwrite("down", &ImGuiKeyData::Down)
        .def_readwrite("down_duration", &ImGuiKeyData::DownDuration)
        .def_readwrite("down_duration_prev", &ImGuiKeyData::DownDurationPrev)
        .def_readwrite("analog_value", &ImGuiKeyData::AnalogValue)
    ;

    py::class_<ImGuiIO> _IO(_imgui, "IO");
    registry.on(_imgui, "IO", _IO);
        _IO
        .def_readwrite("config_flags", &ImGuiIO::ConfigFlags)
        .def_readwrite("backend_flags", &ImGuiIO::BackendFlags)
        .def_readwrite("display_size", &ImGuiIO::DisplaySize)
        .def_readwrite("display_framebuffer_scale", &ImGuiIO::DisplayFramebufferScale)
        .def_readwrite("delta_time", &ImGuiIO::DeltaTime)
        .def_readwrite("ini_saving_rate", &ImGuiIO::IniSavingRate)
        .def_property("ini_filename",
            [](const ImGuiIO& self){ return self.IniFilename; },
            [](ImGuiIO& self, const char* source){ self.IniFilename = strdup(source); }
        )
        .def_property("log_filename",
            [](const ImGuiIO& self){ return self.LogFilename; },
            [](ImGuiIO& self, const char* source){ self.LogFilename = strdup(source); }
        )
        .def_readwrite("user_data", &ImGuiIO::UserData)
        .def_readwrite("fonts", &ImGuiIO::Fonts)
        .def_readwrite("font_default", &ImGuiIO::FontDefault)
        .def_readwrite("font_allow_user_scaling", &ImGuiIO::FontAllowUserScaling)
        .def_readwrite("config_nav_swap_gamepad_buttons", &ImGuiIO::ConfigNavSwapGamepadButtons)
        .def_readwrite("config_nav_move_set_mouse_pos", &ImGuiIO::ConfigNavMoveSetMousePos)
        .def_readwrite("config_nav_capture_keyboard", &ImGuiIO::ConfigNavCaptureKeyboard)
        .def_readwrite("config_nav_escape_clear_focus_item", &ImGuiIO::ConfigNavEscapeClearFocusItem)
        .def_readwrite("config_nav_escape_clear_focus_window", &ImGuiIO::ConfigNavEscapeClearFocusWindow)
        .def_readwrite("config_nav_cursor_visible_auto", &ImGuiIO::ConfigNavCursorVisibleAuto)
        .def_readwrite("config_nav_cursor_visible_always", &ImGuiIO::ConfigNavCursorVisibleAlways)
        .def_readwrite("config_docking_no_split", &ImGuiIO::ConfigDockingNoSplit)
        .def_readwrite("config_docking_with_shift", &ImGuiIO::ConfigDockingWithShift)
        .def_readwrite("config_docking_always_tab_bar", &ImGuiIO::ConfigDockingAlwaysTabBar)
        .def_readwrite("config_docking_transparent_payload", &ImGuiIO::ConfigDockingTransparentPayload)
        .def_readwrite("config_viewports_no_auto_merge", &ImGuiIO::ConfigViewportsNoAutoMerge)
        .def_readwrite("config_viewports_no_task_bar_icon", &ImGuiIO::ConfigViewportsNoTaskBarIcon)
        .def_readwrite("config_viewports_no_decoration", &ImGuiIO::ConfigViewportsNoDecoration)
        .def_readwrite("config_viewports_no_default_parent", &ImGuiIO::ConfigViewportsNoDefaultParent)
        .def_readwrite("config_viewport_platform_focus_sets_im_gui_focus", &ImGuiIO::ConfigViewportPlatformFocusSetsImGuiFocus)
        .def_readwrite("config_dpi_scale_fonts", &ImGuiIO::ConfigDpiScaleFonts)
        .def_readwrite("config_dpi_scale_viewports", &ImGuiIO::ConfigDpiScaleViewports)
        .def_readwrite("mouse_draw_cursor", &ImGuiIO::MouseDrawCursor)
        .def_readwrite("config_mac_osx_behaviors", &ImGuiIO::ConfigMacOSXBehaviors)
        .def_readwrite("config_input_trickle_event_queue", &ImGuiIO::ConfigInputTrickleEventQueue)
        .def_readwrite("config_input_text_cursor_blink", &ImGuiIO::ConfigInputTextCursorBlink)
        .def_readwrite("config_input_text_enter_keep_active", &ImGuiIO::ConfigInputTextEnterKeepActive)
        .def_readwrite("config_drag_click_to_input_text", &ImGuiIO::ConfigDragClickToInputText)
        .def_readwrite("config_windows_resize_from_edges", &ImGuiIO::ConfigWindowsResizeFromEdges)
        .def_readwrite("config_windows_move_from_title_bar_only", &ImGuiIO::ConfigWindowsMoveFromTitleBarOnly)
        .def_readwrite("config_windows_copy_contents_with_ctrl_c", &ImGuiIO::ConfigWindowsCopyContentsWithCtrlC)
        .def_readwrite("config_scrollbar_scroll_by_page", &ImGuiIO::ConfigScrollbarScrollByPage)
        .def_readwrite("config_memory_compact_timer", &ImGuiIO::ConfigMemoryCompactTimer)
        .def_readwrite("mouse_double_click_time", &ImGuiIO::MouseDoubleClickTime)
        .def_readwrite("mouse_double_click_max_dist", &ImGuiIO::MouseDoubleClickMaxDist)
        .def_readwrite("mouse_drag_threshold", &ImGuiIO::MouseDragThreshold)
        .def_readwrite("key_repeat_delay", &ImGuiIO::KeyRepeatDelay)
        .def_readwrite("key_repeat_rate", &ImGuiIO::KeyRepeatRate)
        .def_readwrite("config_error_recovery", &ImGuiIO::ConfigErrorRecovery)
        .def_readwrite("config_error_recovery_enable_assert", &ImGuiIO::ConfigErrorRecoveryEnableAssert)
        .def_readwrite("config_error_recovery_enable_debug_log", &ImGuiIO::ConfigErrorRecoveryEnableDebugLog)
        .def_readwrite("config_error_recovery_enable_tooltip", &ImGuiIO::ConfigErrorRecoveryEnableTooltip)
        .def_readwrite("config_debug_is_debugger_present", &ImGuiIO::ConfigDebugIsDebuggerPresent)
        .def_readwrite("config_debug_highlight_id_conflicts", &ImGuiIO::ConfigDebugHighlightIdConflicts)
        .def_readwrite("config_debug_highlight_id_conflicts_show_item_picker", &ImGuiIO::ConfigDebugHighlightIdConflictsShowItemPicker)
        .def_readwrite("config_debug_begin_return_value_once", &ImGuiIO::ConfigDebugBeginReturnValueOnce)
        .def_readwrite("config_debug_begin_return_value_loop", &ImGuiIO::ConfigDebugBeginReturnValueLoop)
        .def_readwrite("config_debug_ignore_focus_loss", &ImGuiIO::ConfigDebugIgnoreFocusLoss)
        .def_readwrite("config_debug_ini_settings", &ImGuiIO::ConfigDebugIniSettings)
        .def_property("backend_platform_name",
            [](const ImGuiIO& self){ return self.BackendPlatformName; },
            [](ImGuiIO& self, const char* source){ self.BackendPlatformName = strdup(source); }
        )
        .def_property("backend_renderer_name",
            [](const ImGuiIO& self){ return self.BackendRendererName; },
            [](ImGuiIO& self, const char* source){ self.BackendRendererName = strdup(source); }
        )
        .def_readwrite("backend_platform_user_data", &ImGuiIO::BackendPlatformUserData)
        .def_readwrite("backend_renderer_user_data", &ImGuiIO::BackendRendererUserData)
        .def_readwrite("backend_language_user_data", &ImGuiIO::BackendLanguageUserData)
        .def("add_key_event", &ImGuiIO::AddKeyEvent
            , py::arg("key")
            , py::arg("down")
            , py::return_value_policy::automatic_reference)
        .def("add_key_analog_event", &ImGuiIO::AddKeyAnalogEvent
            , py::arg("key")
            , py::arg("down")
            , py::arg("v")
            , py::return_value_policy::automatic_reference)
        .def("add_mouse_pos_event", &ImGuiIO::AddMousePosEvent
            , py::arg("x")
            , py::arg("y")
            , py::return_value_policy::automatic_reference)
        .def("add_mouse_button_event", &ImGuiIO::AddMouseButtonEvent
            , py::arg("button")
            , py::arg("down")
            , py::return_value_policy::automatic_reference)
        .def("add_mouse_wheel_event", &ImGuiIO::AddMouseWheelEvent
            , py::arg("wheel_x")
            , py::arg("wheel_y")
            , py::return_value_policy::automatic_reference)
        .def("add_mouse_source_event", &ImGuiIO::AddMouseSourceEvent
            , py::arg("source")
            , py::return_value_policy::automatic_reference)
        .def("add_mouse_viewport_event", &ImGuiIO::AddMouseViewportEvent
            , py::arg("id")
            , py::return_value_policy::automatic_reference)
        .def("add_focus_event", &ImGuiIO::AddFocusEvent
            , py::arg("focused")
            , py::return_value_policy::automatic_reference)
        .def("add_input_character", &ImGuiIO::AddInputCharacter
            , py::arg("c")
            , py::return_value_policy::automatic_reference)
        .def("add_input_character_utf16", &ImGuiIO::AddInputCharacterUTF16
            , py::arg("c")
            , py::return_value_policy::automatic_reference)
        .def("add_input_characters_utf8", &ImGuiIO::AddInputCharactersUTF8
            , py::arg("str")
            , py::return_value_policy::automatic_reference)
        .def("set_key_event_native_data", &ImGuiIO::SetKeyEventNativeData
            , py::arg("key")
            , py::arg("native_keycode")
            , py::arg("native_scancode")
            , py::arg("native_legacy_index") = -1
            , py::return_value_policy::automatic_reference)
        .def("set_app_accepting_events", &ImGuiIO::SetAppAcceptingEvents
            , py::arg("accepting_events")
            , py::return_value_policy::automatic_reference)
        .def("clear_events_queue", &ImGuiIO::ClearEventsQueue
            , py::return_value_policy::automatic_reference)
        .def("clear_input_keys", &ImGuiIO::ClearInputKeys
            , py::return_value_policy::automatic_reference)
        .def("clear_input_mouse", &ImGuiIO::ClearInputMouse
            , py::return_value_policy::automatic_reference)
        .def_readwrite("want_capture_mouse", &ImGuiIO::WantCaptureMouse)
        .def_readwrite("want_capture_keyboard", &ImGuiIO::WantCaptureKeyboard)
        .def_readwrite("want_text_input", &ImGuiIO::WantTextInput)
        .def_readwrite("want_set_mouse_pos", &ImGuiIO::WantSetMousePos)
        .def_readwrite("want_save_ini_settings", &ImGuiIO::WantSaveIniSettings)
        .def_readwrite("nav_active", &ImGuiIO::NavActive)
        .def_readwrite("nav_visible", &ImGuiIO::NavVisible)
        .def_readwrite("framerate", &ImGuiIO::Framerate)
        .def_readwrite("metrics_render_vertices", &ImGuiIO::MetricsRenderVertices)
        .def_readwrite("metrics_render_indices", &ImGuiIO::MetricsRenderIndices)
        .def_readwrite("metrics_render_windows", &ImGuiIO::MetricsRenderWindows)
        .def_readwrite("metrics_active_windows", &ImGuiIO::MetricsActiveWindows)
        .def_readwrite("mouse_delta", &ImGuiIO::MouseDelta)
        .def_readwrite("mouse_pos", &ImGuiIO::MousePos)
        .def_readonly("mouse_down", &ImGuiIO::MouseDown)
        .def_readwrite("mouse_wheel", &ImGuiIO::MouseWheel)
        .def_readwrite("mouse_wheel_h", &ImGuiIO::MouseWheelH)
        .def_readwrite("mouse_source", &ImGuiIO::MouseSource)
        .def_readwrite("mouse_hovered_viewport", &ImGuiIO::MouseHoveredViewport)
        .def_readwrite("key_ctrl", &ImGuiIO::KeyCtrl)
        .def_readwrite("key_shift", &ImGuiIO::KeyShift)
        .def_readwrite("key_alt", &ImGuiIO::KeyAlt)
        .def_readwrite("key_super", &ImGuiIO::KeySuper)
        .def_readwrite("key_mods", &ImGuiIO::KeyMods)
        .def_readonly("keys_data", &ImGuiIO::KeysData)
        .def_readwrite("want_capture_mouse_unless_popup_close", &ImGuiIO::WantCaptureMouseUnlessPopupClose)
        .def_readwrite("mouse_pos_prev", &ImGuiIO::MousePosPrev)
        .def_readonly("mouse_clicked_pos", &ImGuiIO::MouseClickedPos)
        .def_readonly("mouse_clicked_time", &ImGuiIO::MouseClickedTime)
        .def_readonly("mouse_clicked", &ImGuiIO::MouseClicked)
        .def_readonly("mouse_double_clicked", &ImGuiIO::MouseDoubleClicked)
        .def_readonly("mouse_clicked_count", &ImGuiIO::MouseClickedCount)
        .def_readonly("mouse_clicked_last_count", &ImGuiIO::MouseClickedLastCount)
        .def_readonly("mouse_released", &ImGuiIO::MouseReleased)
        .def_readonly("mouse_released_time", &ImGuiIO::MouseReleasedTime)
        .def_readonly("mouse_down_owned", &ImGuiIO::MouseDownOwned)
        .def_readonly("mouse_down_owned_unless_popup_close", &ImGuiIO::MouseDownOwnedUnlessPopupClose)
        .def_readwrite("mouse_wheel_request_axis_swap", &ImGuiIO::MouseWheelRequestAxisSwap)
        .def_readwrite("mouse_ctrl_left_as_right_click", &ImGuiIO::MouseCtrlLeftAsRightClick)
        .def_readonly("mouse_down_duration", &ImGuiIO::MouseDownDuration)
        .def_readonly("mouse_down_duration_prev", &ImGuiIO::MouseDownDurationPrev)
        .def_readonly("mouse_drag_max_distance_abs", &ImGuiIO::MouseDragMaxDistanceAbs)
        .def_readonly("mouse_drag_max_distance_sqr", &ImGuiIO::MouseDragMaxDistanceSqr)
        .def_readwrite("pen_pressure", &ImGuiIO::PenPressure)
        .def_readwrite("app_focus_lost", &ImGuiIO::AppFocusLost)
        .def_readwrite("app_accepting_events", &ImGuiIO::AppAcceptingEvents)
        .def_readwrite("input_queue_surrogate", &ImGuiIO::InputQueueSurrogate)
        .def_readwrite("input_queue_characters", &ImGuiIO::InputQueueCharacters)
        .def(py::init<>())
    ;

    py::class_<ImGuiInputTextCallbackData> _InputTextCallbackData(_imgui, "InputTextCallbackData");
    registry.on(_imgui, "InputTextCallbackData", _InputTextCallbackData);
        _InputTextCallbackData
        .def_readwrite("event_flag", &ImGuiInputTextCallbackData::EventFlag)
        .def_readwrite("flags", &ImGuiInputTextCallbackData::Flags)
        .def_readwrite("user_data", &ImGuiInputTextCallbackData::UserData)
        .def_readwrite("event_char", &ImGuiInputTextCallbackData::EventChar)
        .def_readwrite("event_key", &ImGuiInputTextCallbackData::EventKey)
        .def_property("buf",
            [](const ImGuiInputTextCallbackData& self){ return self.Buf; },
            [](ImGuiInputTextCallbackData& self, const char* source){ self.Buf = strdup(source); }
        )
        .def_readwrite("buf_text_len", &ImGuiInputTextCallbackData::BufTextLen)
        .def_readwrite("buf_size", &ImGuiInputTextCallbackData::BufSize)
        .def_readwrite("buf_dirty", &ImGuiInputTextCallbackData::BufDirty)
        .def_readwrite("cursor_pos", &ImGuiInputTextCallbackData::CursorPos)
        .def_readwrite("selection_start", &ImGuiInputTextCallbackData::SelectionStart)
        .def_readwrite("selection_end", &ImGuiInputTextCallbackData::SelectionEnd)
        .def(py::init<>())
        .def("delete_chars", &ImGuiInputTextCallbackData::DeleteChars
            , py::arg("pos")
            , py::arg("bytes_count")
            , py::return_value_policy::automatic_reference)
        .def("insert_chars", &ImGuiInputTextCallbackData::InsertChars
            , py::arg("pos")
            , py::arg("text")
            , py::arg("text_end") = nullptr
            , py::return_value_policy::automatic_reference)
        .def("select_all", &ImGuiInputTextCallbackData::SelectAll
            , py::return_value_policy::automatic_reference)
        .def("clear_selection", &ImGuiInputTextCallbackData::ClearSelection
            , py::return_value_policy::automatic_reference)
        .def("has_selection", &ImGuiInputTextCallbackData::HasSelection
            , py::return_value_policy::automatic_reference)
    ;

    py::class_<ImGuiSizeCallbackData> _SizeCallbackData(_imgui, "SizeCallbackData");
    registry.on(_imgui, "SizeCallbackData", _SizeCallbackData);
        _SizeCallbackData
        .def_readwrite("user_data", &ImGuiSizeCallbackData::UserData)
        .def_readwrite("pos", &ImGuiSizeCallbackData::Pos)
        .def_readwrite("current_size", &ImGuiSizeCallbackData::CurrentSize)
        .def_readwrite("desired_size", &ImGuiSizeCallbackData::DesiredSize)
    ;

    py::class_<ImGuiWindowClass> _WindowClass(_imgui, "WindowClass");
    registry.on(_imgui, "WindowClass", _WindowClass);
        _WindowClass
        .def_readwrite("class_id", &ImGuiWindowClass::ClassId)
        .def_readwrite("parent_viewport_id", &ImGuiWindowClass::ParentViewportId)
        .def_readwrite("focus_route_parent_window_id", &ImGuiWindowClass::FocusRouteParentWindowId)
        .def_readwrite("viewport_flags_override_set", &ImGuiWindowClass::ViewportFlagsOverrideSet)
        .def_readwrite("viewport_flags_override_clear", &ImGuiWindowClass::ViewportFlagsOverrideClear)
        .def_readwrite("tab_item_flags_override_set", &ImGuiWindowClass::TabItemFlagsOverrideSet)
        .def_readwrite("dock_node_flags_override_set", &ImGuiWindowClass::DockNodeFlagsOverrideSet)
        .def_readwrite("docking_always_tab_bar", &ImGuiWindowClass::DockingAlwaysTabBar)
        .def_readwrite("docking_allow_unclassed", &ImGuiWindowClass::DockingAllowUnclassed)
        .def(py::init<>())
    ;

    py::class_<ImGuiPayload> _Payload(_imgui, "Payload");
    registry.on(_imgui, "Payload", _Payload);
        _Payload
        .def_readwrite("data", &ImGuiPayload::Data)
        .def_readwrite("data_size", &ImGuiPayload::DataSize)
        .def_readwrite("source_id", &ImGuiPayload::SourceId)
        .def_readwrite("source_parent_id", &ImGuiPayload::SourceParentId)
        .def_readwrite("data_frame_count", &ImGuiPayload::DataFrameCount)
        .def_readonly("data_type", &ImGuiPayload::DataType)
        .def_readwrite("preview", &ImGuiPayload::Preview)
        .def_readwrite("delivery", &ImGuiPayload::Delivery)
        .def(py::init<>())
        .def("clear", &ImGuiPayload::Clear
            , py::return_value_policy::automatic_reference)
        .def("is_data_type", &ImGuiPayload::IsDataType
            , py::arg("type")
            , py::return_value_policy::automatic_reference)
        .def("is_preview", &ImGuiPayload::IsPreview
            , py::return_value_policy::automatic_reference)
        .def("is_delivery", &ImGuiPayload::IsDelivery
            , py::return_value_policy::automatic_reference)
    ;

    py::class_<ImGuiOnceUponAFrame> _OnceUponAFrame(_imgui, "OnceUponAFrame");
    registry.on(_imgui, "OnceUponAFrame", _OnceUponAFrame);
        _OnceUponAFrame
        .def(py::init<>())
        .def_readwrite("ref_frame", &ImGuiOnceUponAFrame::RefFrame)
    ;

    py::class_<ImGuiTextFilter> _TextFilter(_imgui, "TextFilter");
    registry.on(_imgui, "TextFilter", _TextFilter);
        _TextFilter
        .def(py::init<const char *>()
        , py::arg("default_filter") = nullptr
        )
        .def("draw", &ImGuiTextFilter::Draw
            , py::arg("label") = nullptr
            , py::arg("width") = 0.0f
            , py::return_value_policy::automatic_reference)
        .def("pass_filter", &ImGuiTextFilter::PassFilter
            , py::arg("text")
            , py::arg("text_end") = nullptr
            , py::return_value_policy::automatic_reference)
        .def("build", &ImGuiTextFilter::Build
            , py::return_value_policy::automatic_reference)
        .def("clear", &ImGuiTextFilter::Clear
            , py::return_value_policy::automatic_reference)
        .def("is_active", &ImGuiTextFilter::IsActive
            , py::return_value_policy::automatic_reference)
        ;

        py::class_<ImGuiTextFilter::ImGuiTextRange> _TextFilterTextRange(_imgui, "TextFilterTextRange");
        registry.on(_imgui, "TextFilterTextRange", _TextFilterTextRange);
            _TextFilterTextRange
            .def_property("b",
                [](const ImGuiTextFilter::ImGuiTextRange& self){ return self.b; },
                [](ImGuiTextFilter::ImGuiTextRange& self, const char* source){ self.b = strdup(source); }
            )
            .def_property("e",
                [](const ImGuiTextFilter::ImGuiTextRange& self){ return self.e; },
                [](ImGuiTextFilter::ImGuiTextRange& self, const char* source){ self.e = strdup(source); }
            )
            .def(py::init<>())
            .def(py::init<const char *, const char *>()
            , py::arg("_b")
            , py::arg("_e")
            )
            .def("empty", &ImGuiTextFilter::ImGuiTextRange::empty
                , py::return_value_policy::automatic_reference)
            .def("split", &ImGuiTextFilter::ImGuiTextRange::split
                , py::arg("separator")
                , py::arg("out")
                , py::return_value_policy::automatic_reference)
        ;

        _TextFilter
        .def_readonly("input_buf", &ImGuiTextFilter::InputBuf)
        .def_readwrite("count_grep", &ImGuiTextFilter::CountGrep)
    ;

    py::class_<ImGuiStoragePair> _StoragePair(_imgui, "StoragePair");
    registry.on(_imgui, "StoragePair", _StoragePair);
        _StoragePair
        .def_readwrite("key", &ImGuiStoragePair::key)
        .def(py::init<unsigned int, int>()
        , py::arg("_key")
        , py::arg("_val")
        )
        .def(py::init<unsigned int, float>()
        , py::arg("_key")
        , py::arg("_val")
        )
        .def(py::init<unsigned int, void *>()
        , py::arg("_key")
        , py::arg("_val")
        )
    ;

    py::class_<ImGuiStorage> _Storage(_imgui, "Storage");
    registry.on(_imgui, "Storage", _Storage);
        _Storage
        .def("clear", &ImGuiStorage::Clear
            , py::return_value_policy::automatic_reference)
        .def("get_int", &ImGuiStorage::GetInt
            , py::arg("key")
            , py::arg("default_val") = 0
            , py::return_value_policy::automatic_reference)
        .def("set_int", &ImGuiStorage::SetInt
            , py::arg("key")
            , py::arg("val")
            , py::return_value_policy::automatic_reference)
        .def("get_bool", &ImGuiStorage::GetBool
            , py::arg("key")
            , py::arg("default_val") = false
            , py::return_value_policy::automatic_reference)
        .def("set_bool", &ImGuiStorage::SetBool
            , py::arg("key")
            , py::arg("val")
            , py::return_value_policy::automatic_reference)
        .def("get_float", &ImGuiStorage::GetFloat
            , py::arg("key")
            , py::arg("default_val") = 0.0f
            , py::return_value_policy::automatic_reference)
        .def("set_float", &ImGuiStorage::SetFloat
            , py::arg("key")
            , py::arg("val")
            , py::return_value_policy::automatic_reference)
        .def("get_void_ptr", &ImGuiStorage::GetVoidPtr
            , py::arg("key")
            , py::return_value_policy::automatic_reference)
        .def("set_void_ptr", &ImGuiStorage::SetVoidPtr
            , py::arg("key")
            , py::arg("val")
            , py::return_value_policy::automatic_reference)
        .def("get_int_ref", &ImGuiStorage::GetIntRef
            , py::arg("key")
            , py::arg("default_val") = 0
            , py::return_value_policy::automatic_reference)
        .def("get_bool_ref", &ImGuiStorage::GetBoolRef
            , py::arg("key")
            , py::arg("default_val") = false
            , py::return_value_policy::automatic_reference)
        .def("get_float_ref", &ImGuiStorage::GetFloatRef
            , py::arg("key")
            , py::arg("default_val") = 0.0f
            , py::return_value_policy::automatic_reference)
        .def("get_void_ptr_ref", &ImGuiStorage::GetVoidPtrRef
            , py::arg("key")
            , py::arg("default_val") = nullptr
            , py::return_value_policy::automatic_reference)
        .def("build_sort_by_key", &ImGuiStorage::BuildSortByKey
            , py::return_value_policy::automatic_reference)
        .def("set_all_int", &ImGuiStorage::SetAllInt
            , py::arg("val")
            , py::return_value_policy::automatic_reference)
    ;

    py::enum_<ImGuiListClipperFlags_>(_imgui, "ListClipperFlags", py::arithmetic())
        .value("NONE", ImGuiListClipperFlags_::ImGuiListClipperFlags_None)
        .value("NO_SET_TABLE_ROW_COUNTERS", ImGuiListClipperFlags_::ImGuiListClipperFlags_NoSetTableRowCounters)
        .export_values()
    ;
    py::class_<ImColor> _Color(_imgui, "Color");
    registry.on(_imgui, "Color", _Color);
        _Color
        .def_readwrite("value", &ImColor::Value)
        .def(py::init<>())
        .def(py::init<float, float, float, float>()
        , py::arg("r")
        , py::arg("g")
        , py::arg("b")
        , py::arg("a") = 1.0f
        )
        .def(py::init<const ImVec4 &>()
        , py::arg("col")
        )
        .def(py::init<int, int, int, int>()
        , py::arg("r")
        , py::arg("g")
        , py::arg("b")
        , py::arg("a") = 255
        )
        .def(py::init<unsigned int>()
        , py::arg("rgba")
        )
        .def_static("hsv", &ImColor::HSV
            , py::arg("h")
            , py::arg("s")
            , py::arg("v")
            , py::arg("a") = 1.0f
            , py::return_value_policy::automatic_reference)
    ;

    py::enum_<ImGuiMultiSelectFlags_>(_imgui, "MultiSelectFlags", py::arithmetic())
        .value("NONE", ImGuiMultiSelectFlags_::ImGuiMultiSelectFlags_None)
        .value("SINGLE_SELECT", ImGuiMultiSelectFlags_::ImGuiMultiSelectFlags_SingleSelect)
        .value("NO_SELECT_ALL", ImGuiMultiSelectFlags_::ImGuiMultiSelectFlags_NoSelectAll)
        .value("NO_RANGE_SELECT", ImGuiMultiSelectFlags_::ImGuiMultiSelectFlags_NoRangeSelect)
        .value("NO_AUTO_SELECT", ImGuiMultiSelectFlags_::ImGuiMultiSelectFlags_NoAutoSelect)
        .value("NO_AUTO_CLEAR", ImGuiMultiSelectFlags_::ImGuiMultiSelectFlags_NoAutoClear)
        .value("NO_AUTO_CLEAR_ON_RESELECT", ImGuiMultiSelectFlags_::ImGuiMultiSelectFlags_NoAutoClearOnReselect)
        .value("BOX_SELECT1D", ImGuiMultiSelectFlags_::ImGuiMultiSelectFlags_BoxSelect1d)
        .value("BOX_SELECT2D", ImGuiMultiSelectFlags_::ImGuiMultiSelectFlags_BoxSelect2d)
        .value("BOX_SELECT_NO_SCROLL", ImGuiMultiSelectFlags_::ImGuiMultiSelectFlags_BoxSelectNoScroll)
        .value("CLEAR_ON_ESCAPE", ImGuiMultiSelectFlags_::ImGuiMultiSelectFlags_ClearOnEscape)
        .value("CLEAR_ON_CLICK_VOID", ImGuiMultiSelectFlags_::ImGuiMultiSelectFlags_ClearOnClickVoid)
        .value("SCOPE_WINDOW", ImGuiMultiSelectFlags_::ImGuiMultiSelectFlags_ScopeWindow)
        .value("SCOPE_RECT", ImGuiMultiSelectFlags_::ImGuiMultiSelectFlags_ScopeRect)
        .value("SELECT_ON_CLICK", ImGuiMultiSelectFlags_::ImGuiMultiSelectFlags_SelectOnClick)
        .value("SELECT_ON_CLICK_RELEASE", ImGuiMultiSelectFlags_::ImGuiMultiSelectFlags_SelectOnClickRelease)
        .value("NAV_WRAP_X", ImGuiMultiSelectFlags_::ImGuiMultiSelectFlags_NavWrapX)
        .export_values()
    ;
    py::class_<ImGuiMultiSelectIO> _MultiSelectIO(_imgui, "MultiSelectIO");
    registry.on(_imgui, "MultiSelectIO", _MultiSelectIO);
        _MultiSelectIO
        .def_readwrite("requests", &ImGuiMultiSelectIO::Requests)
        .def_readwrite("range_src_item", &ImGuiMultiSelectIO::RangeSrcItem)
        .def_readwrite("nav_id_item", &ImGuiMultiSelectIO::NavIdItem)
        .def_readwrite("nav_id_selected", &ImGuiMultiSelectIO::NavIdSelected)
        .def_readwrite("range_src_reset", &ImGuiMultiSelectIO::RangeSrcReset)
        .def_readwrite("items_count", &ImGuiMultiSelectIO::ItemsCount)
    ;

    py::enum_<ImGuiSelectionRequestType>(_imgui, "SelectionRequestType", py::arithmetic())
        .value("NONE", ImGuiSelectionRequestType::ImGuiSelectionRequestType_None)
        .value("SET_ALL", ImGuiSelectionRequestType::ImGuiSelectionRequestType_SetAll)
        .value("SET_RANGE", ImGuiSelectionRequestType::ImGuiSelectionRequestType_SetRange)
        .export_values()
    ;
    py::class_<ImGuiSelectionRequest> _SelectionRequest(_imgui, "SelectionRequest");
    registry.on(_imgui, "SelectionRequest", _SelectionRequest);
        _SelectionRequest
        .def_readwrite("type", &ImGuiSelectionRequest::Type)
        .def_readwrite("selected", &ImGuiSelectionRequest::Selected)
        .def_readwrite("range_direction", &ImGuiSelectionRequest::RangeDirection)
        .def_readwrite("range_first_item", &ImGuiSelectionRequest::RangeFirstItem)
        .def_readwrite("range_last_item", &ImGuiSelectionRequest::RangeLastItem)
    ;

    py::class_<ImDrawCmd> _DrawCmd(_imgui, "DrawCmd");
    registry.on(_imgui, "DrawCmd", _DrawCmd);
        _DrawCmd
        .def_readwrite("clip_rect", &ImDrawCmd::ClipRect)
        .def_readwrite("tex_ref", &ImDrawCmd::TexRef)
        .def_readwrite("vtx_offset", &ImDrawCmd::VtxOffset)
        .def_readwrite("idx_offset", &ImDrawCmd::IdxOffset)
        .def_readwrite("elem_count", &ImDrawCmd::ElemCount)
        .def_readwrite("user_callback", &ImDrawCmd::UserCallback)
        .def_readwrite("user_callback_data", &ImDrawCmd::UserCallbackData)
        .def_readwrite("user_callback_data_size", &ImDrawCmd::UserCallbackDataSize)
        .def_readwrite("user_callback_data_offset", &ImDrawCmd::UserCallbackDataOffset)
        .def(py::init<>())
    ;

    py::class_<ImDrawVert> _DrawVert(_imgui, "DrawVert");
    registry.on(_imgui, "DrawVert", _DrawVert);
        _DrawVert
        .def_readwrite("pos", &ImDrawVert::pos)
        .def_readwrite("uv", &ImDrawVert::uv)
        .def_readwrite("col", &ImDrawVert::col)
    ;

    py::class_<ImDrawCmdHeader> _DrawCmdHeader(_imgui, "DrawCmdHeader");
    registry.on(_imgui, "DrawCmdHeader", _DrawCmdHeader);
        _DrawCmdHeader
        .def_readwrite("clip_rect", &ImDrawCmdHeader::ClipRect)
        .def_readwrite("tex_ref", &ImDrawCmdHeader::TexRef)
        .def_readwrite("vtx_offset", &ImDrawCmdHeader::VtxOffset)
    ;

    py::class_<ImDrawChannel> _DrawChannel(_imgui, "DrawChannel");
    registry.on(_imgui, "DrawChannel", _DrawChannel);
    py::class_<ImDrawListSplitter> _DrawListSplitter(_imgui, "DrawListSplitter");
    registry.on(_imgui, "DrawListSplitter", _DrawListSplitter);
        _DrawListSplitter
        .def("clear_free_memory", &ImDrawListSplitter::ClearFreeMemory
            , py::return_value_policy::automatic_reference)
        .def("split", &ImDrawListSplitter::Split
            , py::arg("draw_list")
            , py::arg("count")
            , py::return_value_policy::automatic_reference)
        .def("merge", &ImDrawListSplitter::Merge
            , py::arg("draw_list")
            , py::return_value_policy::automatic_reference)
        .def("set_current_channel", &ImDrawListSplitter::SetCurrentChannel
            , py::arg("draw_list")
            , py::arg("channel_idx")
            , py::return_value_policy::automatic_reference)
    ;

    py::enum_<ImDrawFlags_>(_imgui, "DrawFlags", py::arithmetic())
        .value("NONE", ImDrawFlags_::ImDrawFlags_None)
        .value("CLOSED", ImDrawFlags_::ImDrawFlags_Closed)
        .value("ROUND_CORNERS_TOP_LEFT", ImDrawFlags_::ImDrawFlags_RoundCornersTopLeft)
        .value("ROUND_CORNERS_TOP_RIGHT", ImDrawFlags_::ImDrawFlags_RoundCornersTopRight)
        .value("ROUND_CORNERS_BOTTOM_LEFT", ImDrawFlags_::ImDrawFlags_RoundCornersBottomLeft)
        .value("ROUND_CORNERS_BOTTOM_RIGHT", ImDrawFlags_::ImDrawFlags_RoundCornersBottomRight)
        .value("ROUND_CORNERS_NONE", ImDrawFlags_::ImDrawFlags_RoundCornersNone)
        .value("ROUND_CORNERS_TOP", ImDrawFlags_::ImDrawFlags_RoundCornersTop)
        .value("ROUND_CORNERS_BOTTOM", ImDrawFlags_::ImDrawFlags_RoundCornersBottom)
        .value("ROUND_CORNERS_LEFT", ImDrawFlags_::ImDrawFlags_RoundCornersLeft)
        .value("ROUND_CORNERS_RIGHT", ImDrawFlags_::ImDrawFlags_RoundCornersRight)
        .value("ROUND_CORNERS_ALL", ImDrawFlags_::ImDrawFlags_RoundCornersAll)
        .value("ROUND_CORNERS_DEFAULT", ImDrawFlags_::ImDrawFlags_RoundCornersDefault_)
        .value("ROUND_CORNERS_MASK", ImDrawFlags_::ImDrawFlags_RoundCornersMask_)
        .export_values()
    ;
    py::enum_<ImDrawListFlags_>(_imgui, "DrawListFlags", py::arithmetic())
        .value("NONE", ImDrawListFlags_::ImDrawListFlags_None)
        .value("ANTI_ALIASED_LINES", ImDrawListFlags_::ImDrawListFlags_AntiAliasedLines)
        .value("ANTI_ALIASED_LINES_USE_TEX", ImDrawListFlags_::ImDrawListFlags_AntiAliasedLinesUseTex)
        .value("ANTI_ALIASED_FILL", ImDrawListFlags_::ImDrawListFlags_AntiAliasedFill)
        .value("ALLOW_VTX_OFFSET", ImDrawListFlags_::ImDrawListFlags_AllowVtxOffset)
        .export_values()
    ;
    py::class_<ImDrawList> _DrawList(_imgui, "DrawList");
    registry.on(_imgui, "DrawList", _DrawList);
        _DrawList
        .def_readwrite("cmd_buffer", &ImDrawList::CmdBuffer)
        .def_readwrite("idx_buffer", &ImDrawList::IdxBuffer)
        .def_readwrite("vtx_buffer", &ImDrawList::VtxBuffer)
        .def_readwrite("flags", &ImDrawList::Flags)
        .def("push_clip_rect", &ImDrawList::PushClipRect
            , py::arg("clip_rect_min")
            , py::arg("clip_rect_max")
            , py::arg("intersect_with_current_clip_rect") = false
            , py::return_value_policy::automatic_reference)
        .def("push_clip_rect_full_screen", &ImDrawList::PushClipRectFullScreen
            , py::return_value_policy::automatic_reference)
        .def("pop_clip_rect", &ImDrawList::PopClipRect
            , py::return_value_policy::automatic_reference)
        .def("push_texture", &ImDrawList::PushTexture
            , py::arg("tex_ref")
            , py::return_value_policy::automatic_reference)
        .def("pop_texture", &ImDrawList::PopTexture
            , py::return_value_policy::automatic_reference)
        .def("add_line", &ImDrawList::AddLine
            , py::arg("p1")
            , py::arg("p2")
            , py::arg("col")
            , py::arg("thickness") = 1.0f
            , py::return_value_policy::automatic_reference)
        .def("add_rect", &ImDrawList::AddRect
            , py::arg("p_min")
            , py::arg("p_max")
            , py::arg("col")
            , py::arg("rounding") = 0.0f
            , py::arg("flags") = 0
            , py::arg("thickness") = 1.0f
            , py::return_value_policy::automatic_reference)
        .def("add_rect_filled", &ImDrawList::AddRectFilled
            , py::arg("p_min")
            , py::arg("p_max")
            , py::arg("col")
            , py::arg("rounding") = 0.0f
            , py::arg("flags") = 0
            , py::return_value_policy::automatic_reference)
        .def("add_rect_filled_multi_color", &ImDrawList::AddRectFilledMultiColor
            , py::arg("p_min")
            , py::arg("p_max")
            , py::arg("col_upr_left")
            , py::arg("col_upr_right")
            , py::arg("col_bot_right")
            , py::arg("col_bot_left")
            , py::return_value_policy::automatic_reference)
        .def("add_quad", &ImDrawList::AddQuad
            , py::arg("p1")
            , py::arg("p2")
            , py::arg("p3")
            , py::arg("p4")
            , py::arg("col")
            , py::arg("thickness") = 1.0f
            , py::return_value_policy::automatic_reference)
        .def("add_quad_filled", &ImDrawList::AddQuadFilled
            , py::arg("p1")
            , py::arg("p2")
            , py::arg("p3")
            , py::arg("p4")
            , py::arg("col")
            , py::return_value_policy::automatic_reference)
        .def("add_triangle", &ImDrawList::AddTriangle
            , py::arg("p1")
            , py::arg("p2")
            , py::arg("p3")
            , py::arg("col")
            , py::arg("thickness") = 1.0f
            , py::return_value_policy::automatic_reference)
        .def("add_triangle_filled", &ImDrawList::AddTriangleFilled
            , py::arg("p1")
            , py::arg("p2")
            , py::arg("p3")
            , py::arg("col")
            , py::return_value_policy::automatic_reference)
        .def("add_circle", &ImDrawList::AddCircle
            , py::arg("center")
            , py::arg("radius")
            , py::arg("col")
            , py::arg("num_segments") = 0
            , py::arg("thickness") = 1.0f
            , py::return_value_policy::automatic_reference)
        .def("add_circle_filled", &ImDrawList::AddCircleFilled
            , py::arg("center")
            , py::arg("radius")
            , py::arg("col")
            , py::arg("num_segments") = 0
            , py::return_value_policy::automatic_reference)
        .def("add_ngon", &ImDrawList::AddNgon
            , py::arg("center")
            , py::arg("radius")
            , py::arg("col")
            , py::arg("num_segments")
            , py::arg("thickness") = 1.0f
            , py::return_value_policy::automatic_reference)
        .def("add_ngon_filled", &ImDrawList::AddNgonFilled
            , py::arg("center")
            , py::arg("radius")
            , py::arg("col")
            , py::arg("num_segments")
            , py::return_value_policy::automatic_reference)
        .def("add_ellipse", &ImDrawList::AddEllipse
            , py::arg("center")
            , py::arg("radius")
            , py::arg("col")
            , py::arg("rot") = 0.0f
            , py::arg("num_segments") = 0
            , py::arg("thickness") = 1.0f
            , py::return_value_policy::automatic_reference)
        .def("add_ellipse_filled", &ImDrawList::AddEllipseFilled
            , py::arg("center")
            , py::arg("radius")
            , py::arg("col")
            , py::arg("rot") = 0.0f
            , py::arg("num_segments") = 0
            , py::return_value_policy::automatic_reference)
        .def("add_text", py::overload_cast<const ImVec2 &, unsigned int, const char *, const char *>(&ImDrawList::AddText)
            , py::arg("pos")
            , py::arg("col")
            , py::arg("text_begin")
            , py::arg("text_end") = nullptr
            , py::return_value_policy::automatic_reference)
        .def("add_text", py::overload_cast<ImFont *, float, const ImVec2 &, unsigned int, const char *, const char *, float, const ImVec4 *>(&ImDrawList::AddText)
            , py::arg("font")
            , py::arg("font_size")
            , py::arg("pos")
            , py::arg("col")
            , py::arg("text_begin")
            , py::arg("text_end") = nullptr
            , py::arg("wrap_width") = 0.0f
            , py::arg("cpu_fine_clip_rect") = nullptr
            , py::return_value_policy::automatic_reference)
        .def("add_bezier_cubic", &ImDrawList::AddBezierCubic
            , py::arg("p1")
            , py::arg("p2")
            , py::arg("p3")
            , py::arg("p4")
            , py::arg("col")
            , py::arg("thickness")
            , py::arg("num_segments") = 0
            , py::return_value_policy::automatic_reference)
        .def("add_bezier_quadratic", &ImDrawList::AddBezierQuadratic
            , py::arg("p1")
            , py::arg("p2")
            , py::arg("p3")
            , py::arg("col")
            , py::arg("thickness")
            , py::arg("num_segments") = 0
            , py::return_value_policy::automatic_reference)
        .def("add_polyline", &ImDrawList::AddPolyline
            , py::arg("points")
            , py::arg("num_points")
            , py::arg("col")
            , py::arg("flags")
            , py::arg("thickness")
            , py::return_value_policy::automatic_reference)
        .def("add_convex_poly_filled", &ImDrawList::AddConvexPolyFilled
            , py::arg("points")
            , py::arg("num_points")
            , py::arg("col")
            , py::return_value_policy::automatic_reference)
        .def("add_concave_poly_filled", &ImDrawList::AddConcavePolyFilled
            , py::arg("points")
            , py::arg("num_points")
            , py::arg("col")
            , py::return_value_policy::automatic_reference)
        .def("add_image", &ImDrawList::AddImage
            , py::arg("tex_ref")
            , py::arg("p_min")
            , py::arg("p_max")
            , py::arg("uv_min") = ImVec2(0,0)
            , py::arg("uv_max") = ImVec2(1,1)
            , py::arg("col") = IM_COL32_WHITE
            , py::return_value_policy::automatic_reference)
        .def("add_image_quad", &ImDrawList::AddImageQuad
            , py::arg("tex_ref")
            , py::arg("p1")
            , py::arg("p2")
            , py::arg("p3")
            , py::arg("p4")
            , py::arg("uv1") = ImVec2(0,0)
            , py::arg("uv2") = ImVec2(1,0)
            , py::arg("uv3") = ImVec2(1,1)
            , py::arg("uv4") = ImVec2(0,1)
            , py::arg("col") = IM_COL32_WHITE
            , py::return_value_policy::automatic_reference)
        .def("add_image_rounded", &ImDrawList::AddImageRounded
            , py::arg("tex_ref")
            , py::arg("p_min")
            , py::arg("p_max")
            , py::arg("uv_min")
            , py::arg("uv_max")
            , py::arg("col")
            , py::arg("rounding")
            , py::arg("flags") = 0
            , py::return_value_policy::automatic_reference)
        .def("path_arc_to", &ImDrawList::PathArcTo
            , py::arg("center")
            , py::arg("radius")
            , py::arg("a_min")
            , py::arg("a_max")
            , py::arg("num_segments") = 0
            , py::return_value_policy::automatic_reference)
        .def("path_arc_to_fast", &ImDrawList::PathArcToFast
            , py::arg("center")
            , py::arg("radius")
            , py::arg("a_min_of_12")
            , py::arg("a_max_of_12")
            , py::return_value_policy::automatic_reference)
        .def("path_elliptical_arc_to", &ImDrawList::PathEllipticalArcTo
            , py::arg("center")
            , py::arg("radius")
            , py::arg("rot")
            , py::arg("a_min")
            , py::arg("a_max")
            , py::arg("num_segments") = 0
            , py::return_value_policy::automatic_reference)
        .def("path_bezier_cubic_curve_to", &ImDrawList::PathBezierCubicCurveTo
            , py::arg("p2")
            , py::arg("p3")
            , py::arg("p4")
            , py::arg("num_segments") = 0
            , py::return_value_policy::automatic_reference)
        .def("path_bezier_quadratic_curve_to", &ImDrawList::PathBezierQuadraticCurveTo
            , py::arg("p2")
            , py::arg("p3")
            , py::arg("num_segments") = 0
            , py::return_value_policy::automatic_reference)
        .def("path_rect", &ImDrawList::PathRect
            , py::arg("rect_min")
            , py::arg("rect_max")
            , py::arg("rounding") = 0.0f
            , py::arg("flags") = 0
            , py::return_value_policy::automatic_reference)
        .def("add_callback", &ImDrawList::AddCallback
            , py::arg("callback")
            , py::arg("userdata")
            , py::arg("userdata_size") = 0
            , py::return_value_policy::automatic_reference)
        .def("add_draw_cmd", &ImDrawList::AddDrawCmd
            , py::return_value_policy::automatic_reference)
        .def("clone_output", &ImDrawList::CloneOutput
            , py::return_value_policy::automatic_reference)
        .def("prim_reserve", &ImDrawList::PrimReserve
            , py::arg("idx_count")
            , py::arg("vtx_count")
            , py::return_value_policy::automatic_reference)
        .def("prim_unreserve", &ImDrawList::PrimUnreserve
            , py::arg("idx_count")
            , py::arg("vtx_count")
            , py::return_value_policy::automatic_reference)
        .def("prim_rect", &ImDrawList::PrimRect
            , py::arg("a")
            , py::arg("b")
            , py::arg("col")
            , py::return_value_policy::automatic_reference)
        .def("prim_rect_uv", &ImDrawList::PrimRectUV
            , py::arg("a")
            , py::arg("b")
            , py::arg("uv_a")
            , py::arg("uv_b")
            , py::arg("col")
            , py::return_value_policy::automatic_reference)
        .def("prim_quad_uv", &ImDrawList::PrimQuadUV
            , py::arg("a")
            , py::arg("b")
            , py::arg("c")
            , py::arg("d")
            , py::arg("uv_a")
            , py::arg("uv_b")
            , py::arg("uv_c")
            , py::arg("uv_d")
            , py::arg("col")
            , py::return_value_policy::automatic_reference)
    ;

    py::class_<ImDrawData> _DrawData(_imgui, "DrawData");
    registry.on(_imgui, "DrawData", _DrawData);
        _DrawData
        .def_readwrite("valid", &ImDrawData::Valid)
        .def_readwrite("cmd_lists_count", &ImDrawData::CmdListsCount)
        .def_readwrite("total_idx_count", &ImDrawData::TotalIdxCount)
        .def_readwrite("total_vtx_count", &ImDrawData::TotalVtxCount)
        .def_readwrite("display_pos", &ImDrawData::DisplayPos)
        .def_readwrite("display_size", &ImDrawData::DisplaySize)
        .def_readwrite("framebuffer_scale", &ImDrawData::FramebufferScale)
        .def_readwrite("owner_viewport", &ImDrawData::OwnerViewport)
        .def_readwrite("textures", &ImDrawData::Textures)
        .def(py::init<>())
        .def("clear", &ImDrawData::Clear
            , py::return_value_policy::automatic_reference)
        .def("add_draw_list", &ImDrawData::AddDrawList
            , py::arg("draw_list")
            , py::return_value_policy::automatic_reference)
        .def("de_index_all_buffers", &ImDrawData::DeIndexAllBuffers
            , py::return_value_policy::automatic_reference)
        .def("scale_clip_rects", &ImDrawData::ScaleClipRects
            , py::arg("fb_scale")
            , py::return_value_policy::automatic_reference)
    ;

    py::enum_<ImTextureFormat>(_imgui, "TextureFormat", py::arithmetic())
        .value("RGBA32", ImTextureFormat::ImTextureFormat_RGBA32)
        .value("ALPHA8", ImTextureFormat::ImTextureFormat_Alpha8)
        .export_values()
    ;
    py::enum_<ImTextureStatus>(_imgui, "TextureStatus", py::arithmetic())
        .value("OK", ImTextureStatus::ImTextureStatus_OK)
        .value("DESTROYED", ImTextureStatus::ImTextureStatus_Destroyed)
        .value("WANT_CREATE", ImTextureStatus::ImTextureStatus_WantCreate)
        .value("WANT_UPDATES", ImTextureStatus::ImTextureStatus_WantUpdates)
        .value("WANT_DESTROY", ImTextureStatus::ImTextureStatus_WantDestroy)
        .export_values()
    ;
    py::class_<ImTextureRect> _TextureRect(_imgui, "TextureRect");
    registry.on(_imgui, "TextureRect", _TextureRect);
        _TextureRect
        .def_readwrite("x", &ImTextureRect::x)
        .def_readwrite("y", &ImTextureRect::y)
        .def_readwrite("w", &ImTextureRect::w)
        .def_readwrite("h", &ImTextureRect::h)
    ;

    py::class_<ImTextureData> _TextureData(_imgui, "TextureData");
    registry.on(_imgui, "TextureData", _TextureData);
        _TextureData
        .def_readwrite("unique_id", &ImTextureData::UniqueID)
        .def_readwrite("status", &ImTextureData::Status)
        .def_readwrite("backend_user_data", &ImTextureData::BackendUserData)
        .def_readwrite("tex_id", &ImTextureData::TexID)
        .def_readwrite("format", &ImTextureData::Format)
        .def_readwrite("width", &ImTextureData::Width)
        .def_readwrite("height", &ImTextureData::Height)
        .def_readwrite("bytes_per_pixel", &ImTextureData::BytesPerPixel)
        .def_readwrite("used_rect", &ImTextureData::UsedRect)
        .def_readwrite("update_rect", &ImTextureData::UpdateRect)
        .def_readwrite("updates", &ImTextureData::Updates)
        .def_readwrite("unused_frames", &ImTextureData::UnusedFrames)
        .def_readwrite("ref_count", &ImTextureData::RefCount)
        .def_readwrite("use_colors", &ImTextureData::UseColors)
        .def_readwrite("want_destroy_next_frame", &ImTextureData::WantDestroyNextFrame)
        .def(py::init<>())
        .def("create", &ImTextureData::Create
            , py::arg("format")
            , py::arg("w")
            , py::arg("h")
            , py::return_value_policy::automatic_reference)
        .def("destroy_pixels", &ImTextureData::DestroyPixels
            , py::return_value_policy::automatic_reference)
        .def("get_pixels", &ImTextureData::GetPixels
            , py::return_value_policy::automatic_reference)
        .def("get_pixels_at", &ImTextureData::GetPixelsAt
            , py::arg("x")
            , py::arg("y")
            , py::return_value_policy::automatic_reference)
        .def("get_size_in_bytes", &ImTextureData::GetSizeInBytes
            , py::return_value_policy::automatic_reference)
        .def("get_pitch", &ImTextureData::GetPitch
            , py::return_value_policy::automatic_reference)
        .def("get_tex_ref", &ImTextureData::GetTexRef
            , py::return_value_policy::automatic_reference)
        .def("get_tex_id", &ImTextureData::GetTexID
            , py::return_value_policy::automatic_reference)
        .def("set_tex_id", &ImTextureData::SetTexID
            , py::arg("tex_id")
            , py::return_value_policy::automatic_reference)
        .def("set_status", &ImTextureData::SetStatus
            , py::arg("status")
            , py::return_value_policy::automatic_reference)
    ;

    py::class_<ImFontConfig> _FontConfig(_imgui, "FontConfig");
    registry.on(_imgui, "FontConfig", _FontConfig);
        _FontConfig
        .def_readonly("name", &ImFontConfig::Name)
        .def_readwrite("font_data", &ImFontConfig::FontData)
        .def_readwrite("font_data_size", &ImFontConfig::FontDataSize)
        .def_readwrite("font_data_owned_by_atlas", &ImFontConfig::FontDataOwnedByAtlas)
        .def_readwrite("merge_mode", &ImFontConfig::MergeMode)
        .def_readwrite("pixel_snap_h", &ImFontConfig::PixelSnapH)
        .def_readwrite("pixel_snap_v", &ImFontConfig::PixelSnapV)
        .def_readwrite("oversample_h", &ImFontConfig::OversampleH)
        .def_readwrite("oversample_v", &ImFontConfig::OversampleV)
        .def_readwrite("ellipsis_char", &ImFontConfig::EllipsisChar)
        .def_readwrite("size_pixels", &ImFontConfig::SizePixels)
        .def_readwrite("glyph_ranges", &ImFontConfig::GlyphRanges)
        .def_readwrite("glyph_exclude_ranges", &ImFontConfig::GlyphExcludeRanges)
        .def_readwrite("glyph_offset", &ImFontConfig::GlyphOffset)
        .def_readwrite("glyph_min_advance_x", &ImFontConfig::GlyphMinAdvanceX)
        .def_readwrite("glyph_max_advance_x", &ImFontConfig::GlyphMaxAdvanceX)
        .def_readwrite("glyph_extra_advance_x", &ImFontConfig::GlyphExtraAdvanceX)
        .def_readwrite("font_no", &ImFontConfig::FontNo)
        .def_readwrite("font_loader_flags", &ImFontConfig::FontLoaderFlags)
        .def_readwrite("rasterizer_multiply", &ImFontConfig::RasterizerMultiply)
        .def_readwrite("rasterizer_density", &ImFontConfig::RasterizerDensity)
        .def_readwrite("flags", &ImFontConfig::Flags)
        .def_readwrite("dst_font", &ImFontConfig::DstFont)
        //render_wrapped_field
        .def_property("font_loader",
            [](const ImFontConfig& self){ return py::capsule(self.FontLoader, "ImFontLoader"); },
            [](ImFontConfig& self, const py::capsule& value){ self.FontLoader = value; }
        )
        .def_readwrite("font_loader_data", &ImFontConfig::FontLoaderData)
        .def(py::init<>())
    ;

    py::class_<ImFontGlyph> _FontGlyph(_imgui, "FontGlyph");
    registry.on(_imgui, "FontGlyph", _FontGlyph);
        _FontGlyph
        .def_property("colored",
            [](ImFontGlyph& self){ return self.Colored; },
            [](ImFontGlyph& self, unsigned int source){ self.Colored = source; }
        )
        .def_property("visible",
            [](ImFontGlyph& self){ return self.Visible; },
            [](ImFontGlyph& self, unsigned int source){ self.Visible = source; }
        )
        .def_property("source_idx",
            [](ImFontGlyph& self){ return self.SourceIdx; },
            [](ImFontGlyph& self, unsigned int source){ self.SourceIdx = source; }
        )
        .def_property("codepoint",
            [](ImFontGlyph& self){ return self.Codepoint; },
            [](ImFontGlyph& self, unsigned int source){ self.Codepoint = source; }
        )
        .def_readwrite("advance_x", &ImFontGlyph::AdvanceX)
        .def_readwrite("x0", &ImFontGlyph::X0)
        .def_readwrite("y0", &ImFontGlyph::Y0)
        .def_readwrite("x1", &ImFontGlyph::X1)
        .def_readwrite("y1", &ImFontGlyph::Y1)
        .def_readwrite("u0", &ImFontGlyph::U0)
        .def_readwrite("v0", &ImFontGlyph::V0)
        .def_readwrite("u1", &ImFontGlyph::U1)
        .def_readwrite("v1", &ImFontGlyph::V1)
        .def_readwrite("pack_id", &ImFontGlyph::PackId)
        .def(py::init<>())
    ;

    py::class_<ImFontGlyphRangesBuilder> _FontGlyphRangesBuilder(_imgui, "FontGlyphRangesBuilder");
    registry.on(_imgui, "FontGlyphRangesBuilder", _FontGlyphRangesBuilder);
        _FontGlyphRangesBuilder
        .def_readwrite("used_chars", &ImFontGlyphRangesBuilder::UsedChars)
        .def(py::init<>())
        .def("add_text", &ImFontGlyphRangesBuilder::AddText
            , py::arg("text")
            , py::arg("text_end") = nullptr
            , py::return_value_policy::automatic_reference)
        .def("add_ranges", &ImFontGlyphRangesBuilder::AddRanges
            , py::arg("ranges")
            , py::return_value_policy::automatic_reference)
        .def("build_ranges", &ImFontGlyphRangesBuilder::BuildRanges
            , py::arg("out_ranges")
            , py::return_value_policy::automatic_reference)
    ;

    py::class_<ImFontAtlasRect> _FontAtlasRect(_imgui, "FontAtlasRect");
    registry.on(_imgui, "FontAtlasRect", _FontAtlasRect);
        _FontAtlasRect
        .def_readwrite("x", &ImFontAtlasRect::x)
        .def_readwrite("y", &ImFontAtlasRect::y)
        .def_readwrite("w", &ImFontAtlasRect::w)
        .def_readwrite("h", &ImFontAtlasRect::h)
        .def_readwrite("uv0", &ImFontAtlasRect::uv0)
        .def_readwrite("uv1", &ImFontAtlasRect::uv1)
        .def(py::init<>())
    ;

    py::enum_<ImFontAtlasFlags_>(_imgui, "FontAtlasFlags", py::arithmetic())
        .value("NONE", ImFontAtlasFlags_::ImFontAtlasFlags_None)
        .value("NO_POWER_OF_TWO_HEIGHT", ImFontAtlasFlags_::ImFontAtlasFlags_NoPowerOfTwoHeight)
        .value("NO_MOUSE_CURSORS", ImFontAtlasFlags_::ImFontAtlasFlags_NoMouseCursors)
        .value("NO_BAKED_LINES", ImFontAtlasFlags_::ImFontAtlasFlags_NoBakedLines)
        .export_values()
    ;
    py::class_<ImFontAtlas> _FontAtlas(_imgui, "FontAtlas");
    registry.on(_imgui, "FontAtlas", _FontAtlas);
        _FontAtlas
        .def(py::init<>())
        .def("add_font", &ImFontAtlas::AddFont
            , py::arg("font_cfg")
            , py::return_value_policy::automatic_reference)
        .def("add_font_default", &ImFontAtlas::AddFontDefault
            , py::arg("font_cfg") = nullptr
            , py::return_value_policy::automatic_reference)
        .def("add_font_from_memory_ttf", &ImFontAtlas::AddFontFromMemoryTTF
            , py::arg("font_data")
            , py::arg("font_data_size")
            , py::arg("size_pixels") = 0.0f
            , py::arg("font_cfg") = nullptr
            , py::arg("glyph_ranges") = nullptr
            , py::return_value_policy::automatic_reference)
        .def("add_font_from_memory_compressed_ttf", &ImFontAtlas::AddFontFromMemoryCompressedTTF
            , py::arg("compressed_font_data")
            , py::arg("compressed_font_data_size")
            , py::arg("size_pixels") = 0.0f
            , py::arg("font_cfg") = nullptr
            , py::arg("glyph_ranges") = nullptr
            , py::return_value_policy::automatic_reference)
        .def("add_font_from_memory_compressed_base85ttf", &ImFontAtlas::AddFontFromMemoryCompressedBase85TTF
            , py::arg("compressed_font_data_base85")
            , py::arg("size_pixels") = 0.0f
            , py::arg("font_cfg") = nullptr
            , py::arg("glyph_ranges") = nullptr
            , py::return_value_policy::automatic_reference)
        .def("remove_font", &ImFontAtlas::RemoveFont
            , py::arg("font")
            , py::return_value_policy::automatic_reference)
        .def("clear", &ImFontAtlas::Clear
            , py::return_value_policy::automatic_reference)
        .def("compact_cache", &ImFontAtlas::CompactCache
            , py::return_value_policy::automatic_reference)
        .def("set_font_loader", [](ImFontAtlas& self, const py::capsule& font_loader)
            {
                self.SetFontLoader(font_loader);
                return ;
            }
            , py::arg("font_loader")
            , py::return_value_policy::automatic_reference)
        .def("clear_input_data", &ImFontAtlas::ClearInputData
            , py::return_value_policy::automatic_reference)
        .def("clear_fonts", &ImFontAtlas::ClearFonts
            , py::return_value_policy::automatic_reference)
        .def("clear_tex_data", &ImFontAtlas::ClearTexData
            , py::return_value_policy::automatic_reference)
        .def("get_glyph_ranges_default", &ImFontAtlas::GetGlyphRangesDefault
            , py::return_value_policy::automatic_reference)
        .def("add_custom_rect", &ImFontAtlas::AddCustomRect
            , py::arg("width")
            , py::arg("height")
            , py::arg("out_r") = nullptr
            , py::return_value_policy::automatic_reference)
        .def("remove_custom_rect", &ImFontAtlas::RemoveCustomRect
            , py::arg("id")
            , py::return_value_policy::automatic_reference)
        .def("get_custom_rect", &ImFontAtlas::GetCustomRect
            , py::arg("id")
            , py::arg("out_r")
            , py::return_value_policy::automatic_reference)
        .def_readwrite("flags", &ImFontAtlas::Flags)
        .def_readwrite("tex_desired_format", &ImFontAtlas::TexDesiredFormat)
        .def_readwrite("tex_glyph_padding", &ImFontAtlas::TexGlyphPadding)
        .def_readwrite("tex_min_width", &ImFontAtlas::TexMinWidth)
        .def_readwrite("tex_min_height", &ImFontAtlas::TexMinHeight)
        .def_readwrite("tex_max_width", &ImFontAtlas::TexMaxWidth)
        .def_readwrite("tex_max_height", &ImFontAtlas::TexMaxHeight)
        .def_readwrite("user_data", &ImFontAtlas::UserData)
        .def_readwrite("tex_ref", &ImFontAtlas::TexRef)
        .def_readwrite("tex_data", &ImFontAtlas::TexData)
        .def_readwrite("tex_list", &ImFontAtlas::TexList)
        .def_readwrite("locked", &ImFontAtlas::Locked)
        .def_readwrite("renderer_has_textures", &ImFontAtlas::RendererHasTextures)
        .def_readwrite("tex_is_built", &ImFontAtlas::TexIsBuilt)
        .def_readwrite("tex_pixels_use_colors", &ImFontAtlas::TexPixelsUseColors)
        .def_readwrite("tex_uv_scale", &ImFontAtlas::TexUvScale)
        .def_readwrite("tex_uv_white_pixel", &ImFontAtlas::TexUvWhitePixel)
        .def_readwrite("sources", &ImFontAtlas::Sources)
        .def_readonly("tex_uv_lines", &ImFontAtlas::TexUvLines)
        .def_readwrite("tex_next_unique_id", &ImFontAtlas::TexNextUniqueID)
        .def_readwrite("font_next_unique_id", &ImFontAtlas::FontNextUniqueID)
        .def_readwrite("draw_list_shared_datas", &ImFontAtlas::DrawListSharedDatas)
        //render_wrapped_field
        .def_property("builder",
            [](const ImFontAtlas& self){ return py::capsule(self.Builder, "ImFontAtlasBuilder"); },
            [](ImFontAtlas& self, const py::capsule& value){ self.Builder = value; }
        )
        //render_wrapped_field
        .def_property("font_loader",
            [](const ImFontAtlas& self){ return py::capsule(self.FontLoader, "ImFontLoader"); },
            [](ImFontAtlas& self, const py::capsule& value){ self.FontLoader = value; }
        )
        .def_property("font_loader_name",
            [](const ImFontAtlas& self){ return self.FontLoaderName; },
            [](ImFontAtlas& self, const char* source){ self.FontLoaderName = strdup(source); }
        )
        .def_readwrite("font_loader_data", &ImFontAtlas::FontLoaderData)
        .def_readwrite("font_loader_flags", &ImFontAtlas::FontLoaderFlags)
        .def_readwrite("ref_count", &ImFontAtlas::RefCount)
        //render_wrapped_field
        .def_property("owner_context",
            [](const ImFontAtlas& self){ return py::capsule(self.OwnerContext, "ImGuiContext"); },
            [](ImFontAtlas& self, const py::capsule& value){ self.OwnerContext = value; }
        )
    ;

    py::class_<ImFontBaked> _FontBaked(_imgui, "FontBaked");
    registry.on(_imgui, "FontBaked", _FontBaked);
        _FontBaked
        .def_readwrite("index_advance_x", &ImFontBaked::IndexAdvanceX)
        .def_readwrite("fallback_advance_x", &ImFontBaked::FallbackAdvanceX)
        .def_readwrite("size", &ImFontBaked::Size)
        .def_readwrite("rasterizer_density", &ImFontBaked::RasterizerDensity)
        .def_readwrite("index_lookup", &ImFontBaked::IndexLookup)
        .def_readwrite("glyphs", &ImFontBaked::Glyphs)
        .def_readwrite("fallback_glyph_index", &ImFontBaked::FallbackGlyphIndex)
        .def_readwrite("ascent", &ImFontBaked::Ascent)
        .def_readwrite("descent", &ImFontBaked::Descent)
        .def_property("metrics_total_surface",
            [](ImFontBaked& self){ return self.MetricsTotalSurface; },
            [](ImFontBaked& self, unsigned int source){ self.MetricsTotalSurface = source; }
        )
        .def_property("want_destroy",
            [](ImFontBaked& self){ return self.WantDestroy; },
            [](ImFontBaked& self, unsigned int source){ self.WantDestroy = source; }
        )
        .def_property("load_no_fallback",
            [](ImFontBaked& self){ return self.LoadNoFallback; },
            [](ImFontBaked& self, unsigned int source){ self.LoadNoFallback = source; }
        )
        .def_property("load_no_render_on_layout",
            [](ImFontBaked& self){ return self.LoadNoRenderOnLayout; },
            [](ImFontBaked& self, unsigned int source){ self.LoadNoRenderOnLayout = source; }
        )
        .def_readwrite("last_used_frame", &ImFontBaked::LastUsedFrame)
        .def_readwrite("baked_id", &ImFontBaked::BakedId)
        .def_readwrite("container_font", &ImFontBaked::ContainerFont)
        .def_readwrite("font_loader_datas", &ImFontBaked::FontLoaderDatas)
        .def(py::init<>())
        .def("clear_output_data", &ImFontBaked::ClearOutputData
            , py::return_value_policy::automatic_reference)
        .def("find_glyph", &ImFontBaked::FindGlyph
            , py::arg("c")
            , py::return_value_policy::automatic_reference)
        .def("find_glyph_no_fallback", &ImFontBaked::FindGlyphNoFallback
            , py::arg("c")
            , py::return_value_policy::automatic_reference)
        .def("get_char_advance", &ImFontBaked::GetCharAdvance
            , py::arg("c")
            , py::return_value_policy::automatic_reference)
        .def("is_glyph_loaded", &ImFontBaked::IsGlyphLoaded
            , py::arg("c")
            , py::return_value_policy::automatic_reference)
    ;

    py::enum_<ImFontFlags_>(_imgui, "FontFlags", py::arithmetic())
        .value("NONE", ImFontFlags_::ImFontFlags_None)
        .value("NO_LOAD_ERROR", ImFontFlags_::ImFontFlags_NoLoadError)
        .value("NO_LOAD_GLYPHS", ImFontFlags_::ImFontFlags_NoLoadGlyphs)
        .value("LOCK_BAKED_SIZES", ImFontFlags_::ImFontFlags_LockBakedSizes)
        .export_values()
    ;
    py::class_<ImFont> _Font(_imgui, "Font");
    registry.on(_imgui, "Font", _Font);
        _Font
        .def_readwrite("last_baked", &ImFont::LastBaked)
        .def_readwrite("container_atlas", &ImFont::ContainerAtlas)
        .def_readwrite("flags", &ImFont::Flags)
        .def_readwrite("current_rasterizer_density", &ImFont::CurrentRasterizerDensity)
        .def_readwrite("font_id", &ImFont::FontId)
        .def_readwrite("legacy_size", &ImFont::LegacySize)
        .def_readwrite("sources", &ImFont::Sources)
        .def_readwrite("ellipsis_char", &ImFont::EllipsisChar)
        .def_readwrite("fallback_char", &ImFont::FallbackChar)
        .def_readonly("used8k_pages_map", &ImFont::Used8kPagesMap)
        .def_readwrite("ellipsis_auto_bake", &ImFont::EllipsisAutoBake)
        .def_readwrite("remap_pairs", &ImFont::RemapPairs)
        .def(py::init<>())
        .def("is_glyph_in_font", &ImFont::IsGlyphInFont
            , py::arg("c")
            , py::return_value_policy::automatic_reference)
        .def("is_loaded", &ImFont::IsLoaded
            , py::return_value_policy::automatic_reference)
        .def("get_debug_name", &ImFont::GetDebugName
            , py::return_value_policy::automatic_reference)
        .def("get_font_baked", &ImFont::GetFontBaked
            , py::arg("font_size")
            , py::arg("density") = -1.0f
            , py::return_value_policy::automatic_reference)
        .def("calc_word_wrap_position", &ImFont::CalcWordWrapPosition
            , py::arg("size")
            , py::arg("text")
            , py::arg("text_end")
            , py::arg("wrap_width")
            , py::return_value_policy::automatic_reference)
        .def("render_char", &ImFont::RenderChar
            , py::arg("draw_list")
            , py::arg("size")
            , py::arg("pos")
            , py::arg("col")
            , py::arg("c")
            , py::arg("cpu_fine_clip") = nullptr
            , py::return_value_policy::automatic_reference)
        .def("render_text", &ImFont::RenderText
            , py::arg("draw_list")
            , py::arg("size")
            , py::arg("pos")
            , py::arg("col")
            , py::arg("clip_rect")
            , py::arg("text_begin")
            , py::arg("text_end")
            , py::arg("wrap_width") = 0.0f
            , py::arg("flags") = 0
            , py::return_value_policy::automatic_reference)
        .def("clear_output_data", &ImFont::ClearOutputData
            , py::return_value_policy::automatic_reference)
        .def("add_remap_char", &ImFont::AddRemapChar
            , py::arg("from_codepoint")
            , py::arg("to_codepoint")
            , py::return_value_policy::automatic_reference)
        .def("is_glyph_range_unused", &ImFont::IsGlyphRangeUnused
            , py::arg("c_begin")
            , py::arg("c_last")
            , py::return_value_policy::automatic_reference)
    ;

    py::enum_<ImGuiViewportFlags_>(_imgui, "ViewportFlags", py::arithmetic())
        .value("NONE", ImGuiViewportFlags_::ImGuiViewportFlags_None)
        .value("IS_PLATFORM_WINDOW", ImGuiViewportFlags_::ImGuiViewportFlags_IsPlatformWindow)
        .value("IS_PLATFORM_MONITOR", ImGuiViewportFlags_::ImGuiViewportFlags_IsPlatformMonitor)
        .value("OWNED_BY_APP", ImGuiViewportFlags_::ImGuiViewportFlags_OwnedByApp)
        .value("NO_DECORATION", ImGuiViewportFlags_::ImGuiViewportFlags_NoDecoration)
        .value("NO_TASK_BAR_ICON", ImGuiViewportFlags_::ImGuiViewportFlags_NoTaskBarIcon)
        .value("NO_FOCUS_ON_APPEARING", ImGuiViewportFlags_::ImGuiViewportFlags_NoFocusOnAppearing)
        .value("NO_FOCUS_ON_CLICK", ImGuiViewportFlags_::ImGuiViewportFlags_NoFocusOnClick)
        .value("NO_INPUTS", ImGuiViewportFlags_::ImGuiViewportFlags_NoInputs)
        .value("NO_RENDERER_CLEAR", ImGuiViewportFlags_::ImGuiViewportFlags_NoRendererClear)
        .value("NO_AUTO_MERGE", ImGuiViewportFlags_::ImGuiViewportFlags_NoAutoMerge)
        .value("TOP_MOST", ImGuiViewportFlags_::ImGuiViewportFlags_TopMost)
        .value("CAN_HOST_OTHER_WINDOWS", ImGuiViewportFlags_::ImGuiViewportFlags_CanHostOtherWindows)
        .value("IS_MINIMIZED", ImGuiViewportFlags_::ImGuiViewportFlags_IsMinimized)
        .value("IS_FOCUSED", ImGuiViewportFlags_::ImGuiViewportFlags_IsFocused)
        .export_values()
    ;
    py::class_<ImGuiViewport> _Viewport(_imgui, "Viewport");
    registry.on(_imgui, "Viewport", _Viewport);
        _Viewport
        .def_readwrite("id", &ImGuiViewport::ID)
        .def_readwrite("flags", &ImGuiViewport::Flags)
        .def_readwrite("pos", &ImGuiViewport::Pos)
        .def_readwrite("size", &ImGuiViewport::Size)
        .def_readwrite("framebuffer_scale", &ImGuiViewport::FramebufferScale)
        .def_readwrite("work_pos", &ImGuiViewport::WorkPos)
        .def_readwrite("work_size", &ImGuiViewport::WorkSize)
        .def_readwrite("dpi_scale", &ImGuiViewport::DpiScale)
        .def_readwrite("parent_viewport_id", &ImGuiViewport::ParentViewportId)
        .def_readwrite("draw_data", &ImGuiViewport::DrawData)
        .def_readwrite("renderer_user_data", &ImGuiViewport::RendererUserData)
        .def_readwrite("platform_user_data", &ImGuiViewport::PlatformUserData)
        .def_readwrite("platform_handle", &ImGuiViewport::PlatformHandle)
        .def_readwrite("platform_handle_raw", &ImGuiViewport::PlatformHandleRaw)
        .def_readwrite("platform_window_created", &ImGuiViewport::PlatformWindowCreated)
        .def_readwrite("platform_request_move", &ImGuiViewport::PlatformRequestMove)
        .def_readwrite("platform_request_resize", &ImGuiViewport::PlatformRequestResize)
        .def_readwrite("platform_request_close", &ImGuiViewport::PlatformRequestClose)
        .def(py::init<>())
        .def("get_center", &ImGuiViewport::GetCenter
            , py::return_value_policy::automatic_reference)
        .def("get_work_center", &ImGuiViewport::GetWorkCenter
            , py::return_value_policy::automatic_reference)
    ;

    py::class_<ImGuiPlatformImeData> _PlatformImeData(_imgui, "PlatformImeData");
    registry.on(_imgui, "PlatformImeData", _PlatformImeData);
        _PlatformImeData
        .def_readwrite("want_visible", &ImGuiPlatformImeData::WantVisible)
        .def_readwrite("want_text_input", &ImGuiPlatformImeData::WantTextInput)
        .def_readwrite("input_pos", &ImGuiPlatformImeData::InputPos)
        .def_readwrite("input_line_height", &ImGuiPlatformImeData::InputLineHeight)
        .def_readwrite("viewport_id", &ImGuiPlatformImeData::ViewportId)
        .def(py::init<>())
    ;


}