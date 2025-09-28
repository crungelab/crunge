#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include "implot.h"
//#include "implot_internal.h"

#include <cxbind/cxbind.h>
#include <crunge/imgui/crunge-imgui.h>
#include <crunge/imgui/conversions.h>

namespace py = pybind11;

void init_generated(py::module &_implot, Registry &registry) {
    py::enum_<ImAxis_>(_implot, "Axis", py::arithmetic())
        .value("X1", ImAxis_::ImAxis_X1)
        .value("X2", ImAxis_::ImAxis_X2)
        .value("X3", ImAxis_::ImAxis_X3)
        .value("Y1", ImAxis_::ImAxis_Y1)
        .value("Y2", ImAxis_::ImAxis_Y2)
        .value("Y3", ImAxis_::ImAxis_Y3)
        .value("COUNT", ImAxis_::ImAxis_COUNT)
        .export_values()
    ;
    py::enum_<ImPlotFlags_>(_implot, "Flags", py::arithmetic())
        .value("NONE", ImPlotFlags_::ImPlotFlags_None)
        .value("NO_TITLE", ImPlotFlags_::ImPlotFlags_NoTitle)
        .value("NO_LEGEND", ImPlotFlags_::ImPlotFlags_NoLegend)
        .value("NO_MOUSE_TEXT", ImPlotFlags_::ImPlotFlags_NoMouseText)
        .value("NO_INPUTS", ImPlotFlags_::ImPlotFlags_NoInputs)
        .value("NO_MENUS", ImPlotFlags_::ImPlotFlags_NoMenus)
        .value("NO_BOX_SELECT", ImPlotFlags_::ImPlotFlags_NoBoxSelect)
        .value("NO_FRAME", ImPlotFlags_::ImPlotFlags_NoFrame)
        .value("EQUAL", ImPlotFlags_::ImPlotFlags_Equal)
        .value("CROSSHAIRS", ImPlotFlags_::ImPlotFlags_Crosshairs)
        .value("CANVAS_ONLY", ImPlotFlags_::ImPlotFlags_CanvasOnly)
        .export_values()
    ;
    py::enum_<ImPlotAxisFlags_>(_implot, "AxisFlags", py::arithmetic())
        .value("NONE", ImPlotAxisFlags_::ImPlotAxisFlags_None)
        .value("NO_LABEL", ImPlotAxisFlags_::ImPlotAxisFlags_NoLabel)
        .value("NO_GRID_LINES", ImPlotAxisFlags_::ImPlotAxisFlags_NoGridLines)
        .value("NO_TICK_MARKS", ImPlotAxisFlags_::ImPlotAxisFlags_NoTickMarks)
        .value("NO_TICK_LABELS", ImPlotAxisFlags_::ImPlotAxisFlags_NoTickLabels)
        .value("NO_INITIAL_FIT", ImPlotAxisFlags_::ImPlotAxisFlags_NoInitialFit)
        .value("NO_MENUS", ImPlotAxisFlags_::ImPlotAxisFlags_NoMenus)
        .value("NO_SIDE_SWITCH", ImPlotAxisFlags_::ImPlotAxisFlags_NoSideSwitch)
        .value("NO_HIGHLIGHT", ImPlotAxisFlags_::ImPlotAxisFlags_NoHighlight)
        .value("OPPOSITE", ImPlotAxisFlags_::ImPlotAxisFlags_Opposite)
        .value("FOREGROUND", ImPlotAxisFlags_::ImPlotAxisFlags_Foreground)
        .value("INVERT", ImPlotAxisFlags_::ImPlotAxisFlags_Invert)
        .value("AUTO_FIT", ImPlotAxisFlags_::ImPlotAxisFlags_AutoFit)
        .value("RANGE_FIT", ImPlotAxisFlags_::ImPlotAxisFlags_RangeFit)
        .value("PAN_STRETCH", ImPlotAxisFlags_::ImPlotAxisFlags_PanStretch)
        .value("LOCK_MIN", ImPlotAxisFlags_::ImPlotAxisFlags_LockMin)
        .value("LOCK_MAX", ImPlotAxisFlags_::ImPlotAxisFlags_LockMax)
        .value("LOCK", ImPlotAxisFlags_::ImPlotAxisFlags_Lock)
        .value("NO_DECORATIONS", ImPlotAxisFlags_::ImPlotAxisFlags_NoDecorations)
        .value("AUX_DEFAULT", ImPlotAxisFlags_::ImPlotAxisFlags_AuxDefault)
        .export_values()
    ;
    py::enum_<ImPlotSubplotFlags_>(_implot, "SubplotFlags", py::arithmetic())
        .value("NONE", ImPlotSubplotFlags_::ImPlotSubplotFlags_None)
        .value("NO_TITLE", ImPlotSubplotFlags_::ImPlotSubplotFlags_NoTitle)
        .value("NO_LEGEND", ImPlotSubplotFlags_::ImPlotSubplotFlags_NoLegend)
        .value("NO_MENUS", ImPlotSubplotFlags_::ImPlotSubplotFlags_NoMenus)
        .value("NO_RESIZE", ImPlotSubplotFlags_::ImPlotSubplotFlags_NoResize)
        .value("NO_ALIGN", ImPlotSubplotFlags_::ImPlotSubplotFlags_NoAlign)
        .value("SHARE_ITEMS", ImPlotSubplotFlags_::ImPlotSubplotFlags_ShareItems)
        .value("LINK_ROWS", ImPlotSubplotFlags_::ImPlotSubplotFlags_LinkRows)
        .value("LINK_COLS", ImPlotSubplotFlags_::ImPlotSubplotFlags_LinkCols)
        .value("LINK_ALL_X", ImPlotSubplotFlags_::ImPlotSubplotFlags_LinkAllX)
        .value("LINK_ALL_Y", ImPlotSubplotFlags_::ImPlotSubplotFlags_LinkAllY)
        .value("COL_MAJOR", ImPlotSubplotFlags_::ImPlotSubplotFlags_ColMajor)
        .export_values()
    ;
    py::enum_<ImPlotLegendFlags_>(_implot, "LegendFlags", py::arithmetic())
        .value("NONE", ImPlotLegendFlags_::ImPlotLegendFlags_None)
        .value("NO_BUTTONS", ImPlotLegendFlags_::ImPlotLegendFlags_NoButtons)
        .value("NO_HIGHLIGHT_ITEM", ImPlotLegendFlags_::ImPlotLegendFlags_NoHighlightItem)
        .value("NO_HIGHLIGHT_AXIS", ImPlotLegendFlags_::ImPlotLegendFlags_NoHighlightAxis)
        .value("NO_MENUS", ImPlotLegendFlags_::ImPlotLegendFlags_NoMenus)
        .value("OUTSIDE", ImPlotLegendFlags_::ImPlotLegendFlags_Outside)
        .value("HORIZONTAL", ImPlotLegendFlags_::ImPlotLegendFlags_Horizontal)
        .value("SORT", ImPlotLegendFlags_::ImPlotLegendFlags_Sort)
        .export_values()
    ;
    py::enum_<ImPlotMouseTextFlags_>(_implot, "MouseTextFlags", py::arithmetic())
        .value("NONE", ImPlotMouseTextFlags_::ImPlotMouseTextFlags_None)
        .value("NO_AUX_AXES", ImPlotMouseTextFlags_::ImPlotMouseTextFlags_NoAuxAxes)
        .value("NO_FORMAT", ImPlotMouseTextFlags_::ImPlotMouseTextFlags_NoFormat)
        .value("SHOW_ALWAYS", ImPlotMouseTextFlags_::ImPlotMouseTextFlags_ShowAlways)
        .export_values()
    ;
    py::enum_<ImPlotDragToolFlags_>(_implot, "DragToolFlags", py::arithmetic())
        .value("NONE", ImPlotDragToolFlags_::ImPlotDragToolFlags_None)
        .value("NO_CURSORS", ImPlotDragToolFlags_::ImPlotDragToolFlags_NoCursors)
        .value("NO_FIT", ImPlotDragToolFlags_::ImPlotDragToolFlags_NoFit)
        .value("NO_INPUTS", ImPlotDragToolFlags_::ImPlotDragToolFlags_NoInputs)
        .value("DELAYED", ImPlotDragToolFlags_::ImPlotDragToolFlags_Delayed)
        .export_values()
    ;
    py::enum_<ImPlotColormapScaleFlags_>(_implot, "ColormapScaleFlags", py::arithmetic())
        .value("NONE", ImPlotColormapScaleFlags_::ImPlotColormapScaleFlags_None)
        .value("NO_LABEL", ImPlotColormapScaleFlags_::ImPlotColormapScaleFlags_NoLabel)
        .value("OPPOSITE", ImPlotColormapScaleFlags_::ImPlotColormapScaleFlags_Opposite)
        .value("INVERT", ImPlotColormapScaleFlags_::ImPlotColormapScaleFlags_Invert)
        .export_values()
    ;
    py::enum_<ImPlotItemFlags_>(_implot, "ItemFlags", py::arithmetic())
        .value("NONE", ImPlotItemFlags_::ImPlotItemFlags_None)
        .value("NO_LEGEND", ImPlotItemFlags_::ImPlotItemFlags_NoLegend)
        .value("NO_FIT", ImPlotItemFlags_::ImPlotItemFlags_NoFit)
        .export_values()
    ;
    py::enum_<ImPlotLineFlags_>(_implot, "LineFlags", py::arithmetic())
        .value("NONE", ImPlotLineFlags_::ImPlotLineFlags_None)
        .value("SEGMENTS", ImPlotLineFlags_::ImPlotLineFlags_Segments)
        .value("LOOP", ImPlotLineFlags_::ImPlotLineFlags_Loop)
        .value("SKIP_NA_N", ImPlotLineFlags_::ImPlotLineFlags_SkipNaN)
        .value("NO_CLIP", ImPlotLineFlags_::ImPlotLineFlags_NoClip)
        .value("SHADED", ImPlotLineFlags_::ImPlotLineFlags_Shaded)
        .export_values()
    ;
    py::enum_<ImPlotScatterFlags_>(_implot, "ScatterFlags", py::arithmetic())
        .value("NONE", ImPlotScatterFlags_::ImPlotScatterFlags_None)
        .value("NO_CLIP", ImPlotScatterFlags_::ImPlotScatterFlags_NoClip)
        .export_values()
    ;
    py::enum_<ImPlotStairsFlags_>(_implot, "StairsFlags", py::arithmetic())
        .value("NONE", ImPlotStairsFlags_::ImPlotStairsFlags_None)
        .value("PRE_STEP", ImPlotStairsFlags_::ImPlotStairsFlags_PreStep)
        .value("SHADED", ImPlotStairsFlags_::ImPlotStairsFlags_Shaded)
        .export_values()
    ;
    py::enum_<ImPlotShadedFlags_>(_implot, "ShadedFlags", py::arithmetic())
        .value("NONE", ImPlotShadedFlags_::ImPlotShadedFlags_None)
        .export_values()
    ;
    py::enum_<ImPlotBarsFlags_>(_implot, "BarsFlags", py::arithmetic())
        .value("NONE", ImPlotBarsFlags_::ImPlotBarsFlags_None)
        .value("HORIZONTAL", ImPlotBarsFlags_::ImPlotBarsFlags_Horizontal)
        .export_values()
    ;
    py::enum_<ImPlotBarGroupsFlags_>(_implot, "BarGroupsFlags", py::arithmetic())
        .value("NONE", ImPlotBarGroupsFlags_::ImPlotBarGroupsFlags_None)
        .value("HORIZONTAL", ImPlotBarGroupsFlags_::ImPlotBarGroupsFlags_Horizontal)
        .value("STACKED", ImPlotBarGroupsFlags_::ImPlotBarGroupsFlags_Stacked)
        .export_values()
    ;
    py::enum_<ImPlotErrorBarsFlags_>(_implot, "ErrorBarsFlags", py::arithmetic())
        .value("NONE", ImPlotErrorBarsFlags_::ImPlotErrorBarsFlags_None)
        .value("HORIZONTAL", ImPlotErrorBarsFlags_::ImPlotErrorBarsFlags_Horizontal)
        .export_values()
    ;
    py::enum_<ImPlotStemsFlags_>(_implot, "StemsFlags", py::arithmetic())
        .value("NONE", ImPlotStemsFlags_::ImPlotStemsFlags_None)
        .value("HORIZONTAL", ImPlotStemsFlags_::ImPlotStemsFlags_Horizontal)
        .export_values()
    ;
    py::enum_<ImPlotInfLinesFlags_>(_implot, "InfLinesFlags", py::arithmetic())
        .value("NONE", ImPlotInfLinesFlags_::ImPlotInfLinesFlags_None)
        .value("HORIZONTAL", ImPlotInfLinesFlags_::ImPlotInfLinesFlags_Horizontal)
        .export_values()
    ;
    py::enum_<ImPlotPieChartFlags_>(_implot, "PieChartFlags", py::arithmetic())
        .value("NONE", ImPlotPieChartFlags_::ImPlotPieChartFlags_None)
        .value("NORMALIZE", ImPlotPieChartFlags_::ImPlotPieChartFlags_Normalize)
        .value("IGNORE_HIDDEN", ImPlotPieChartFlags_::ImPlotPieChartFlags_IgnoreHidden)
        .value("EXPLODING", ImPlotPieChartFlags_::ImPlotPieChartFlags_Exploding)
        .export_values()
    ;
    py::enum_<ImPlotHeatmapFlags_>(_implot, "HeatmapFlags", py::arithmetic())
        .value("NONE", ImPlotHeatmapFlags_::ImPlotHeatmapFlags_None)
        .value("COL_MAJOR", ImPlotHeatmapFlags_::ImPlotHeatmapFlags_ColMajor)
        .export_values()
    ;
    py::enum_<ImPlotHistogramFlags_>(_implot, "HistogramFlags", py::arithmetic())
        .value("NONE", ImPlotHistogramFlags_::ImPlotHistogramFlags_None)
        .value("HORIZONTAL", ImPlotHistogramFlags_::ImPlotHistogramFlags_Horizontal)
        .value("CUMULATIVE", ImPlotHistogramFlags_::ImPlotHistogramFlags_Cumulative)
        .value("DENSITY", ImPlotHistogramFlags_::ImPlotHistogramFlags_Density)
        .value("NO_OUTLIERS", ImPlotHistogramFlags_::ImPlotHistogramFlags_NoOutliers)
        .value("COL_MAJOR", ImPlotHistogramFlags_::ImPlotHistogramFlags_ColMajor)
        .export_values()
    ;
    py::enum_<ImPlotDigitalFlags_>(_implot, "DigitalFlags", py::arithmetic())
        .value("NONE", ImPlotDigitalFlags_::ImPlotDigitalFlags_None)
        .export_values()
    ;
    py::enum_<ImPlotImageFlags_>(_implot, "ImageFlags", py::arithmetic())
        .value("NONE", ImPlotImageFlags_::ImPlotImageFlags_None)
        .export_values()
    ;
    py::enum_<ImPlotTextFlags_>(_implot, "TextFlags", py::arithmetic())
        .value("NONE", ImPlotTextFlags_::ImPlotTextFlags_None)
        .value("VERTICAL", ImPlotTextFlags_::ImPlotTextFlags_Vertical)
        .export_values()
    ;
    py::enum_<ImPlotDummyFlags_>(_implot, "DummyFlags", py::arithmetic())
        .value("NONE", ImPlotDummyFlags_::ImPlotDummyFlags_None)
        .export_values()
    ;
    py::enum_<ImPlotCond_>(_implot, "Cond", py::arithmetic())
        .value("NONE", ImPlotCond_::ImPlotCond_None)
        .value("ALWAYS", ImPlotCond_::ImPlotCond_Always)
        .value("ONCE", ImPlotCond_::ImPlotCond_Once)
        .export_values()
    ;
    py::enum_<ImPlotCol_>(_implot, "Col", py::arithmetic())
        .value("LINE", ImPlotCol_::ImPlotCol_Line)
        .value("FILL", ImPlotCol_::ImPlotCol_Fill)
        .value("MARKER_OUTLINE", ImPlotCol_::ImPlotCol_MarkerOutline)
        .value("MARKER_FILL", ImPlotCol_::ImPlotCol_MarkerFill)
        .value("ERROR_BAR", ImPlotCol_::ImPlotCol_ErrorBar)
        .value("FRAME_BG", ImPlotCol_::ImPlotCol_FrameBg)
        .value("PLOT_BG", ImPlotCol_::ImPlotCol_PlotBg)
        .value("PLOT_BORDER", ImPlotCol_::ImPlotCol_PlotBorder)
        .value("LEGEND_BG", ImPlotCol_::ImPlotCol_LegendBg)
        .value("LEGEND_BORDER", ImPlotCol_::ImPlotCol_LegendBorder)
        .value("LEGEND_TEXT", ImPlotCol_::ImPlotCol_LegendText)
        .value("TITLE_TEXT", ImPlotCol_::ImPlotCol_TitleText)
        .value("INLAY_TEXT", ImPlotCol_::ImPlotCol_InlayText)
        .value("AXIS_TEXT", ImPlotCol_::ImPlotCol_AxisText)
        .value("AXIS_GRID", ImPlotCol_::ImPlotCol_AxisGrid)
        .value("AXIS_TICK", ImPlotCol_::ImPlotCol_AxisTick)
        .value("AXIS_BG", ImPlotCol_::ImPlotCol_AxisBg)
        .value("AXIS_BG_HOVERED", ImPlotCol_::ImPlotCol_AxisBgHovered)
        .value("AXIS_BG_ACTIVE", ImPlotCol_::ImPlotCol_AxisBgActive)
        .value("SELECTION", ImPlotCol_::ImPlotCol_Selection)
        .value("CROSSHAIRS", ImPlotCol_::ImPlotCol_Crosshairs)
        .value("COUNT", ImPlotCol_::ImPlotCol_COUNT)
        .export_values()
    ;
    py::enum_<ImPlotStyleVar_>(_implot, "StyleVar", py::arithmetic())
        .value("LINE_WEIGHT", ImPlotStyleVar_::ImPlotStyleVar_LineWeight)
        .value("MARKER", ImPlotStyleVar_::ImPlotStyleVar_Marker)
        .value("MARKER_SIZE", ImPlotStyleVar_::ImPlotStyleVar_MarkerSize)
        .value("MARKER_WEIGHT", ImPlotStyleVar_::ImPlotStyleVar_MarkerWeight)
        .value("FILL_ALPHA", ImPlotStyleVar_::ImPlotStyleVar_FillAlpha)
        .value("ERROR_BAR_SIZE", ImPlotStyleVar_::ImPlotStyleVar_ErrorBarSize)
        .value("ERROR_BAR_WEIGHT", ImPlotStyleVar_::ImPlotStyleVar_ErrorBarWeight)
        .value("DIGITAL_BIT_HEIGHT", ImPlotStyleVar_::ImPlotStyleVar_DigitalBitHeight)
        .value("DIGITAL_BIT_GAP", ImPlotStyleVar_::ImPlotStyleVar_DigitalBitGap)
        .value("PLOT_BORDER_SIZE", ImPlotStyleVar_::ImPlotStyleVar_PlotBorderSize)
        .value("MINOR_ALPHA", ImPlotStyleVar_::ImPlotStyleVar_MinorAlpha)
        .value("MAJOR_TICK_LEN", ImPlotStyleVar_::ImPlotStyleVar_MajorTickLen)
        .value("MINOR_TICK_LEN", ImPlotStyleVar_::ImPlotStyleVar_MinorTickLen)
        .value("MAJOR_TICK_SIZE", ImPlotStyleVar_::ImPlotStyleVar_MajorTickSize)
        .value("MINOR_TICK_SIZE", ImPlotStyleVar_::ImPlotStyleVar_MinorTickSize)
        .value("MAJOR_GRID_SIZE", ImPlotStyleVar_::ImPlotStyleVar_MajorGridSize)
        .value("MINOR_GRID_SIZE", ImPlotStyleVar_::ImPlotStyleVar_MinorGridSize)
        .value("PLOT_PADDING", ImPlotStyleVar_::ImPlotStyleVar_PlotPadding)
        .value("LABEL_PADDING", ImPlotStyleVar_::ImPlotStyleVar_LabelPadding)
        .value("LEGEND_PADDING", ImPlotStyleVar_::ImPlotStyleVar_LegendPadding)
        .value("LEGEND_INNER_PADDING", ImPlotStyleVar_::ImPlotStyleVar_LegendInnerPadding)
        .value("LEGEND_SPACING", ImPlotStyleVar_::ImPlotStyleVar_LegendSpacing)
        .value("MOUSE_POS_PADDING", ImPlotStyleVar_::ImPlotStyleVar_MousePosPadding)
        .value("ANNOTATION_PADDING", ImPlotStyleVar_::ImPlotStyleVar_AnnotationPadding)
        .value("FIT_PADDING", ImPlotStyleVar_::ImPlotStyleVar_FitPadding)
        .value("PLOT_DEFAULT_SIZE", ImPlotStyleVar_::ImPlotStyleVar_PlotDefaultSize)
        .value("PLOT_MIN_SIZE", ImPlotStyleVar_::ImPlotStyleVar_PlotMinSize)
        .value("COUNT", ImPlotStyleVar_::ImPlotStyleVar_COUNT)
        .export_values()
    ;
    py::enum_<ImPlotScale_>(_implot, "Scale", py::arithmetic())
        .value("LINEAR", ImPlotScale_::ImPlotScale_Linear)
        .value("TIME", ImPlotScale_::ImPlotScale_Time)
        .value("LOG10", ImPlotScale_::ImPlotScale_Log10)
        .value("SYM_LOG", ImPlotScale_::ImPlotScale_SymLog)
        .export_values()
    ;
    py::enum_<ImPlotMarker_>(_implot, "Marker", py::arithmetic())
        .value("NONE", ImPlotMarker_::ImPlotMarker_None)
        .value("CIRCLE", ImPlotMarker_::ImPlotMarker_Circle)
        .value("SQUARE", ImPlotMarker_::ImPlotMarker_Square)
        .value("DIAMOND", ImPlotMarker_::ImPlotMarker_Diamond)
        .value("UP", ImPlotMarker_::ImPlotMarker_Up)
        .value("DOWN", ImPlotMarker_::ImPlotMarker_Down)
        .value("LEFT", ImPlotMarker_::ImPlotMarker_Left)
        .value("RIGHT", ImPlotMarker_::ImPlotMarker_Right)
        .value("CROSS", ImPlotMarker_::ImPlotMarker_Cross)
        .value("PLUS", ImPlotMarker_::ImPlotMarker_Plus)
        .value("ASTERISK", ImPlotMarker_::ImPlotMarker_Asterisk)
        .value("COUNT", ImPlotMarker_::ImPlotMarker_COUNT)
        .export_values()
    ;
    py::enum_<ImPlotColormap_>(_implot, "Colormap", py::arithmetic())
        .value("DEEP", ImPlotColormap_::ImPlotColormap_Deep)
        .value("DARK", ImPlotColormap_::ImPlotColormap_Dark)
        .value("PASTEL", ImPlotColormap_::ImPlotColormap_Pastel)
        .value("PAIRED", ImPlotColormap_::ImPlotColormap_Paired)
        .value("VIRIDIS", ImPlotColormap_::ImPlotColormap_Viridis)
        .value("PLASMA", ImPlotColormap_::ImPlotColormap_Plasma)
        .value("HOT", ImPlotColormap_::ImPlotColormap_Hot)
        .value("COOL", ImPlotColormap_::ImPlotColormap_Cool)
        .value("PINK", ImPlotColormap_::ImPlotColormap_Pink)
        .value("JET", ImPlotColormap_::ImPlotColormap_Jet)
        .value("TWILIGHT", ImPlotColormap_::ImPlotColormap_Twilight)
        .value("RD_BU", ImPlotColormap_::ImPlotColormap_RdBu)
        .value("BR_BG", ImPlotColormap_::ImPlotColormap_BrBG)
        .value("PI_YG", ImPlotColormap_::ImPlotColormap_PiYG)
        .value("SPECTRAL", ImPlotColormap_::ImPlotColormap_Spectral)
        .value("GREYS", ImPlotColormap_::ImPlotColormap_Greys)
        .export_values()
    ;
    py::enum_<ImPlotLocation_>(_implot, "Location", py::arithmetic())
        .value("CENTER", ImPlotLocation_::ImPlotLocation_Center)
        .value("NORTH", ImPlotLocation_::ImPlotLocation_North)
        .value("SOUTH", ImPlotLocation_::ImPlotLocation_South)
        .value("WEST", ImPlotLocation_::ImPlotLocation_West)
        .value("EAST", ImPlotLocation_::ImPlotLocation_East)
        .value("NORTH_WEST", ImPlotLocation_::ImPlotLocation_NorthWest)
        .value("NORTH_EAST", ImPlotLocation_::ImPlotLocation_NorthEast)
        .value("SOUTH_WEST", ImPlotLocation_::ImPlotLocation_SouthWest)
        .value("SOUTH_EAST", ImPlotLocation_::ImPlotLocation_SouthEast)
        .export_values()
    ;
    py::enum_<ImPlotBin_>(_implot, "Bin", py::arithmetic())
        .value("SQRT", ImPlotBin_::ImPlotBin_Sqrt)
        .value("STURGES", ImPlotBin_::ImPlotBin_Sturges)
        .value("RICE", ImPlotBin_::ImPlotBin_Rice)
        .value("SCOTT", ImPlotBin_::ImPlotBin_Scott)
        .export_values()
    ;
    py::class_<ImPlotPoint> _Point(_implot, "Point");
    registry.on(_implot, "Point", _Point);
        _Point
        .def_readwrite("x", &ImPlotPoint::x)
        .def_readwrite("y", &ImPlotPoint::y)
        .def(py::init<>())
        .def(py::init<double, double>()
        , py::arg("x")
        , py::arg("y")
        )
        .def(py::init<const ImVec2 &>()
        , py::arg("p")
        )
    ;

    py::class_<ImPlotRange> _Range(_implot, "Range");
    registry.on(_implot, "Range", _Range);
        _Range
        .def_readwrite("min", &ImPlotRange::Min)
        .def_readwrite("max", &ImPlotRange::Max)
        .def(py::init<>())
        .def(py::init<double, double>()
        , py::arg("min")
        , py::arg("max")
        )
        .def("contains", &ImPlotRange::Contains
            , py::arg("value")
            , py::return_value_policy::automatic_reference)
        .def("size", &ImPlotRange::Size
            , py::return_value_policy::automatic_reference)
        .def("clamp", &ImPlotRange::Clamp
            , py::arg("value")
            , py::return_value_policy::automatic_reference)
    ;

    py::class_<ImPlotRect> _Rect(_implot, "Rect");
    registry.on(_implot, "Rect", _Rect);
        _Rect
        .def_readwrite("x", &ImPlotRect::X)
        .def_readwrite("y", &ImPlotRect::Y)
        .def(py::init<>())
        .def(py::init<double, double, double, double>()
        , py::arg("x_min")
        , py::arg("x_max")
        , py::arg("y_min")
        , py::arg("y_max")
        )
        .def("size", &ImPlotRect::Size
            , py::return_value_policy::automatic_reference)
        .def("clamp", py::overload_cast<const ImPlotPoint &>(&ImPlotRect::Clamp)
            , py::arg("p")
            , py::return_value_policy::automatic_reference)
        .def("clamp", py::overload_cast<double, double>(&ImPlotRect::Clamp)
            , py::arg("x")
            , py::arg("y")
            , py::return_value_policy::automatic_reference)
        .def("min", &ImPlotRect::Min
            , py::return_value_policy::automatic_reference)
        .def("max", &ImPlotRect::Max
            , py::return_value_policy::automatic_reference)
    ;

    py::class_<ImPlotStyle> _Style(_implot, "Style");
    registry.on(_implot, "Style", _Style);
        _Style
        .def_readwrite("line_weight", &ImPlotStyle::LineWeight)
        .def_readwrite("marker", &ImPlotStyle::Marker)
        .def_readwrite("marker_size", &ImPlotStyle::MarkerSize)
        .def_readwrite("marker_weight", &ImPlotStyle::MarkerWeight)
        .def_readwrite("fill_alpha", &ImPlotStyle::FillAlpha)
        .def_readwrite("error_bar_size", &ImPlotStyle::ErrorBarSize)
        .def_readwrite("error_bar_weight", &ImPlotStyle::ErrorBarWeight)
        .def_readwrite("digital_bit_height", &ImPlotStyle::DigitalBitHeight)
        .def_readwrite("digital_bit_gap", &ImPlotStyle::DigitalBitGap)
        .def_readwrite("plot_border_size", &ImPlotStyle::PlotBorderSize)
        .def_readwrite("minor_alpha", &ImPlotStyle::MinorAlpha)
        .def_readwrite("major_tick_len", &ImPlotStyle::MajorTickLen)
        .def_readwrite("minor_tick_len", &ImPlotStyle::MinorTickLen)
        .def_readwrite("major_tick_size", &ImPlotStyle::MajorTickSize)
        .def_readwrite("minor_tick_size", &ImPlotStyle::MinorTickSize)
        .def_readwrite("major_grid_size", &ImPlotStyle::MajorGridSize)
        .def_readwrite("minor_grid_size", &ImPlotStyle::MinorGridSize)
        .def_readwrite("plot_padding", &ImPlotStyle::PlotPadding)
        .def_readwrite("label_padding", &ImPlotStyle::LabelPadding)
        .def_readwrite("legend_padding", &ImPlotStyle::LegendPadding)
        .def_readwrite("legend_inner_padding", &ImPlotStyle::LegendInnerPadding)
        .def_readwrite("legend_spacing", &ImPlotStyle::LegendSpacing)
        .def_readwrite("mouse_pos_padding", &ImPlotStyle::MousePosPadding)
        .def_readwrite("annotation_padding", &ImPlotStyle::AnnotationPadding)
        .def_readwrite("fit_padding", &ImPlotStyle::FitPadding)
        .def_readwrite("plot_default_size", &ImPlotStyle::PlotDefaultSize)
        .def_readwrite("plot_min_size", &ImPlotStyle::PlotMinSize)
        .def_readonly("colors", &ImPlotStyle::Colors)
        .def_readwrite("colormap", &ImPlotStyle::Colormap)
        .def_readwrite("use_local_time", &ImPlotStyle::UseLocalTime)
        .def_readwrite("use_iso8601", &ImPlotStyle::UseISO8601)
        .def_readwrite("use24_hour_clock", &ImPlotStyle::Use24HourClock)
        .def(py::init<>())
    ;

    py::class_<ImPlotInputMap> _InputMap(_implot, "InputMap");
    registry.on(_implot, "InputMap", _InputMap);
        _InputMap
        .def_readwrite("pan", &ImPlotInputMap::Pan)
        .def_readwrite("pan_mod", &ImPlotInputMap::PanMod)
        .def_readwrite("fit", &ImPlotInputMap::Fit)
        .def_readwrite("select", &ImPlotInputMap::Select)
        .def_readwrite("select_cancel", &ImPlotInputMap::SelectCancel)
        .def_readwrite("select_mod", &ImPlotInputMap::SelectMod)
        .def_readwrite("select_horz_mod", &ImPlotInputMap::SelectHorzMod)
        .def_readwrite("select_vert_mod", &ImPlotInputMap::SelectVertMod)
        .def_readwrite("menu", &ImPlotInputMap::Menu)
        .def_readwrite("override_mod", &ImPlotInputMap::OverrideMod)
        .def_readwrite("zoom_mod", &ImPlotInputMap::ZoomMod)
        .def_readwrite("zoom_rate", &ImPlotInputMap::ZoomRate)
        .def(py::init<>())
    ;

    _implot
    .def("create_context", []()
        {
            auto ret = py::capsule(ImPlot::CreateContext(), "ImPlotContext");
            return ret;
        }
        , py::return_value_policy::automatic_reference)
    .def("destroy_context", [](const py::capsule& ctx)
        {
            ImPlot::DestroyContext(ctx);
            return ;
        }
        , py::arg("ctx") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("get_current_context", []()
        {
            auto ret = py::capsule(ImPlot::GetCurrentContext(), "ImPlotContext");
            return ret;
        }
        , py::return_value_policy::automatic_reference)
    .def("set_current_context", [](const py::capsule& ctx)
        {
            ImPlot::SetCurrentContext(ctx);
            return ;
        }
        , py::arg("ctx")
        , py::return_value_policy::automatic_reference)
    .def("set_im_gui_context", [](const py::capsule& ctx)
        {
            ImPlot::SetImGuiContext(ctx);
            return ;
        }
        , py::arg("ctx")
        , py::return_value_policy::automatic_reference)
    .def("begin_plot", &ImPlot::BeginPlot
        , py::arg("title_id")
        , py::arg("size") = ImVec2(-1,0)
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("end_plot", &ImPlot::EndPlot
        , py::return_value_policy::automatic_reference)
    .def("begin_subplots", [](const char * title_id, int rows, int cols, const ImVec2 & size, int flags, float * row_ratios, float * col_ratios)
        {
            auto ret = ImPlot::BeginSubplots(title_id, rows, cols, size, flags, row_ratios, col_ratios);
            return std::make_tuple(ret, row_ratios, col_ratios);
        }
        , py::arg("title_id")
        , py::arg("rows")
        , py::arg("cols")
        , py::arg("size")
        , py::arg("flags") = 0
        , py::arg("row_ratios") = nullptr
        , py::arg("col_ratios") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("end_subplots", &ImPlot::EndSubplots
        , py::return_value_policy::automatic_reference)
    .def("setup_axis", &ImPlot::SetupAxis
        , py::arg("axis")
        , py::arg("label") = nullptr
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("setup_axis_limits", &ImPlot::SetupAxisLimits
        , py::arg("axis")
        , py::arg("v_min")
        , py::arg("v_max")
        , py::arg("cond") = ImPlotCond_::ImPlotCond_Once
        , py::return_value_policy::automatic_reference)
    .def("setup_axis_links", [](int axis, double * link_min, double * link_max)
        {
            ImPlot::SetupAxisLinks(axis, link_min, link_max);
            return std::make_tuple(link_min, link_max);
        }
        , py::arg("axis")
        , py::arg("link_min")
        , py::arg("link_max")
        , py::return_value_policy::automatic_reference)
    .def("setup_axis_format", py::overload_cast<int, const char *>(&ImPlot::SetupAxisFormat)
        , py::arg("axis")
        , py::arg("fmt")
        , py::return_value_policy::automatic_reference)
    .def("setup_axis_format", py::overload_cast<int, int (*)(double, char *, int, void *), void *>(&ImPlot::SetupAxisFormat)
        , py::arg("axis")
        , py::arg("formatter")
        , py::arg("data") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("setup_axis_scale", py::overload_cast<int, int>(&ImPlot::SetupAxisScale)
        , py::arg("axis")
        , py::arg("scale")
        , py::return_value_policy::automatic_reference)
    .def("setup_axis_scale", py::overload_cast<int, double (*)(double, void *), double (*)(double, void *), void *>(&ImPlot::SetupAxisScale)
        , py::arg("axis")
        , py::arg("forward")
        , py::arg("inverse")
        , py::arg("data") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("setup_axis_limits_constraints", &ImPlot::SetupAxisLimitsConstraints
        , py::arg("axis")
        , py::arg("v_min")
        , py::arg("v_max")
        , py::return_value_policy::automatic_reference)
    .def("setup_axis_zoom_constraints", &ImPlot::SetupAxisZoomConstraints
        , py::arg("axis")
        , py::arg("z_min")
        , py::arg("z_max")
        , py::return_value_policy::automatic_reference)
    .def("setup_axes", &ImPlot::SetupAxes
        , py::arg("x_label")
        , py::arg("y_label")
        , py::arg("x_flags") = 0
        , py::arg("y_flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("setup_axes_limits", &ImPlot::SetupAxesLimits
        , py::arg("x_min")
        , py::arg("x_max")
        , py::arg("y_min")
        , py::arg("y_max")
        , py::arg("cond") = ImPlotCond_::ImPlotCond_Once
        , py::return_value_policy::automatic_reference)
    .def("setup_legend", &ImPlot::SetupLegend
        , py::arg("location")
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("setup_mouse_text", &ImPlot::SetupMouseText
        , py::arg("location")
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("setup_finish", &ImPlot::SetupFinish
        , py::return_value_policy::automatic_reference)
    .def("set_next_axis_limits", &ImPlot::SetNextAxisLimits
        , py::arg("axis")
        , py::arg("v_min")
        , py::arg("v_max")
        , py::arg("cond") = ImPlotCond_::ImPlotCond_Once
        , py::return_value_policy::automatic_reference)
    .def("set_next_axis_links", [](int axis, double * link_min, double * link_max)
        {
            ImPlot::SetNextAxisLinks(axis, link_min, link_max);
            return std::make_tuple(link_min, link_max);
        }
        , py::arg("axis")
        , py::arg("link_min")
        , py::arg("link_max")
        , py::return_value_policy::automatic_reference)
    .def("set_next_axis_to_fit", &ImPlot::SetNextAxisToFit
        , py::arg("axis")
        , py::return_value_policy::automatic_reference)
    .def("set_next_axes_limits", &ImPlot::SetNextAxesLimits
        , py::arg("x_min")
        , py::arg("x_max")
        , py::arg("y_min")
        , py::arg("y_max")
        , py::arg("cond") = ImPlotCond_::ImPlotCond_Once
        , py::return_value_policy::automatic_reference)
    .def("set_next_axes_to_fit", &ImPlot::SetNextAxesToFit
        , py::return_value_policy::automatic_reference)
    .def("plot_line_g", &ImPlot::PlotLineG
        , py::arg("label_id")
        , py::arg("getter")
        , py::arg("data")
        , py::arg("count")
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("plot_scatter_g", &ImPlot::PlotScatterG
        , py::arg("label_id")
        , py::arg("getter")
        , py::arg("data")
        , py::arg("count")
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("plot_stairs_g", &ImPlot::PlotStairsG
        , py::arg("label_id")
        , py::arg("getter")
        , py::arg("data")
        , py::arg("count")
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("plot_shaded_g", &ImPlot::PlotShadedG
        , py::arg("label_id")
        , py::arg("getter1")
        , py::arg("data1")
        , py::arg("getter2")
        , py::arg("data2")
        , py::arg("count")
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("plot_bars_g", &ImPlot::PlotBarsG
        , py::arg("label_id")
        , py::arg("getter")
        , py::arg("data")
        , py::arg("count")
        , py::arg("bar_size")
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("plot_digital_g", &ImPlot::PlotDigitalG
        , py::arg("label_id")
        , py::arg("getter")
        , py::arg("data")
        , py::arg("count")
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("plot_image", &ImPlot::PlotImage
        , py::arg("label_id")
        , py::arg("tex_ref")
        , py::arg("bounds_min")
        , py::arg("bounds_max")
        , py::arg("uv0") = ImVec2(0,0)
        , py::arg("uv1") = ImVec2(1,1)
        , py::arg("tint_col") = ImVec4(1,1,1,1)
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("plot_text", &ImPlot::PlotText
        , py::arg("text")
        , py::arg("x")
        , py::arg("y")
        , py::arg("pix_offset") = ImVec2(0,0)
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("plot_dummy", &ImPlot::PlotDummy
        , py::arg("label_id")
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("drag_point", [](int id, double * x, double * y, const ImVec4 & col, float size, int flags, bool * out_clicked, bool * out_hovered, bool * held)
        {
            auto ret = ImPlot::DragPoint(id, x, y, col, size, flags, out_clicked, out_hovered, held);
            return std::make_tuple(ret, x, y, out_clicked, out_hovered, held);
        }
        , py::arg("id")
        , py::arg("x")
        , py::arg("y")
        , py::arg("col")
        , py::arg("size") = 4
        , py::arg("flags") = 0
        , py::arg("out_clicked") = nullptr
        , py::arg("out_hovered") = nullptr
        , py::arg("held") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("drag_line_x", [](int id, double * x, const ImVec4 & col, float thickness, int flags, bool * out_clicked, bool * out_hovered, bool * held)
        {
            auto ret = ImPlot::DragLineX(id, x, col, thickness, flags, out_clicked, out_hovered, held);
            return std::make_tuple(ret, x, out_clicked, out_hovered, held);
        }
        , py::arg("id")
        , py::arg("x")
        , py::arg("col")
        , py::arg("thickness") = 1
        , py::arg("flags") = 0
        , py::arg("out_clicked") = nullptr
        , py::arg("out_hovered") = nullptr
        , py::arg("held") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("drag_line_y", [](int id, double * y, const ImVec4 & col, float thickness, int flags, bool * out_clicked, bool * out_hovered, bool * held)
        {
            auto ret = ImPlot::DragLineY(id, y, col, thickness, flags, out_clicked, out_hovered, held);
            return std::make_tuple(ret, y, out_clicked, out_hovered, held);
        }
        , py::arg("id")
        , py::arg("y")
        , py::arg("col")
        , py::arg("thickness") = 1
        , py::arg("flags") = 0
        , py::arg("out_clicked") = nullptr
        , py::arg("out_hovered") = nullptr
        , py::arg("held") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("drag_rect", [](int id, double * x1, double * y1, double * x2, double * y2, const ImVec4 & col, int flags, bool * out_clicked, bool * out_hovered, bool * held)
        {
            auto ret = ImPlot::DragRect(id, x1, y1, x2, y2, col, flags, out_clicked, out_hovered, held);
            return std::make_tuple(ret, x1, y1, x2, y2, out_clicked, out_hovered, held);
        }
        , py::arg("id")
        , py::arg("x1")
        , py::arg("y1")
        , py::arg("x2")
        , py::arg("y2")
        , py::arg("col")
        , py::arg("flags") = 0
        , py::arg("out_clicked") = nullptr
        , py::arg("out_hovered") = nullptr
        , py::arg("held") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("annotation", py::overload_cast<double, double, const ImVec4 &, const ImVec2 &, bool, bool>(&ImPlot::Annotation)
        , py::arg("x")
        , py::arg("y")
        , py::arg("col")
        , py::arg("pix_offset")
        , py::arg("clamp")
        , py::arg("round") = false
        , py::return_value_policy::automatic_reference)
    .def("annotation", [](double x, double y, const ImVec4 & col, const ImVec2 & pix_offset, bool clamp, const char * fmt)
        {
            ImPlot::Annotation(x, y, col, pix_offset, clamp, fmt);
            return ;
        }
        , py::arg("x")
        , py::arg("y")
        , py::arg("col")
        , py::arg("pix_offset")
        , py::arg("clamp")
        , py::arg("fmt")
        , py::return_value_policy::automatic_reference)
    .def("tag_x", py::overload_cast<double, const ImVec4 &, bool>(&ImPlot::TagX)
        , py::arg("x")
        , py::arg("col")
        , py::arg("round") = false
        , py::return_value_policy::automatic_reference)
    .def("tag_x", [](double x, const ImVec4 & col, const char * fmt)
        {
            ImPlot::TagX(x, col, fmt);
            return ;
        }
        , py::arg("x")
        , py::arg("col")
        , py::arg("fmt")
        , py::return_value_policy::automatic_reference)
    .def("tag_y", py::overload_cast<double, const ImVec4 &, bool>(&ImPlot::TagY)
        , py::arg("y")
        , py::arg("col")
        , py::arg("round") = false
        , py::return_value_policy::automatic_reference)
    .def("tag_y", [](double y, const ImVec4 & col, const char * fmt)
        {
            ImPlot::TagY(y, col, fmt);
            return ;
        }
        , py::arg("y")
        , py::arg("col")
        , py::arg("fmt")
        , py::return_value_policy::automatic_reference)
    .def("set_axis", &ImPlot::SetAxis
        , py::arg("axis")
        , py::return_value_policy::automatic_reference)
    .def("set_axes", &ImPlot::SetAxes
        , py::arg("x_axis")
        , py::arg("y_axis")
        , py::return_value_policy::automatic_reference)
    .def("plot_to_pixels", py::overload_cast<const ImPlotPoint &, int, int>(&ImPlot::PlotToPixels)
        , py::arg("plt")
        , py::arg("x_axis") = IMPLOT_AUTO
        , py::arg("y_axis") = IMPLOT_AUTO
        , py::return_value_policy::automatic_reference)
    .def("plot_to_pixels", py::overload_cast<double, double, int, int>(&ImPlot::PlotToPixels)
        , py::arg("x")
        , py::arg("y")
        , py::arg("x_axis") = IMPLOT_AUTO
        , py::arg("y_axis") = IMPLOT_AUTO
        , py::return_value_policy::automatic_reference)
    .def("get_plot_pos", &ImPlot::GetPlotPos
        , py::return_value_policy::automatic_reference)
    .def("get_plot_size", &ImPlot::GetPlotSize
        , py::return_value_policy::automatic_reference)
    .def("get_plot_mouse_pos", &ImPlot::GetPlotMousePos
        , py::arg("x_axis") = IMPLOT_AUTO
        , py::arg("y_axis") = IMPLOT_AUTO
        , py::return_value_policy::automatic_reference)
    .def("get_plot_limits", &ImPlot::GetPlotLimits
        , py::arg("x_axis") = IMPLOT_AUTO
        , py::arg("y_axis") = IMPLOT_AUTO
        , py::return_value_policy::automatic_reference)
    .def("is_plot_hovered", &ImPlot::IsPlotHovered
        , py::return_value_policy::automatic_reference)
    .def("is_axis_hovered", &ImPlot::IsAxisHovered
        , py::arg("axis")
        , py::return_value_policy::automatic_reference)
    .def("is_subplots_hovered", &ImPlot::IsSubplotsHovered
        , py::return_value_policy::automatic_reference)
    .def("is_plot_selected", &ImPlot::IsPlotSelected
        , py::return_value_policy::automatic_reference)
    .def("get_plot_selection", &ImPlot::GetPlotSelection
        , py::arg("x_axis") = IMPLOT_AUTO
        , py::arg("y_axis") = IMPLOT_AUTO
        , py::return_value_policy::automatic_reference)
    .def("cancel_plot_selection", &ImPlot::CancelPlotSelection
        , py::return_value_policy::automatic_reference)
    .def("hide_next_item", &ImPlot::HideNextItem
        , py::arg("hidden") = true
        , py::arg("cond") = ImPlotCond_::ImPlotCond_Once
        , py::return_value_policy::automatic_reference)
    .def("begin_aligned_plots", &ImPlot::BeginAlignedPlots
        , py::arg("group_id")
        , py::arg("vertical") = true
        , py::return_value_policy::automatic_reference)
    .def("end_aligned_plots", &ImPlot::EndAlignedPlots
        , py::return_value_policy::automatic_reference)
    .def("begin_legend_popup", &ImPlot::BeginLegendPopup
        , py::arg("label_id")
        , py::arg("mouse_button") = 1
        , py::return_value_policy::automatic_reference)
    .def("end_legend_popup", &ImPlot::EndLegendPopup
        , py::return_value_policy::automatic_reference)
    .def("is_legend_entry_hovered", &ImPlot::IsLegendEntryHovered
        , py::arg("label_id")
        , py::return_value_policy::automatic_reference)
    .def("begin_drag_drop_target_plot", &ImPlot::BeginDragDropTargetPlot
        , py::return_value_policy::automatic_reference)
    .def("begin_drag_drop_target_axis", &ImPlot::BeginDragDropTargetAxis
        , py::arg("axis")
        , py::return_value_policy::automatic_reference)
    .def("begin_drag_drop_target_legend", &ImPlot::BeginDragDropTargetLegend
        , py::return_value_policy::automatic_reference)
    .def("end_drag_drop_target", &ImPlot::EndDragDropTarget
        , py::return_value_policy::automatic_reference)
    .def("begin_drag_drop_source_plot", &ImPlot::BeginDragDropSourcePlot
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("begin_drag_drop_source_axis", &ImPlot::BeginDragDropSourceAxis
        , py::arg("axis")
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("begin_drag_drop_source_item", &ImPlot::BeginDragDropSourceItem
        , py::arg("label_id")
        , py::arg("flags") = 0
        , py::return_value_policy::automatic_reference)
    .def("end_drag_drop_source", &ImPlot::EndDragDropSource
        , py::return_value_policy::automatic_reference)
    .def("get_style", &ImPlot::GetStyle
        , py::return_value_policy::reference)
    .def("style_colors_auto", &ImPlot::StyleColorsAuto
        , py::arg("dst") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("style_colors_classic", &ImPlot::StyleColorsClassic
        , py::arg("dst") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("style_colors_dark", &ImPlot::StyleColorsDark
        , py::arg("dst") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("style_colors_light", &ImPlot::StyleColorsLight
        , py::arg("dst") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("push_style_color", py::overload_cast<int, unsigned int>(&ImPlot::PushStyleColor)
        , py::arg("idx")
        , py::arg("col")
        , py::return_value_policy::automatic_reference)
    .def("push_style_color", py::overload_cast<int, const ImVec4 &>(&ImPlot::PushStyleColor)
        , py::arg("idx")
        , py::arg("col")
        , py::return_value_policy::automatic_reference)
    .def("pop_style_color", &ImPlot::PopStyleColor
        , py::arg("count") = 1
        , py::return_value_policy::automatic_reference)
    .def("push_style_var", py::overload_cast<int, float>(&ImPlot::PushStyleVar)
        , py::arg("idx")
        , py::arg("val")
        , py::return_value_policy::automatic_reference)
    .def("push_style_var", py::overload_cast<int, int>(&ImPlot::PushStyleVar)
        , py::arg("idx")
        , py::arg("val")
        , py::return_value_policy::automatic_reference)
    .def("push_style_var", py::overload_cast<int, const ImVec2 &>(&ImPlot::PushStyleVar)
        , py::arg("idx")
        , py::arg("val")
        , py::return_value_policy::automatic_reference)
    .def("pop_style_var", &ImPlot::PopStyleVar
        , py::arg("count") = 1
        , py::return_value_policy::automatic_reference)
    .def("set_next_line_style", &ImPlot::SetNextLineStyle
        , py::arg("col") = IMPLOT_AUTO_COL
        , py::arg("weight") = IMPLOT_AUTO
        , py::return_value_policy::automatic_reference)
    .def("set_next_fill_style", &ImPlot::SetNextFillStyle
        , py::arg("col") = IMPLOT_AUTO_COL
        , py::arg("alpha_mod") = IMPLOT_AUTO
        , py::return_value_policy::automatic_reference)
    .def("set_next_marker_style", &ImPlot::SetNextMarkerStyle
        , py::arg("marker") = IMPLOT_AUTO
        , py::arg("size") = IMPLOT_AUTO
        , py::arg("fill") = IMPLOT_AUTO_COL
        , py::arg("weight") = IMPLOT_AUTO
        , py::arg("outline") = IMPLOT_AUTO_COL
        , py::return_value_policy::automatic_reference)
    .def("set_next_error_bar_style", &ImPlot::SetNextErrorBarStyle
        , py::arg("col") = IMPLOT_AUTO_COL
        , py::arg("size") = IMPLOT_AUTO
        , py::arg("weight") = IMPLOT_AUTO
        , py::return_value_policy::automatic_reference)
    .def("get_last_item_color", &ImPlot::GetLastItemColor
        , py::return_value_policy::automatic_reference)
    .def("get_style_color_name", &ImPlot::GetStyleColorName
        , py::arg("idx")
        , py::return_value_policy::automatic_reference)
    .def("get_marker_name", &ImPlot::GetMarkerName
        , py::arg("idx")
        , py::return_value_policy::automatic_reference)
    .def("add_colormap", py::overload_cast<const char *, const ImVec4 *, int, bool>(&ImPlot::AddColormap)
        , py::arg("name")
        , py::arg("cols")
        , py::arg("size")
        , py::arg("qual") = true
        , py::return_value_policy::automatic_reference)
    .def("add_colormap", py::overload_cast<const char *, const unsigned int *, int, bool>(&ImPlot::AddColormap)
        , py::arg("name")
        , py::arg("cols")
        , py::arg("size")
        , py::arg("qual") = true
        , py::return_value_policy::automatic_reference)
    .def("get_colormap_count", &ImPlot::GetColormapCount
        , py::return_value_policy::automatic_reference)
    .def("get_colormap_name", &ImPlot::GetColormapName
        , py::arg("cmap")
        , py::return_value_policy::automatic_reference)
    .def("get_colormap_index", &ImPlot::GetColormapIndex
        , py::arg("name")
        , py::return_value_policy::automatic_reference)
    .def("push_colormap", py::overload_cast<int>(&ImPlot::PushColormap)
        , py::arg("cmap")
        , py::return_value_policy::automatic_reference)
    .def("push_colormap", py::overload_cast<const char *>(&ImPlot::PushColormap)
        , py::arg("name")
        , py::return_value_policy::automatic_reference)
    .def("pop_colormap", &ImPlot::PopColormap
        , py::arg("count") = 1
        , py::return_value_policy::automatic_reference)
    .def("next_colormap_color", &ImPlot::NextColormapColor
        , py::return_value_policy::automatic_reference)
    .def("get_colormap_size", &ImPlot::GetColormapSize
        , py::arg("cmap") = IMPLOT_AUTO
        , py::return_value_policy::automatic_reference)
    .def("get_colormap_color", &ImPlot::GetColormapColor
        , py::arg("idx")
        , py::arg("cmap") = IMPLOT_AUTO
        , py::return_value_policy::automatic_reference)
    .def("sample_colormap", &ImPlot::SampleColormap
        , py::arg("t")
        , py::arg("cmap") = IMPLOT_AUTO
        , py::return_value_policy::automatic_reference)
    .def("colormap_scale", &ImPlot::ColormapScale
        , py::arg("label")
        , py::arg("scale_min")
        , py::arg("scale_max")
        , py::arg("size") = ImVec2(0,0)
        , py::arg("format") = nullptr
        , py::arg("flags") = 0
        , py::arg("cmap") = IMPLOT_AUTO
        , py::return_value_policy::automatic_reference)
    .def("colormap_slider", [](const char * label, float * t, ImVec4 * out, const char * format, int cmap)
        {
            auto ret = ImPlot::ColormapSlider(label, t, out, format, cmap);
            return std::make_tuple(ret, t);
        }
        , py::arg("label")
        , py::arg("t")
        , py::arg("out") = nullptr
        , py::arg("format") = nullptr
        , py::arg("cmap") = IMPLOT_AUTO
        , py::return_value_policy::automatic_reference)
    .def("colormap_button", &ImPlot::ColormapButton
        , py::arg("label")
        , py::arg("size") = ImVec2(0,0)
        , py::arg("cmap") = IMPLOT_AUTO
        , py::return_value_policy::automatic_reference)
    .def("bust_color_cache", &ImPlot::BustColorCache
        , py::arg("plot_title_id") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("get_input_map", &ImPlot::GetInputMap
        , py::return_value_policy::reference)
    .def("map_input_default", &ImPlot::MapInputDefault
        , py::arg("dst") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("map_input_reverse", &ImPlot::MapInputReverse
        , py::arg("dst") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("item_icon", py::overload_cast<const ImVec4 &>(&ImPlot::ItemIcon)
        , py::arg("col")
        , py::return_value_policy::automatic_reference)
    .def("item_icon", py::overload_cast<unsigned int>(&ImPlot::ItemIcon)
        , py::arg("col")
        , py::return_value_policy::automatic_reference)
    .def("colormap_icon", &ImPlot::ColormapIcon
        , py::arg("cmap")
        , py::return_value_policy::automatic_reference)
    .def("get_plot_draw_list", &ImPlot::GetPlotDrawList
        , py::return_value_policy::automatic_reference)
    .def("push_plot_clip_rect", &ImPlot::PushPlotClipRect
        , py::arg("expand") = 0
        , py::return_value_policy::automatic_reference)
    .def("pop_plot_clip_rect", &ImPlot::PopPlotClipRect
        , py::return_value_policy::automatic_reference)
    .def("show_style_selector", &ImPlot::ShowStyleSelector
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    .def("show_colormap_selector", &ImPlot::ShowColormapSelector
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    .def("show_input_map_selector", &ImPlot::ShowInputMapSelector
        , py::arg("label")
        , py::return_value_policy::automatic_reference)
    .def("show_style_editor", &ImPlot::ShowStyleEditor
        , py::arg("ref") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("show_user_guide", &ImPlot::ShowUserGuide
        , py::return_value_policy::automatic_reference)
    .def("show_metrics_window", [](bool * p_popen)
        {
            ImPlot::ShowMetricsWindow(p_popen);
            return p_popen;
        }
        , py::arg("p_popen") = nullptr
        , py::return_value_policy::automatic_reference)
    .def("show_demo_window", [](bool * p_open)
        {
            ImPlot::ShowDemoWindow(p_open);
            return p_open;
        }
        , py::arg("p_open") = nullptr
        , py::return_value_policy::automatic_reference)
    ;


}