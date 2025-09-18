#include <limits>
#include <filesystem>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#include "implot.h"
#include "implot_internal.h"

#include <crunge/imgui/crunge-imgui.h>
#include <crunge/imgui/conversions.h>
#include <cxbind/cxbind.h>

namespace py = pybind11;

//TODO:Why did I have to put this here?  Getting an external reference error
char ImGuiTextBuffer::EmptyString[1] = { 0 };

void init_main(py::module &_implot, Registry &registry) {

    //template <typename T> IMPLOT_API void PlotLine(const char* label_id, const T* values, int count, double xscale=1, double x0=0, int offset=0, int stride=sizeof(T));
    _implot.def("plot_line", [](const char* label_id, const py::array_t<double>& values, int count)
    {
        ImPlot::PlotLine<double>(label_id, (double*)values.unchecked().data(), count);
    }
    , py::arg("label_id")
    , py::arg("values")
    , py::arg("count")
    , py::return_value_policy::automatic_reference);

    //template IMPLOT_API void PlotLine<double>(const char* label_id, const double* xs, const double* ys, int count, int offset, int stride);
    _implot.def("plot_line", [](const char* label_id, const py::array_t<double>& xs, const py::array_t<double>& ys, int count)
    {
        ImPlot::PlotLine<double>(label_id, (double*)xs.unchecked().data(), (double*)ys.unchecked().data(), count);
    }
    , py::arg("label_id")
    , py::arg("xs")
    , py::arg("ys")
    , py::arg("count")
    , py::return_value_policy::automatic_reference);

    //template <typename T> IMPLOT_API  void PlotScatter(const char* label_id, const T* values, int count, double xscale=1, double x0=0, int offset=0, int stride=sizeof(T));
    _implot.def("plot_scatter", [](const char* label_id, const py::array_t<double>& values, int count)
    {
        ImPlot::PlotScatter<double>(label_id, (double*)values.unchecked().data(), count);
    }
    , py::arg("label_id")
    , py::arg("values")
    , py::arg("count")
    , py::return_value_policy::automatic_reference);

    //template <typename T> IMPLOT_API void PlotShaded(const char* label_id, const T* values, int count, double y_ref=0, double xscale=1, double x0=0, int offset=0, int stride=sizeof(T));
    _implot.def("plot_shaded", [](const char* label_id, const py::array_t<double>& values, int count)
    {
        ImPlot::PlotShaded<double>(label_id, (double*)values.unchecked().data(), count);
    }
    , py::arg("label_id")
    , py::arg("values")
    , py::arg("count")
    , py::return_value_policy::automatic_reference);

    //template <typename T> IMPLOT_API void PlotBars(const char* label_id, const T* values, int count, double width=0.67, double shift=0, int offset=0, int stride=sizeof(T));
    _implot.def("plot_bars", [](const char* label_id, const py::array_t<double>& values, int count)
    {
        ImPlot::PlotBars<double>(label_id, (double*)values.unchecked().data(), count);
    }
    , py::arg("label_id")
    , py::arg("values")
    , py::arg("count")
    , py::return_value_policy::automatic_reference);

    //template <typename T> IMPLOT_API void PlotBarsH(const char* label_id, const T* values, int count, double height=0.67, double shift=0, int offset=0, int stride=sizeof(T));
    _implot.def("plot_bars_h", [](const char* label_id, const py::array_t<double>& values, int count)
    {
        ImPlot::PlotBars<double>(label_id, (double*)values.unchecked().data(), count, 0.67, 0, ImPlotBarsFlags_Horizontal);
    }
    , py::arg("label_id")
    , py::arg("values")
    , py::arg("count")
    , py::return_value_policy::automatic_reference);

    //template <typename T> IMPLOT_API void PlotErrorBars(const char* label_id, const T* xs, const T* ys, const T* err, int count, int offset=0, int stride=sizeof(T));
    /* TODO: Put this one off until I understand it!
    _implot.def("plot_error_bars", [](const char* label_id, const py::array_t<double>& xs, const py::array_t<double>& ys, const py::array_t<double>& err int count)
    {
        ImPlot::PlotErrorBars<double>(label_id, (double*)xs.unchecked().data(), (double*)ys.unchecked().data(), (double*)err.unchecked().data(), count);
    }
    , py::arg("label_id")
    , py::arg("values")
    , py::arg("count")
    , py::return_value_policy::automatic_reference);
    */
}

