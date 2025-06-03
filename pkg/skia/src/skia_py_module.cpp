#include <pybind11/pybind11.h>

#include <cxbind/cxbind.h>

namespace py = pybind11;

void init_main(py::module &, Registry &registry);
void init_skia_shader_py(py::module &, Registry &registry);
void init_skia_graphite_types_py_auto(py::module &, Registry &registry);
void init_skia_clip_op_py_auto(py::module &, Registry &registry);
void init_skia_rect_py_auto(py::module &, Registry &registry);
void init_skia_rect_py(py::module &, Registry &registry);
void init_skia_size_py_auto(py::module &, Registry &registry);
void init_skia_blend_mode_py_auto(py::module &, Registry &registry);
void init_skia_tile_mode_py_auto(py::module &, Registry &registry);
void init_skia_context_py_auto(py::module &, Registry &registry);
void init_skia_context_py(py::module &, Registry &registry);
void init_skia_font_types_py_auto(py::module &, Registry &registry);

void init_skia_canvas_py(py::module &, Registry &registry);
void init_skia_canvas_py_auto(py::module &, Registry &registry);

void init_skia_surface_py_auto(py::module &, Registry &registry);
void init_skia_surface_py(py::module &, Registry &registry);

void init_skia_recorder_py_auto(py::module &, Registry &registry);
void init_skia_recording_py_auto(py::module &, Registry &registry);

void init_skia_paint_py(py::module &, Registry &registry);
void init_skia_paint_py_auto(py::module &, Registry &registry);

void init_skia_color_py(py::module &, Registry &registry);
void init_skia_color_py_auto(py::module &, Registry &registry);

void init_skia_alpha_type_py_auto(py::module &, Registry &registry);
void init_skia_color_type_py_auto(py::module &, Registry &registry);

void init_skia_font_py(py::module &, Registry &registry);
void init_skia_font_py_auto(py::module &, Registry &registry);

void init_skia_matrix_py_auto(py::module &, Registry &registry);

void init_skia_image_filter_py_auto(py::module &, Registry &registry);

void init_skia_point_py(py::module &, Registry &registry);
void init_skia_point_py_auto(py::module &, Registry &registry);

void init_skia_gradient_shader_py(py::module &, Registry &registry);
void init_skia_gradient_shader_py_auto(py::module &, Registry &registry);

void init_skia_perlin_noise_shader_py(py::module &, Registry &registry);

void init_skia_image_filters_py_auto(py::module &, Registry &registry);

void init_skia_text_blob_py_auto(py::module &, Registry &registry);

void init_skia_data_py_auto(py::module &, Registry &registry);
void init_skia_sampling_options_py_auto(py::module &, Registry &registry);
void init_skia_image_info_py_auto(py::module &, Registry &registry);
void init_skia_image_py_auto(py::module &, Registry &registry);

void init_skia_standard_recorder_options_py(py::module &, Registry &registry);

void init_skia_path_py_auto(py::module &, Registry &registry);
// NOTE: initialization/binding order does matter!
// This popped up using default arguments that use structure constructors

PYBIND11_MODULE(_skia, m)
{
    Registry r;
    init_main(m, r);
    init_skia_shader_py(m, r);
    init_skia_graphite_types_py_auto(m, r);
    init_skia_clip_op_py_auto(m, r);

    init_skia_rect_py(m, r);
    init_skia_rect_py_auto(m, r);

    init_skia_size_py_auto(m, r);

    init_skia_blend_mode_py_auto(m, r);
    init_skia_tile_mode_py_auto(m, r);

    init_skia_recorder_py_auto(m, r);
    init_skia_recording_py_auto(m, r);

    init_skia_context_py_auto(m, r);
    init_skia_context_py(m, r);

    init_skia_font_types_py_auto(m, r);

    init_skia_canvas_py(m, r);
    init_skia_canvas_py_auto(m, r);

    init_skia_surface_py(m, r);
    init_skia_surface_py_auto(m, r);

    init_skia_paint_py(m, r);
    init_skia_paint_py_auto(m, r);

    init_skia_color_py(m, r);
    init_skia_color_py_auto(m, r);

    init_skia_alpha_type_py_auto(m, r);
    init_skia_color_type_py_auto(m, r);

    init_skia_point_py(m, r);
    init_skia_point_py_auto(m, r);

    init_skia_matrix_py_auto(m, r);

    init_skia_image_filter_py_auto(m, r);

    init_skia_gradient_shader_py(m, r);
    init_skia_gradient_shader_py_auto(m, r);

    init_skia_perlin_noise_shader_py(m, r);

    init_skia_image_filters_py_auto(m, r);

    init_skia_font_py(m, r);
    init_skia_font_py_auto(m, r);

    init_skia_text_blob_py_auto(m, r);

    init_skia_data_py_auto(m, r);
    init_skia_sampling_options_py_auto(m, r);
    init_skia_image_info_py_auto(m, r);
    init_skia_image_py_auto(m, r);

    init_skia_standard_recorder_options_py(m, r);

    init_skia_path_py_auto(m, r);
}