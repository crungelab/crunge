#include <limits>
#include <filesystem>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>
#include <pybind11/numpy.h>

#define BUILDING_DLL

#include "imgui.h"
#include "imgui_internal.h"

#include <cxbind/cxbind.h>

#include <crunge/imgui/crunge-imgui.h>
#include <crunge/imgui/conversions.h>

namespace py = pybind11;

/*thread_local ImGuiContext* TImGui;
ImGuiContext* GetGImGui() {
  return TImGui;
}*/
ImGuiContext* TImGui;  // Current implicit context pointer

PYBIND11_MAKE_OPAQUE(std::vector<ImWchar>);
//PYBIND11_MAKE_OPAQUE(std::vector<ImDrawCmd>);
//PYBIND11_MAKE_OPAQUE(std::vector<ImDrawVert>);
//PYBIND11_MAKE_OPAQUE(std::vector<ImFontGlyph>);

void init_imgui_py(py::module &_imgui, Registry &registry) {
    py::bind_vector<std::vector<ImWchar>>(_imgui, "GlyphRanges", "ImGui Glyph Range Vector");

    template_ImVector<char>(_imgui, "Vector_char");
    template_ImVector<float>(_imgui, "Vector_float");
    template_ImVector<unsigned char>(_imgui, "Vector_unsignedchar");
    template_ImVector<unsigned short>(_imgui, "Vector_unsignedshort");
    template_ImVector<ImDrawCmd>(_imgui, "Vector_DrawCmd");
    template_ImVector<ImDrawVert>(_imgui, "Vector_DrawVert");
    template_ImVector<ImFontGlyph>(_imgui, "Vector_FontGlyph");
    template_ImVector<ImTextureData*>(_imgui, "Vector_TextureData");

    //bool ImGui::SetDragDropPayload(const char* type, const void* data, size_t data_size, ImGuiCond cond)
    _imgui.def("set_drag_drop_payload", [](std::string type, std::string data, ImGuiCond cond)
    {
        return ImGui::SetDragDropPayload(type.c_str(), data.c_str(), data.length(), cond);
    }
    , py::arg("type")
    , py::arg("data")
    , py::arg("cond") = 0
    , py::return_value_policy::automatic_reference);

    _imgui.def("get_vertex_buffer_vertex_pos_offset", []()
    {
        return offsetof(ImDrawVert, pos);
    }
    , py::return_value_policy::automatic_reference);
    _imgui.def("get_vertex_buffer_vertex_uv_offset", []()
    {
        return offsetof(ImDrawVert, uv);
    }
    , py::return_value_policy::automatic_reference);
    _imgui.def("get_vertex_buffer_vertex_col_offset", []()
    {
        return offsetof(ImDrawVert, col);
    }
    , py::return_value_policy::automatic_reference);
    _imgui.def("get_vertex_buffer_vertex_size", []()
    {
        return AimDrawList::VERTEX_SIZE;
    }
    , py::return_value_policy::automatic_reference);
    _imgui.def("get_index_buffer_index_size", []() {
        return AimDrawList::INDEX_SIZE;
    }
    , py::return_value_policy::automatic_reference);


    PYEXTEND_BEGIN(ImGuiStyle, Style)
    _Style.def_property_readonly("colors", [](const ImGuiStyle &self) {
        auto colors = self.Colors;
        auto result = PyList_New(ImGuiCol_COUNT);
        for(int i = 0; i < ImGuiCol_COUNT; ++i ) {
            ImVec4 color = colors[i];
            auto item = PyTuple_New(4);
            PyTuple_SetItem(item, 0, PyFloat_FromDouble(color.x));
            PyTuple_SetItem(item, 1, PyFloat_FromDouble(color.y));
            PyTuple_SetItem(item, 2, PyFloat_FromDouble(color.z));
            PyTuple_SetItem(item, 3, PyFloat_FromDouble(color.w));
            PyList_SetItem(result, i, item);
        }
        return py::reinterpret_steal<py::list>(result);
    });
    _Style.def("set_color", [](ImGuiStyle& self, int item, ImVec4 color)
    {
        if (item < 0) throw py::index_error();
        if (item >= IM_ARRAYSIZE(self.Colors)) throw py::index_error();
        self.Colors[item] = color;
    }, py::arg("item"), py::arg("color"));
    PYEXTEND_END

    PYEXTEND_BEGIN(ImGuiIO, IO)
    _IO.def("set_mouse_down", [](ImGuiIO& self, int button, bool down)
    {
        if (button < 0) throw py::index_error();
        if (button >= IM_ARRAYSIZE(self.MouseDown)) throw py::index_error();
        self.MouseDown[button] = down;
    }, py::arg("button"), py::arg("down"));
    PYEXTEND_END

    PYEXTEND_BEGIN(ImDrawCmd, DrawCmd)
    _DrawCmd.def_property_readonly("texture_id", [](const ImDrawCmd& self) {
        return self.GetTexID();
    });
    PYEXTEND_END

    /*
    PYEXTEND_BEGIN(ImDrawCmd, DrawCmd)
    DrawCmd.def_property("user_callback",
        [](const ImDrawCmd& self) {
            if(self.UserCallback.ptr() == nullptr) {
                return py::cast<py::object>(Py_None);
            } else {
                return py::object(self.UserCallback);
            }
        },
        [](ImDrawCmd& self, ImDrawCallback cb) {
            self.UserCallback = cb;
        }
    );
    PYEXTEND_END
    */

    PYEXTEND_BEGIN(ImDrawList, DrawList)

    _DrawList.def("add_callback", 
    [](ImDrawList &self ,ImDrawCallback callback, py::object callback_data) {
        return self.AddCallback(callback, callback_data.ptr());
    }
    , py::arg("callback")
    , py::arg("callback_data")
    , py::return_value_policy::automatic_reference);


    _DrawList.def_property_readonly("cmd_buffer_size",
        [](const ImDrawList &dl) {
            auto result = PyLong_FromLong(dl.CmdBuffer.Size);
            return py::reinterpret_steal<py::object>(result);
        }
    );

    _DrawList.def_property_readonly("cmd_buffer_data",
        [](const ImDrawList &dl) {
            auto result = PyMemoryView_FromMemory((char*)dl.CmdBuffer.Data, dl.CmdBuffer.Size*AimDrawList::COMMAND_SIZE, PyBUF_WRITE);
            return py::reinterpret_steal<py::object>(result);
        }
    );

    _DrawList.def_property_readonly("vtx_buffer_size",
        [](const ImDrawList &dl) {
            auto result = PyLong_FromLong(dl.VtxBuffer.Size);
            return py::reinterpret_steal<py::object>(result);
        }
    );

    _DrawList.def_property_readonly("vtx_buffer_data",
        [](const ImDrawList &dl) {
            auto result = PyMemoryView_FromMemory((char*)dl.VtxBuffer.Data, dl.VtxBuffer.Size*AimDrawList::VERTEX_SIZE, PyBUF_WRITE);
            return py::reinterpret_steal<py::object>(result);
        }
    );

    _DrawList.def_property_readonly("idx_buffer_size",
        [](const ImDrawList &dl) {
            auto result = PyLong_FromLong(dl.IdxBuffer.Size);
            return py::reinterpret_steal<py::object>(result);
        }
    );

    _DrawList.def_property_readonly("idx_buffer_data",
        [](const ImDrawList &dl) {
            auto result = PyMemoryView_FromMemory((char*)dl.IdxBuffer.Data, dl.IdxBuffer.Size*AimDrawList::INDEX_SIZE, PyBUF_WRITE);
            return py::reinterpret_steal<py::object>(result);
        }
    );

    _DrawList.def("__iter__", 
        [](const ImDrawList &dl) { return py::make_iterator(dl.CmdBuffer.Data, dl.CmdBuffer.Data + dl.CmdBuffer.Size); },
        py::keep_alive<0, 1>() /* Essential: keep object alive while iterator exists */);

    //void ImDrawList::AddPolyline(const ImVec2* points, const int points_count, ImU32 col, bool closed, float thickness)
    _DrawList.def("add_polyline",  [](ImDrawList& self, py::list points, ImU32 col, bool closed, float thickness)
    {
        const int points_count = points.size();
        ImVec2 *pts = (ImVec2*)malloc(points_count * sizeof(ImVec2));
        for(int i = 0; i < points_count; ++i) {
            py::object obj = points[i];
            pts[i] = obj.cast<ImVec2>();
        }
        self.AddPolyline(pts, points_count, col, closed, thickness);
        free(pts);
    }
    , py::arg("points")
    , py::arg("col")
    , py::arg("closed")
    , py::arg("thickness")
    , py::return_value_policy::automatic_reference);

    PYEXTEND_END

    PYEXTEND_BEGIN(ImDrawData, DrawData)
    _DrawData.def_property_readonly("cmd_lists", [](const ImDrawData& self)
    {
        py::list ret;
        for(int i = 0; i < self.CmdListsCount; i++)
        {
            ret.append(self.CmdLists[i]);
        }
        return ret;
    });
    PYEXTEND_END

    PYEXTEND_BEGIN(ImDrawVert, DrawVert)
    _DrawVert.def_property_readonly_static("pos_offset", [](py::object)
    {
        return offsetof(ImDrawVert, pos);
    });
    _DrawVert.def_property_readonly_static("uv_offset", [](py::object)
    {
        return offsetof(ImDrawVert, uv);
    });
    _DrawVert.def_property_readonly_static("col_offset", [](py::object)
    {
        return offsetof(ImDrawVert, col);
    });
    PYEXTEND_END

    PYEXTEND_BEGIN(ImFontAtlas, FontAtlas)
    _FontAtlas.def("add_font_from_file_ttf", [](ImFontAtlas& self, const std::string& filename, float size_pixels, const ImFontConfig* font_cfg_template, const std::vector<ImWchar>& glyph_ranges)
    {
        const ImWchar* glyph_ranges_ptr = glyph_ranges.empty() ? nullptr : glyph_ranges.data();
        return self.AddFontFromFileTTF(filename.c_str(), size_pixels, font_cfg_template, glyph_ranges_ptr);
    }
    , py::arg("filename")
    , py::arg("size_pixels")
    , py::arg("font_cfg") = nullptr
    , py::arg("glyph_ranges") = std::vector<ImWchar>()  // Default empty vector
    , py::return_value_policy::automatic_reference);
    PYEXTEND_END

    PYEXTEND_BEGIN(ImTextureData, TextureData)
    _TextureData.def_property_readonly("pixels", [](ImTextureData& t) -> py::object {
        if (!t.Pixels || t.Width <= 0 || t.Height <= 0 || t.BytesPerPixel <= 0)
            return py::none();
        const ssize_t size = (ssize_t)t.Width * t.Height * t.BytesPerPixel;
        // 1-D view is fine for upload; if you prefer HWC strides, use from_buffer(...)
        return py::memoryview::from_memory((void*)t.Pixels, size, /*readonly=*/true);
    });
    PYEXTEND_END

    PYEXTEND_BEGIN(ImTextureRef, TextureRef)
    _TextureRef.def_property_readonly("texture_id", [](ImTextureRef& t) {
        return t.GetTexID();
    });
    PYEXTEND_END

    _imgui.def("input_text", [](const char* label, char* data, size_t max_size, ImGuiInputTextFlags flags)
    {
        max_size++;
        char* text = (char*)malloc(max_size * sizeof(char));
        strncpy(text, data, max_size);
        auto ret = ImGui::InputText(label, text, max_size, flags, nullptr, NULL);
        std::string output(text);
        free(text);
        return std::make_tuple(ret, output);
    }
    , py::arg("label")
    , py::arg("data")
    , py::arg("max_size")
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);

    _imgui.def("input_text_multiline", [](const char* label, char* data, size_t max_size, const ImVec2& size, ImGuiInputTextFlags flags)
    {
        max_size++;
        char* text = (char*)malloc(max_size * sizeof(char));
        strncpy(text, data, max_size);
        auto ret = ImGui::InputTextMultiline(label, text, max_size, size, flags, nullptr, NULL);
        std::string output(text);
        free(text);
        return std::make_tuple(ret, output);
    }
    , py::arg("label")
    , py::arg("data")
    , py::arg("max_size")
    , py::arg("size") = ImVec2(0,0)
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);

    _imgui.def("menu_item", [](const char * label, const char * shortcut, bool * p_selected, bool enabled)
    {
        auto ret = ImGui::MenuItem(label, shortcut, p_selected, enabled);
        return std::make_tuple(ret, p_selected);
    }
    , py::arg("label")
    , py::arg("shortcut")
    , py::arg("p_selected")
    , py::arg("enabled") = true
    , py::return_value_policy::automatic_reference);

    _imgui.def("combo", [](const char* label, int * current_item, std::vector<std::string> items, int popup_max_height_in_items)
    {
        std::vector<const char*> ptrs;
        for (const std::string& s : items)
        {
            ptrs.push_back(s.c_str());
        }
        auto ret = ImGui::Combo(label, current_item, ptrs.data(), ptrs.size(), popup_max_height_in_items);
        return std::make_tuple(ret, current_item);
    }
    , py::arg("label")
    , py::arg("current_item")
    , py::arg("items")
    , py::arg("popup_max_height_in_items") = -1
    , py::return_value_policy::automatic_reference);

    _imgui.def("selectable", [](const char * label, bool * p_selected, ImGuiSelectableFlags flags, const ImVec2 & size)
    {
        auto ret = ImGui::Selectable(label, p_selected, flags, size);
        return std::make_tuple(ret, p_selected);
    }
    , py::arg("label")
    , py::arg("p_selected")
    , py::arg("flags") = 0
    , py::arg("size") = ImVec2(0,0)
    , py::return_value_policy::automatic_reference);

    _imgui.def("list_box", [](const char* label, int * current_item, std::vector<std::string> items, int height_in_items)
    {
        std::vector<const char*> ptrs;
        for (const std::string& s : items)
        {
            ptrs.push_back(s.c_str());
        }
        auto ret = ImGui::ListBox(label, current_item, ptrs.data(), ptrs.size(), height_in_items);
        return std::make_tuple(ret, current_item);
    }
    , py::arg("label")
    , py::arg("current_item")
    , py::arg("items")
    , py::arg("height_in_items") = -1
    , py::return_value_policy::automatic_reference);

    //
    // Collapsing Header
    //
    
    // Non-closeable
    _imgui.def(
        "collapsing_header",
        py::overload_cast<const char*, ImGuiTreeNodeFlags>(&ImGui::CollapsingHeader),
        py::arg("label"),
        py::kw_only(),
        py::arg("flags") = 0
    );

    // Closeable
    _imgui.def(
        "collapsing_header",
        [](const char* label, bool p_open, ImGuiTreeNodeFlags flags)
        {
            bool open = p_open;
            bool expanded = ImGui::CollapsingHeader(label, &open, flags);
            return py::make_tuple(expanded, open);
        },
        py::arg("label"),
        py::arg("p_open"),
        py::kw_only(),
        py::arg("flags") = 0
    );

    _imgui.def("plot_lines", [](const char* label, std::vector<float> values, int values_offset, const char* overlay_text, float scale_min, float scale_max, ImVec2 graph_size)
    {
        ImGui::PlotLines(label, values.data(), values.size(), values_offset, overlay_text, scale_min, scale_max, graph_size, sizeof(float));
    }
    , py::arg("label")
    , py::arg("values")
    , py::arg("values_offset") = 0
    , py::arg("overlay_text") = nullptr
    , py::arg("scale_min") = FLT_MAX
    , py::arg("scale_max") = FLT_MAX
    , py::arg("graph_size") = ImVec2(0,0)
    );

    _imgui.def("plot_histogram", [](const char* label, std::vector<float> values, int values_offset, const char* overlay_text, float scale_min, float scale_max, ImVec2 graph_size)
    {
        ImGui::PlotHistogram(label, values.data(), values.size(), values_offset, overlay_text, scale_min, scale_max, graph_size, sizeof(float));
    }
    , py::arg("label")
    , py::arg("values")
    , py::arg("values_offset") = 0
    , py::arg("overlay_text") = nullptr
    , py::arg("scale_min") = FLT_MAX
    , py::arg("scale_max") = FLT_MAX
    , py::arg("graph_size") = ImVec2(0,0)
    );
}

