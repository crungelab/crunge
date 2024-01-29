#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include "implot.h"
#include "implot_internal.h"

#include <cxbind/cxbind.h>
#include <crunge/imgui/crunge-imgui.h>
#include <crunge/imgui/conversions.h>

namespace py = pybind11;

void init_generated(py::module &_implot, Registry &registry) {
    py::enum_<ImAxis_>(_implot, "Axis", py::arithmetic())
        .value("AXIS_X1", ImAxis_::ImAxis_X1)
        .value("AXIS_X2", ImAxis_::ImAxis_X2)
        .value("AXIS_X3", ImAxis_::ImAxis_X3)
        .value("AXIS_Y1", ImAxis_::ImAxis_Y1)
        .value("AXIS_Y2", ImAxis_::ImAxis_Y2)
        .value("AXIS_Y3", ImAxis_::ImAxis_Y3)
        .value("AXIS_COUNT", ImAxis_::ImAxis_COUNT)
        .export_values();

    py::enum_<ImPlotFlags_>(_implot, "Flags", py::arithmetic())
        .value("FLAGS_NONE", ImPlotFlags_::ImPlotFlags_None)
        .value("FLAGS_NO_TITLE", ImPlotFlags_::ImPlotFlags_NoTitle)
        .value("FLAGS_NO_LEGEND", ImPlotFlags_::ImPlotFlags_NoLegend)
        .value("FLAGS_NO_MOUSE_TEXT", ImPlotFlags_::ImPlotFlags_NoMouseText)
        .value("FLAGS_NO_INPUTS", ImPlotFlags_::ImPlotFlags_NoInputs)
        .value("FLAGS_NO_MENUS", ImPlotFlags_::ImPlotFlags_NoMenus)
        .value("FLAGS_NO_BOX_SELECT", ImPlotFlags_::ImPlotFlags_NoBoxSelect)
        .value("FLAGS_NO_FRAME", ImPlotFlags_::ImPlotFlags_NoFrame)
        .value("FLAGS_EQUAL", ImPlotFlags_::ImPlotFlags_Equal)
        .value("FLAGS_CROSSHAIRS", ImPlotFlags_::ImPlotFlags_Crosshairs)
        .value("FLAGS_CANVAS_ONLY", ImPlotFlags_::ImPlotFlags_CanvasOnly)
        .export_values();

    py::enum_<ImPlotAxisFlags_>(_implot, "AxisFlags", py::arithmetic())
        .value("AXIS_FLAGS_NONE", ImPlotAxisFlags_::ImPlotAxisFlags_None)
        .value("AXIS_FLAGS_NO_LABEL", ImPlotAxisFlags_::ImPlotAxisFlags_NoLabel)
        .value("AXIS_FLAGS_NO_GRID_LINES", ImPlotAxisFlags_::ImPlotAxisFlags_NoGridLines)
        .value("AXIS_FLAGS_NO_TICK_MARKS", ImPlotAxisFlags_::ImPlotAxisFlags_NoTickMarks)
        .value("AXIS_FLAGS_NO_TICK_LABELS", ImPlotAxisFlags_::ImPlotAxisFlags_NoTickLabels)
        .value("AXIS_FLAGS_NO_INITIAL_FIT", ImPlotAxisFlags_::ImPlotAxisFlags_NoInitialFit)
        .value("AXIS_FLAGS_NO_MENUS", ImPlotAxisFlags_::ImPlotAxisFlags_NoMenus)
        .value("AXIS_FLAGS_NO_SIDE_SWITCH", ImPlotAxisFlags_::ImPlotAxisFlags_NoSideSwitch)
        .value("AXIS_FLAGS_NO_HIGHLIGHT", ImPlotAxisFlags_::ImPlotAxisFlags_NoHighlight)
        .value("AXIS_FLAGS_OPPOSITE", ImPlotAxisFlags_::ImPlotAxisFlags_Opposite)
        .value("AXIS_FLAGS_FOREGROUND", ImPlotAxisFlags_::ImPlotAxisFlags_Foreground)
        .value("AXIS_FLAGS_INVERT", ImPlotAxisFlags_::ImPlotAxisFlags_Invert)
        .value("AXIS_FLAGS_AUTO_FIT", ImPlotAxisFlags_::ImPlotAxisFlags_AutoFit)
        .value("AXIS_FLAGS_RANGE_FIT", ImPlotAxisFlags_::ImPlotAxisFlags_RangeFit)
        .value("AXIS_FLAGS_PAN_STRETCH", ImPlotAxisFlags_::ImPlotAxisFlags_PanStretch)
        .value("AXIS_FLAGS_LOCK_MIN", ImPlotAxisFlags_::ImPlotAxisFlags_LockMin)
        .value("AXIS_FLAGS_LOCK_MAX", ImPlotAxisFlags_::ImPlotAxisFlags_LockMax)
        .value("AXIS_FLAGS_LOCK", ImPlotAxisFlags_::ImPlotAxisFlags_Lock)
        .value("AXIS_FLAGS_NO_DECORATIONS", ImPlotAxisFlags_::ImPlotAxisFlags_NoDecorations)
        .value("AXIS_FLAGS_AUX_DEFAULT", ImPlotAxisFlags_::ImPlotAxisFlags_AuxDefault)
        .export_values();

    py::enum_<ImPlotSubplotFlags_>(_implot, "SubplotFlags", py::arithmetic())
        .value("SUBPLOT_FLAGS_NONE", ImPlotSubplotFlags_::ImPlotSubplotFlags_None)
        .value("SUBPLOT_FLAGS_NO_TITLE", ImPlotSubplotFlags_::ImPlotSubplotFlags_NoTitle)
        .value("SUBPLOT_FLAGS_NO_LEGEND", ImPlotSubplotFlags_::ImPlotSubplotFlags_NoLegend)
        .value("SUBPLOT_FLAGS_NO_MENUS", ImPlotSubplotFlags_::ImPlotSubplotFlags_NoMenus)
        .value("SUBPLOT_FLAGS_NO_RESIZE", ImPlotSubplotFlags_::ImPlotSubplotFlags_NoResize)
        .value("SUBPLOT_FLAGS_NO_ALIGN", ImPlotSubplotFlags_::ImPlotSubplotFlags_NoAlign)
        .value("SUBPLOT_FLAGS_SHARE_ITEMS", ImPlotSubplotFlags_::ImPlotSubplotFlags_ShareItems)
        .value("SUBPLOT_FLAGS_LINK_ROWS", ImPlotSubplotFlags_::ImPlotSubplotFlags_LinkRows)
        .value("SUBPLOT_FLAGS_LINK_COLS", ImPlotSubplotFlags_::ImPlotSubplotFlags_LinkCols)
        .value("SUBPLOT_FLAGS_LINK_ALL_X", ImPlotSubplotFlags_::ImPlotSubplotFlags_LinkAllX)
        .value("SUBPLOT_FLAGS_LINK_ALL_Y", ImPlotSubplotFlags_::ImPlotSubplotFlags_LinkAllY)
        .value("SUBPLOT_FLAGS_COL_MAJOR", ImPlotSubplotFlags_::ImPlotSubplotFlags_ColMajor)
        .export_values();

    py::enum_<ImPlotLegendFlags_>(_implot, "LegendFlags", py::arithmetic())
        .value("LEGEND_FLAGS_NONE", ImPlotLegendFlags_::ImPlotLegendFlags_None)
        .value("LEGEND_FLAGS_NO_BUTTONS", ImPlotLegendFlags_::ImPlotLegendFlags_NoButtons)
        .value("LEGEND_FLAGS_NO_HIGHLIGHT_ITEM", ImPlotLegendFlags_::ImPlotLegendFlags_NoHighlightItem)
        .value("LEGEND_FLAGS_NO_HIGHLIGHT_AXIS", ImPlotLegendFlags_::ImPlotLegendFlags_NoHighlightAxis)
        .value("LEGEND_FLAGS_NO_MENUS", ImPlotLegendFlags_::ImPlotLegendFlags_NoMenus)
        .value("LEGEND_FLAGS_OUTSIDE", ImPlotLegendFlags_::ImPlotLegendFlags_Outside)
        .value("LEGEND_FLAGS_HORIZONTAL", ImPlotLegendFlags_::ImPlotLegendFlags_Horizontal)
        .value("LEGEND_FLAGS_SORT", ImPlotLegendFlags_::ImPlotLegendFlags_Sort)
        .export_values();

    py::enum_<ImPlotMouseTextFlags_>(_implot, "MouseTextFlags", py::arithmetic())
        .value("MOUSE_TEXT_FLAGS_NONE", ImPlotMouseTextFlags_::ImPlotMouseTextFlags_None)
        .value("MOUSE_TEXT_FLAGS_NO_AUX_AXES", ImPlotMouseTextFlags_::ImPlotMouseTextFlags_NoAuxAxes)
        .value("MOUSE_TEXT_FLAGS_NO_FORMAT", ImPlotMouseTextFlags_::ImPlotMouseTextFlags_NoFormat)
        .value("MOUSE_TEXT_FLAGS_SHOW_ALWAYS", ImPlotMouseTextFlags_::ImPlotMouseTextFlags_ShowAlways)
        .export_values();

    py::enum_<ImPlotDragToolFlags_>(_implot, "DragToolFlags", py::arithmetic())
        .value("DRAG_TOOL_FLAGS_NONE", ImPlotDragToolFlags_::ImPlotDragToolFlags_None)
        .value("DRAG_TOOL_FLAGS_NO_CURSORS", ImPlotDragToolFlags_::ImPlotDragToolFlags_NoCursors)
        .value("DRAG_TOOL_FLAGS_NO_FIT", ImPlotDragToolFlags_::ImPlotDragToolFlags_NoFit)
        .value("DRAG_TOOL_FLAGS_NO_INPUTS", ImPlotDragToolFlags_::ImPlotDragToolFlags_NoInputs)
        .value("DRAG_TOOL_FLAGS_DELAYED", ImPlotDragToolFlags_::ImPlotDragToolFlags_Delayed)
        .export_values();

    py::enum_<ImPlotColormapScaleFlags_>(_implot, "ColormapScaleFlags", py::arithmetic())
        .value("COLORMAP_SCALE_FLAGS_NONE", ImPlotColormapScaleFlags_::ImPlotColormapScaleFlags_None)
        .value("COLORMAP_SCALE_FLAGS_NO_LABEL", ImPlotColormapScaleFlags_::ImPlotColormapScaleFlags_NoLabel)
        .value("COLORMAP_SCALE_FLAGS_OPPOSITE", ImPlotColormapScaleFlags_::ImPlotColormapScaleFlags_Opposite)
        .value("COLORMAP_SCALE_FLAGS_INVERT", ImPlotColormapScaleFlags_::ImPlotColormapScaleFlags_Invert)
        .export_values();

    py::enum_<ImPlotItemFlags_>(_implot, "ItemFlags", py::arithmetic())
        .value("ITEM_FLAGS_NONE", ImPlotItemFlags_::ImPlotItemFlags_None)
        .value("ITEM_FLAGS_NO_LEGEND", ImPlotItemFlags_::ImPlotItemFlags_NoLegend)
        .value("ITEM_FLAGS_NO_FIT", ImPlotItemFlags_::ImPlotItemFlags_NoFit)
        .export_values();

    py::enum_<ImPlotLineFlags_>(_implot, "LineFlags", py::arithmetic())
        .value("LINE_FLAGS_NONE", ImPlotLineFlags_::ImPlotLineFlags_None)
        .value("LINE_FLAGS_SEGMENTS", ImPlotLineFlags_::ImPlotLineFlags_Segments)
        .value("LINE_FLAGS_LOOP", ImPlotLineFlags_::ImPlotLineFlags_Loop)
        .value("LINE_FLAGS_SKIP_NA_N", ImPlotLineFlags_::ImPlotLineFlags_SkipNaN)
        .value("LINE_FLAGS_NO_CLIP", ImPlotLineFlags_::ImPlotLineFlags_NoClip)
        .value("LINE_FLAGS_SHADED", ImPlotLineFlags_::ImPlotLineFlags_Shaded)
        .export_values();

    py::enum_<ImPlotScatterFlags_>(_implot, "ScatterFlags", py::arithmetic())
        .value("SCATTER_FLAGS_NONE", ImPlotScatterFlags_::ImPlotScatterFlags_None)
        .value("SCATTER_FLAGS_NO_CLIP", ImPlotScatterFlags_::ImPlotScatterFlags_NoClip)
        .export_values();

    py::enum_<ImPlotStairsFlags_>(_implot, "StairsFlags", py::arithmetic())
        .value("STAIRS_FLAGS_NONE", ImPlotStairsFlags_::ImPlotStairsFlags_None)
        .value("STAIRS_FLAGS_PRE_STEP", ImPlotStairsFlags_::ImPlotStairsFlags_PreStep)
        .value("STAIRS_FLAGS_SHADED", ImPlotStairsFlags_::ImPlotStairsFlags_Shaded)
        .export_values();

    py::enum_<ImPlotShadedFlags_>(_implot, "ShadedFlags", py::arithmetic())
        .value("SHADED_FLAGS_NONE", ImPlotShadedFlags_::ImPlotShadedFlags_None)
        .export_values();

    py::enum_<ImPlotBarsFlags_>(_implot, "BarsFlags", py::arithmetic())
        .value("BARS_FLAGS_NONE", ImPlotBarsFlags_::ImPlotBarsFlags_None)
        .value("BARS_FLAGS_HORIZONTAL", ImPlotBarsFlags_::ImPlotBarsFlags_Horizontal)
        .export_values();

    py::enum_<ImPlotBarGroupsFlags_>(_implot, "BarGroupsFlags", py::arithmetic())
        .value("BAR_GROUPS_FLAGS_NONE", ImPlotBarGroupsFlags_::ImPlotBarGroupsFlags_None)
        .value("BAR_GROUPS_FLAGS_HORIZONTAL", ImPlotBarGroupsFlags_::ImPlotBarGroupsFlags_Horizontal)
        .value("BAR_GROUPS_FLAGS_STACKED", ImPlotBarGroupsFlags_::ImPlotBarGroupsFlags_Stacked)
        .export_values();

    py::enum_<ImPlotErrorBarsFlags_>(_implot, "ErrorBarsFlags", py::arithmetic())
        .value("ERROR_BARS_FLAGS_NONE", ImPlotErrorBarsFlags_::ImPlotErrorBarsFlags_None)
        .value("ERROR_BARS_FLAGS_HORIZONTAL", ImPlotErrorBarsFlags_::ImPlotErrorBarsFlags_Horizontal)
        .export_values();

    py::enum_<ImPlotStemsFlags_>(_implot, "StemsFlags", py::arithmetic())
        .value("STEMS_FLAGS_NONE", ImPlotStemsFlags_::ImPlotStemsFlags_None)
        .value("STEMS_FLAGS_HORIZONTAL", ImPlotStemsFlags_::ImPlotStemsFlags_Horizontal)
        .export_values();

    py::enum_<ImPlotInfLinesFlags_>(_implot, "InfLinesFlags", py::arithmetic())
        .value("INF_LINES_FLAGS_NONE", ImPlotInfLinesFlags_::ImPlotInfLinesFlags_None)
        .value("INF_LINES_FLAGS_HORIZONTAL", ImPlotInfLinesFlags_::ImPlotInfLinesFlags_Horizontal)
        .export_values();

    py::enum_<ImPlotPieChartFlags_>(_implot, "PieChartFlags", py::arithmetic())
        .value("PIE_CHART_FLAGS_NONE", ImPlotPieChartFlags_::ImPlotPieChartFlags_None)
        .value("PIE_CHART_FLAGS_NORMALIZE", ImPlotPieChartFlags_::ImPlotPieChartFlags_Normalize)
        .value("PIE_CHART_FLAGS_IGNORE_HIDDEN", ImPlotPieChartFlags_::ImPlotPieChartFlags_IgnoreHidden)
        .export_values();

    py::enum_<ImPlotHeatmapFlags_>(_implot, "HeatmapFlags", py::arithmetic())
        .value("HEATMAP_FLAGS_NONE", ImPlotHeatmapFlags_::ImPlotHeatmapFlags_None)
        .value("HEATMAP_FLAGS_COL_MAJOR", ImPlotHeatmapFlags_::ImPlotHeatmapFlags_ColMajor)
        .export_values();

    py::enum_<ImPlotHistogramFlags_>(_implot, "HistogramFlags", py::arithmetic())
        .value("HISTOGRAM_FLAGS_NONE", ImPlotHistogramFlags_::ImPlotHistogramFlags_None)
        .value("HISTOGRAM_FLAGS_HORIZONTAL", ImPlotHistogramFlags_::ImPlotHistogramFlags_Horizontal)
        .value("HISTOGRAM_FLAGS_CUMULATIVE", ImPlotHistogramFlags_::ImPlotHistogramFlags_Cumulative)
        .value("HISTOGRAM_FLAGS_DENSITY", ImPlotHistogramFlags_::ImPlotHistogramFlags_Density)
        .value("HISTOGRAM_FLAGS_NO_OUTLIERS", ImPlotHistogramFlags_::ImPlotHistogramFlags_NoOutliers)
        .value("HISTOGRAM_FLAGS_COL_MAJOR", ImPlotHistogramFlags_::ImPlotHistogramFlags_ColMajor)
        .export_values();

    py::enum_<ImPlotDigitalFlags_>(_implot, "DigitalFlags", py::arithmetic())
        .value("DIGITAL_FLAGS_NONE", ImPlotDigitalFlags_::ImPlotDigitalFlags_None)
        .export_values();

    py::enum_<ImPlotImageFlags_>(_implot, "ageFlags", py::arithmetic())
        .value("AGE_FLAGS_NONE", ImPlotImageFlags_::ImPlotImageFlags_None)
        .export_values();

    py::enum_<ImPlotTextFlags_>(_implot, "TextFlags", py::arithmetic())
        .value("TEXT_FLAGS_NONE", ImPlotTextFlags_::ImPlotTextFlags_None)
        .value("TEXT_FLAGS_VERTICAL", ImPlotTextFlags_::ImPlotTextFlags_Vertical)
        .export_values();

    py::enum_<ImPlotDummyFlags_>(_implot, "DummyFlags", py::arithmetic())
        .value("DUMMY_FLAGS_NONE", ImPlotDummyFlags_::ImPlotDummyFlags_None)
        .export_values();

    py::enum_<ImPlotCond_>(_implot, "Cond", py::arithmetic())
        .value("COND_NONE", ImPlotCond_::ImPlotCond_None)
        .value("COND_ALWAYS", ImPlotCond_::ImPlotCond_Always)
        .value("COND_ONCE", ImPlotCond_::ImPlotCond_Once)
        .export_values();

    py::enum_<ImPlotCol_>(_implot, "Col", py::arithmetic())
        .value("COL_LINE", ImPlotCol_::ImPlotCol_Line)
        .value("COL_FILL", ImPlotCol_::ImPlotCol_Fill)
        .value("COL_MARKER_OUTLINE", ImPlotCol_::ImPlotCol_MarkerOutline)
        .value("COL_MARKER_FILL", ImPlotCol_::ImPlotCol_MarkerFill)
        .value("COL_ERROR_BAR", ImPlotCol_::ImPlotCol_ErrorBar)
        .value("COL_FRAME_BG", ImPlotCol_::ImPlotCol_FrameBg)
        .value("COL_PLOT_BG", ImPlotCol_::ImPlotCol_PlotBg)
        .value("COL_PLOT_BORDER", ImPlotCol_::ImPlotCol_PlotBorder)
        .value("COL_LEGEND_BG", ImPlotCol_::ImPlotCol_LegendBg)
        .value("COL_LEGEND_BORDER", ImPlotCol_::ImPlotCol_LegendBorder)
        .value("COL_LEGEND_TEXT", ImPlotCol_::ImPlotCol_LegendText)
        .value("COL_TITLE_TEXT", ImPlotCol_::ImPlotCol_TitleText)
        .value("COL_INLAY_TEXT", ImPlotCol_::ImPlotCol_InlayText)
        .value("COL_AXIS_TEXT", ImPlotCol_::ImPlotCol_AxisText)
        .value("COL_AXIS_GRID", ImPlotCol_::ImPlotCol_AxisGrid)
        .value("COL_AXIS_TICK", ImPlotCol_::ImPlotCol_AxisTick)
        .value("COL_AXIS_BG", ImPlotCol_::ImPlotCol_AxisBg)
        .value("COL_AXIS_BG_HOVERED", ImPlotCol_::ImPlotCol_AxisBgHovered)
        .value("COL_AXIS_BG_ACTIVE", ImPlotCol_::ImPlotCol_AxisBgActive)
        .value("COL_SELECTION", ImPlotCol_::ImPlotCol_Selection)
        .value("COL_CROSSHAIRS", ImPlotCol_::ImPlotCol_Crosshairs)
        .value("COL_COUNT", ImPlotCol_::ImPlotCol_COUNT)
        .export_values();

    py::enum_<ImPlotStyleVar_>(_implot, "StyleVar", py::arithmetic())
        .value("STYLE_VAR_LINE_WEIGHT", ImPlotStyleVar_::ImPlotStyleVar_LineWeight)
        .value("STYLE_VAR_MARKER", ImPlotStyleVar_::ImPlotStyleVar_Marker)
        .value("STYLE_VAR_MARKER_SIZE", ImPlotStyleVar_::ImPlotStyleVar_MarkerSize)
        .value("STYLE_VAR_MARKER_WEIGHT", ImPlotStyleVar_::ImPlotStyleVar_MarkerWeight)
        .value("STYLE_VAR_FILL_ALPHA", ImPlotStyleVar_::ImPlotStyleVar_FillAlpha)
        .value("STYLE_VAR_ERROR_BAR_SIZE", ImPlotStyleVar_::ImPlotStyleVar_ErrorBarSize)
        .value("STYLE_VAR_ERROR_BAR_WEIGHT", ImPlotStyleVar_::ImPlotStyleVar_ErrorBarWeight)
        .value("STYLE_VAR_DIGITAL_BIT_HEIGHT", ImPlotStyleVar_::ImPlotStyleVar_DigitalBitHeight)
        .value("STYLE_VAR_DIGITAL_BIT_GAP", ImPlotStyleVar_::ImPlotStyleVar_DigitalBitGap)
        .value("STYLE_VAR_PLOT_BORDER_SIZE", ImPlotStyleVar_::ImPlotStyleVar_PlotBorderSize)
        .value("STYLE_VAR_MINOR_ALPHA", ImPlotStyleVar_::ImPlotStyleVar_MinorAlpha)
        .value("STYLE_VAR_MAJOR_TICK_LEN", ImPlotStyleVar_::ImPlotStyleVar_MajorTickLen)
        .value("STYLE_VAR_MINOR_TICK_LEN", ImPlotStyleVar_::ImPlotStyleVar_MinorTickLen)
        .value("STYLE_VAR_MAJOR_TICK_SIZE", ImPlotStyleVar_::ImPlotStyleVar_MajorTickSize)
        .value("STYLE_VAR_MINOR_TICK_SIZE", ImPlotStyleVar_::ImPlotStyleVar_MinorTickSize)
        .value("STYLE_VAR_MAJOR_GRID_SIZE", ImPlotStyleVar_::ImPlotStyleVar_MajorGridSize)
        .value("STYLE_VAR_MINOR_GRID_SIZE", ImPlotStyleVar_::ImPlotStyleVar_MinorGridSize)
        .value("STYLE_VAR_PLOT_PADDING", ImPlotStyleVar_::ImPlotStyleVar_PlotPadding)
        .value("STYLE_VAR_LABEL_PADDING", ImPlotStyleVar_::ImPlotStyleVar_LabelPadding)
        .value("STYLE_VAR_LEGEND_PADDING", ImPlotStyleVar_::ImPlotStyleVar_LegendPadding)
        .value("STYLE_VAR_LEGEND_INNER_PADDING", ImPlotStyleVar_::ImPlotStyleVar_LegendInnerPadding)
        .value("STYLE_VAR_LEGEND_SPACING", ImPlotStyleVar_::ImPlotStyleVar_LegendSpacing)
        .value("STYLE_VAR_MOUSE_POS_PADDING", ImPlotStyleVar_::ImPlotStyleVar_MousePosPadding)
        .value("STYLE_VAR_ANNOTATION_PADDING", ImPlotStyleVar_::ImPlotStyleVar_AnnotationPadding)
        .value("STYLE_VAR_FIT_PADDING", ImPlotStyleVar_::ImPlotStyleVar_FitPadding)
        .value("STYLE_VAR_PLOT_DEFAULT_SIZE", ImPlotStyleVar_::ImPlotStyleVar_PlotDefaultSize)
        .value("STYLE_VAR_PLOT_MIN_SIZE", ImPlotStyleVar_::ImPlotStyleVar_PlotMinSize)
        .value("STYLE_VAR_COUNT", ImPlotStyleVar_::ImPlotStyleVar_COUNT)
        .export_values();

    py::enum_<ImPlotScale_>(_implot, "Scale", py::arithmetic())
        .value("SCALE_LINEAR", ImPlotScale_::ImPlotScale_Linear)
        .value("SCALE_TIME", ImPlotScale_::ImPlotScale_Time)
        .value("SCALE_LOG10", ImPlotScale_::ImPlotScale_Log10)
        .value("SCALE_SYM_LOG", ImPlotScale_::ImPlotScale_SymLog)
        .export_values();

    py::enum_<ImPlotMarker_>(_implot, "Marker", py::arithmetic())
        .value("MARKER_NONE", ImPlotMarker_::ImPlotMarker_None)
        .value("MARKER_CIRCLE", ImPlotMarker_::ImPlotMarker_Circle)
        .value("MARKER_SQUARE", ImPlotMarker_::ImPlotMarker_Square)
        .value("MARKER_DIAMOND", ImPlotMarker_::ImPlotMarker_Diamond)
        .value("MARKER_UP", ImPlotMarker_::ImPlotMarker_Up)
        .value("MARKER_DOWN", ImPlotMarker_::ImPlotMarker_Down)
        .value("MARKER_LEFT", ImPlotMarker_::ImPlotMarker_Left)
        .value("MARKER_RIGHT", ImPlotMarker_::ImPlotMarker_Right)
        .value("MARKER_CROSS", ImPlotMarker_::ImPlotMarker_Cross)
        .value("MARKER_PLUS", ImPlotMarker_::ImPlotMarker_Plus)
        .value("MARKER_ASTERISK", ImPlotMarker_::ImPlotMarker_Asterisk)
        .value("MARKER_COUNT", ImPlotMarker_::ImPlotMarker_COUNT)
        .export_values();

    py::enum_<ImPlotColormap_>(_implot, "Colormap", py::arithmetic())
        .value("COLORMAP_DEEP", ImPlotColormap_::ImPlotColormap_Deep)
        .value("COLORMAP_DARK", ImPlotColormap_::ImPlotColormap_Dark)
        .value("COLORMAP_PASTEL", ImPlotColormap_::ImPlotColormap_Pastel)
        .value("COLORMAP_PAIRED", ImPlotColormap_::ImPlotColormap_Paired)
        .value("COLORMAP_VIRIDIS", ImPlotColormap_::ImPlotColormap_Viridis)
        .value("COLORMAP_PLASMA", ImPlotColormap_::ImPlotColormap_Plasma)
        .value("COLORMAP_HOT", ImPlotColormap_::ImPlotColormap_Hot)
        .value("COLORMAP_COOL", ImPlotColormap_::ImPlotColormap_Cool)
        .value("COLORMAP_PINK", ImPlotColormap_::ImPlotColormap_Pink)
        .value("COLORMAP_JET", ImPlotColormap_::ImPlotColormap_Jet)
        .value("COLORMAP_TWILIGHT", ImPlotColormap_::ImPlotColormap_Twilight)
        .value("COLORMAP_RD_BU", ImPlotColormap_::ImPlotColormap_RdBu)
        .value("COLORMAP_BR_BG", ImPlotColormap_::ImPlotColormap_BrBG)
        .value("COLORMAP_PI_YG", ImPlotColormap_::ImPlotColormap_PiYG)
        .value("COLORMAP_SPECTRAL", ImPlotColormap_::ImPlotColormap_Spectral)
        .value("COLORMAP_GREYS", ImPlotColormap_::ImPlotColormap_Greys)
        .export_values();

    py::enum_<ImPlotLocation_>(_implot, "Location", py::arithmetic())
        .value("LOCATION_CENTER", ImPlotLocation_::ImPlotLocation_Center)
        .value("LOCATION_NORTH", ImPlotLocation_::ImPlotLocation_North)
        .value("LOCATION_SOUTH", ImPlotLocation_::ImPlotLocation_South)
        .value("LOCATION_WEST", ImPlotLocation_::ImPlotLocation_West)
        .value("LOCATION_EAST", ImPlotLocation_::ImPlotLocation_East)
        .value("LOCATION_NORTH_WEST", ImPlotLocation_::ImPlotLocation_NorthWest)
        .value("LOCATION_NORTH_EAST", ImPlotLocation_::ImPlotLocation_NorthEast)
        .value("LOCATION_SOUTH_WEST", ImPlotLocation_::ImPlotLocation_SouthWest)
        .value("LOCATION_SOUTH_EAST", ImPlotLocation_::ImPlotLocation_SouthEast)
        .export_values();

    py::enum_<ImPlotBin_>(_implot, "Bin", py::arithmetic())
        .value("BIN_SQRT", ImPlotBin_::ImPlotBin_Sqrt)
        .value("BIN_STURGES", ImPlotBin_::ImPlotBin_Sturges)
        .value("BIN_RICE", ImPlotBin_::ImPlotBin_Rice)
        .value("BIN_SCOTT", ImPlotBin_::ImPlotBin_Scott)
        .export_values();

    PYCLASS_BEGIN(_implot, ImPlotPoint, Point)
        Point.def_readwrite("x", &ImPlotPoint::x);
        Point.def_readwrite("y", &ImPlotPoint::y);
        Point.def(py::init<>());
        Point.def(py::init<double, double>()
        , py::arg("_x")
        , py::arg("_y")
        );
        Point.def(py::init<const ImVec2 &>()
        , py::arg("p")
        );
    PYCLASS_END(_implot, ImPlotPoint, Point)

    PYCLASS_BEGIN(_implot, ImPlotRange, Range)
        Range.def_readwrite("min", &ImPlotRange::Min);
        Range.def_readwrite("max", &ImPlotRange::Max);
        Range.def(py::init<>());
        Range.def(py::init<double, double>()
        , py::arg("_min")
        , py::arg("_max")
        );
        Range.def("contains", &ImPlotRange::Contains
        , py::arg("value")
        , py::return_value_policy::automatic_reference);

        Range.def("size", &ImPlotRange::Size
        , py::return_value_policy::automatic_reference);

        Range.def("clamp", &ImPlotRange::Clamp
        , py::arg("value")
        , py::return_value_policy::automatic_reference);

    PYCLASS_END(_implot, ImPlotRange, Range)

    PYCLASS_BEGIN(_implot, ImPlotRect, Rect)
        Rect.def_readwrite("x", &ImPlotRect::X);
        Rect.def_readwrite("y", &ImPlotRect::Y);
        Rect.def(py::init<>());
        Rect.def(py::init<double, double, double, double>()
        , py::arg("x_min")
        , py::arg("x_max")
        , py::arg("y_min")
        , py::arg("y_max")
        );
        Rect.def("size", &ImPlotRect::Size
        , py::return_value_policy::automatic_reference);

        Rect.def("clamp", py::overload_cast<const ImPlotPoint &>(&ImPlotRect::Clamp)
        , py::arg("p")
        , py::return_value_policy::automatic_reference);

        Rect.def("clamp", py::overload_cast<double, double>(&ImPlotRect::Clamp)
        , py::arg("x")
        , py::arg("y")
        , py::return_value_policy::automatic_reference);

        Rect.def("min", &ImPlotRect::Min
        , py::return_value_policy::automatic_reference);

        Rect.def("max", &ImPlotRect::Max
        , py::return_value_policy::automatic_reference);

    PYCLASS_END(_implot, ImPlotRect, Rect)

    PYCLASS_BEGIN(_implot, ImPlotStyle, Style)
        Style.def_readwrite("line_weight", &ImPlotStyle::LineWeight);
        Style.def_readwrite("marker", &ImPlotStyle::Marker);
        Style.def_readwrite("marker_size", &ImPlotStyle::MarkerSize);
        Style.def_readwrite("marker_weight", &ImPlotStyle::MarkerWeight);
        Style.def_readwrite("fill_alpha", &ImPlotStyle::FillAlpha);
        Style.def_readwrite("error_bar_size", &ImPlotStyle::ErrorBarSize);
        Style.def_readwrite("error_bar_weight", &ImPlotStyle::ErrorBarWeight);
        Style.def_readwrite("digital_bit_height", &ImPlotStyle::DigitalBitHeight);
        Style.def_readwrite("digital_bit_gap", &ImPlotStyle::DigitalBitGap);
        Style.def_readwrite("plot_border_size", &ImPlotStyle::PlotBorderSize);
        Style.def_readwrite("minor_alpha", &ImPlotStyle::MinorAlpha);
        Style.def_readwrite("major_tick_len", &ImPlotStyle::MajorTickLen);
        Style.def_readwrite("minor_tick_len", &ImPlotStyle::MinorTickLen);
        Style.def_readwrite("major_tick_size", &ImPlotStyle::MajorTickSize);
        Style.def_readwrite("minor_tick_size", &ImPlotStyle::MinorTickSize);
        Style.def_readwrite("major_grid_size", &ImPlotStyle::MajorGridSize);
        Style.def_readwrite("minor_grid_size", &ImPlotStyle::MinorGridSize);
        Style.def_readwrite("plot_padding", &ImPlotStyle::PlotPadding);
        Style.def_readwrite("label_padding", &ImPlotStyle::LabelPadding);
        Style.def_readwrite("legend_padding", &ImPlotStyle::LegendPadding);
        Style.def_readwrite("legend_inner_padding", &ImPlotStyle::LegendInnerPadding);
        Style.def_readwrite("legend_spacing", &ImPlotStyle::LegendSpacing);
        Style.def_readwrite("mouse_pos_padding", &ImPlotStyle::MousePosPadding);
        Style.def_readwrite("annotation_padding", &ImPlotStyle::AnnotationPadding);
        Style.def_readwrite("fit_padding", &ImPlotStyle::FitPadding);
        Style.def_readwrite("plot_default_size", &ImPlotStyle::PlotDefaultSize);
        Style.def_readwrite("plot_min_size", &ImPlotStyle::PlotMinSize);
        Style.def_readonly("colors", &ImPlotStyle::Colors);
        Style.def_readwrite("colormap", &ImPlotStyle::Colormap);
        Style.def_readwrite("use_local_time", &ImPlotStyle::UseLocalTime);
        Style.def_readwrite("use_iso8601", &ImPlotStyle::UseISO8601);
        Style.def_readwrite("use24_hour_clock", &ImPlotStyle::Use24HourClock);
        Style.def(py::init<>());
    PYCLASS_END(_implot, ImPlotStyle, Style)

    PYCLASS_BEGIN(_implot, ImPlotInputMap, InputMap)
        InputMap.def_readwrite("pan", &ImPlotInputMap::Pan);
        InputMap.def_readwrite("pan_mod", &ImPlotInputMap::PanMod);
        InputMap.def_readwrite("fit", &ImPlotInputMap::Fit);
        InputMap.def_readwrite("select", &ImPlotInputMap::Select);
        InputMap.def_readwrite("select_cancel", &ImPlotInputMap::SelectCancel);
        InputMap.def_readwrite("select_mod", &ImPlotInputMap::SelectMod);
        InputMap.def_readwrite("select_horz_mod", &ImPlotInputMap::SelectHorzMod);
        InputMap.def_readwrite("select_vert_mod", &ImPlotInputMap::SelectVertMod);
        InputMap.def_readwrite("menu", &ImPlotInputMap::Menu);
        InputMap.def_readwrite("override_mod", &ImPlotInputMap::OverrideMod);
        InputMap.def_readwrite("zoom_mod", &ImPlotInputMap::ZoomMod);
        InputMap.def_readwrite("zoom_rate", &ImPlotInputMap::ZoomRate);
        InputMap.def(py::init<>());
    PYCLASS_END(_implot, ImPlotInputMap, InputMap)

    _implot.def("set_im_gui_context", &ImPlot::SetImGuiContext
    , py::arg("ctx")
    , py::return_value_policy::automatic_reference);

    _implot.def("begin_plot", &ImPlot::BeginPlot
    , py::arg("title_id")
    , py::arg("size") = ImVec2(-1,0)
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);

    _implot.def("end_plot", &ImPlot::EndPlot
    , py::return_value_policy::automatic_reference);

    _implot.def("begin_subplots", [](const char * title_id, int rows, int cols, const ImVec2 & size, ImPlotSubplotFlags flags, float * row_ratios, float * col_ratios)
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
    , py::return_value_policy::automatic_reference);

    _implot.def("end_subplots", &ImPlot::EndSubplots
    , py::return_value_policy::automatic_reference);

    _implot.def("setup_axis", &ImPlot::SetupAxis
    , py::arg("axis")
    , py::arg("label") = nullptr
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);

    _implot.def("setup_axis_limits", &ImPlot::SetupAxisLimits
    , py::arg("axis")
    , py::arg("v_min")
    , py::arg("v_max")
    , py::arg("cond") = ImPlotCond_Once
    , py::return_value_policy::automatic_reference);

    _implot.def("setup_axis_links", [](ImAxis axis, double * link_min, double * link_max)
    {
        ImPlot::SetupAxisLinks(axis, link_min, link_max);
        return std::make_tuple(link_min, link_max);
    }
    , py::arg("axis")
    , py::arg("link_min")
    , py::arg("link_max")
    , py::return_value_policy::automatic_reference);

    _implot.def("setup_axis_format", py::overload_cast<ImAxis, const char *>(&ImPlot::SetupAxisFormat)
    , py::arg("axis")
    , py::arg("fmt")
    , py::return_value_policy::automatic_reference);

    _implot.def("setup_axis_scale", py::overload_cast<ImAxis, ImPlotScale>(&ImPlot::SetupAxisScale)
    , py::arg("axis")
    , py::arg("scale")
    , py::return_value_policy::automatic_reference);

    _implot.def("setup_axis_limits_constraints", &ImPlot::SetupAxisLimitsConstraints
    , py::arg("axis")
    , py::arg("v_min")
    , py::arg("v_max")
    , py::return_value_policy::automatic_reference);

    _implot.def("setup_axis_zoom_constraints", &ImPlot::SetupAxisZoomConstraints
    , py::arg("axis")
    , py::arg("z_min")
    , py::arg("z_max")
    , py::return_value_policy::automatic_reference);

    _implot.def("setup_axes", &ImPlot::SetupAxes
    , py::arg("x_label")
    , py::arg("y_label")
    , py::arg("x_flags") = 0
    , py::arg("y_flags") = 0
    , py::return_value_policy::automatic_reference);

    _implot.def("setup_axes_limits", &ImPlot::SetupAxesLimits
    , py::arg("x_min")
    , py::arg("x_max")
    , py::arg("y_min")
    , py::arg("y_max")
    , py::arg("cond") = ImPlotCond_Once
    , py::return_value_policy::automatic_reference);

    _implot.def("setup_legend", &ImPlot::SetupLegend
    , py::arg("location")
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);

    _implot.def("setup_mouse_text", &ImPlot::SetupMouseText
    , py::arg("location")
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);

    _implot.def("setup_finish", &ImPlot::SetupFinish
    , py::return_value_policy::automatic_reference);

    _implot.def("set_next_axis_limits", &ImPlot::SetNextAxisLimits
    , py::arg("axis")
    , py::arg("v_min")
    , py::arg("v_max")
    , py::arg("cond") = ImPlotCond_Once
    , py::return_value_policy::automatic_reference);

    _implot.def("set_next_axis_links", [](ImAxis axis, double * link_min, double * link_max)
    {
        ImPlot::SetNextAxisLinks(axis, link_min, link_max);
        return std::make_tuple(link_min, link_max);
    }
    , py::arg("axis")
    , py::arg("link_min")
    , py::arg("link_max")
    , py::return_value_policy::automatic_reference);

    _implot.def("set_next_axis_to_fit", &ImPlot::SetNextAxisToFit
    , py::arg("axis")
    , py::return_value_policy::automatic_reference);

    _implot.def("set_next_axes_limits", &ImPlot::SetNextAxesLimits
    , py::arg("x_min")
    , py::arg("x_max")
    , py::arg("y_min")
    , py::arg("y_max")
    , py::arg("cond") = ImPlotCond_Once
    , py::return_value_policy::automatic_reference);

    _implot.def("set_next_axes_to_fit", &ImPlot::SetNextAxesToFit
    , py::return_value_policy::automatic_reference);

    _implot.def("plot_image", &ImPlot::PlotImage
    , py::arg("label_id")
    , py::arg("user_texture_id")
    , py::arg("bounds_min")
    , py::arg("bounds_max")
    , py::arg("uv0") = ImVec2(0,0)
    , py::arg("uv1") = ImVec2(1,1)
    , py::arg("tint_col") = ImVec4(1,1,1,1)
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);

    _implot.def("plot_text", &ImPlot::PlotText
    , py::arg("text")
    , py::arg("x")
    , py::arg("y")
    , py::arg("pix_offset") = ImVec2(0,0)
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);

    _implot.def("plot_dummy", &ImPlot::PlotDummy
    , py::arg("label_id")
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);

    _implot.def("drag_point", [](int id, double * x, double * y, const ImVec4 & col, float size, ImPlotDragToolFlags flags, bool * out_clicked, bool * out_hovered, bool * held)
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
    , py::return_value_policy::automatic_reference);

    _implot.def("drag_line_x", [](int id, double * x, const ImVec4 & col, float thickness, ImPlotDragToolFlags flags, bool * out_clicked, bool * out_hovered, bool * held)
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
    , py::return_value_policy::automatic_reference);

    _implot.def("drag_line_y", [](int id, double * y, const ImVec4 & col, float thickness, ImPlotDragToolFlags flags, bool * out_clicked, bool * out_hovered, bool * held)
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
    , py::return_value_policy::automatic_reference);

    _implot.def("drag_rect", [](int id, double * x1, double * y1, double * x2, double * y2, const ImVec4 & col, ImPlotDragToolFlags flags, bool * out_clicked, bool * out_hovered, bool * held)
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
    , py::return_value_policy::automatic_reference);

    _implot.def("annotation", py::overload_cast<double, double, const ImVec4 &, const ImVec2 &, bool, bool>(&ImPlot::Annotation)
    , py::arg("x")
    , py::arg("y")
    , py::arg("col")
    , py::arg("pix_offset")
    , py::arg("clamp")
    , py::arg("round") = false
    , py::return_value_policy::automatic_reference);

    _implot.def("annotation", [](double x, double y, const ImVec4 & col, const ImVec2 & pix_offset, bool clamp, const char * fmt)
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
    , py::return_value_policy::automatic_reference);

    _implot.def("tag_x", py::overload_cast<double, const ImVec4 &, bool>(&ImPlot::TagX)
    , py::arg("x")
    , py::arg("col")
    , py::arg("round") = false
    , py::return_value_policy::automatic_reference);

    _implot.def("tag_x", [](double x, const ImVec4 & col, const char * fmt)
    {
        ImPlot::TagX(x, col, fmt);
        return ;
    }
    , py::arg("x")
    , py::arg("col")
    , py::arg("fmt")
    , py::return_value_policy::automatic_reference);

    _implot.def("tag_y", py::overload_cast<double, const ImVec4 &, bool>(&ImPlot::TagY)
    , py::arg("y")
    , py::arg("col")
    , py::arg("round") = false
    , py::return_value_policy::automatic_reference);

    _implot.def("tag_y", [](double y, const ImVec4 & col, const char * fmt)
    {
        ImPlot::TagY(y, col, fmt);
        return ;
    }
    , py::arg("y")
    , py::arg("col")
    , py::arg("fmt")
    , py::return_value_policy::automatic_reference);

    _implot.def("set_axis", &ImPlot::SetAxis
    , py::arg("axis")
    , py::return_value_policy::automatic_reference);

    _implot.def("set_axes", &ImPlot::SetAxes
    , py::arg("x_axis")
    , py::arg("y_axis")
    , py::return_value_policy::automatic_reference);

    _implot.def("plot_to_pixels", py::overload_cast<const ImPlotPoint &, ImAxis, ImAxis>(&ImPlot::PlotToPixels)
    , py::arg("plt")
    , py::arg("x_axis") = IMPLOT_AUTO
    , py::arg("y_axis") = IMPLOT_AUTO
    , py::return_value_policy::automatic_reference);

    _implot.def("plot_to_pixels", py::overload_cast<double, double, ImAxis, ImAxis>(&ImPlot::PlotToPixels)
    , py::arg("x")
    , py::arg("y")
    , py::arg("x_axis") = IMPLOT_AUTO
    , py::arg("y_axis") = IMPLOT_AUTO
    , py::return_value_policy::automatic_reference);

    _implot.def("get_plot_pos", &ImPlot::GetPlotPos
    , py::return_value_policy::automatic_reference);

    _implot.def("get_plot_size", &ImPlot::GetPlotSize
    , py::return_value_policy::automatic_reference);

    _implot.def("get_plot_mouse_pos", &ImPlot::GetPlotMousePos
    , py::arg("x_axis") = IMPLOT_AUTO
    , py::arg("y_axis") = IMPLOT_AUTO
    , py::return_value_policy::automatic_reference);

    _implot.def("get_plot_limits", &ImPlot::GetPlotLimits
    , py::arg("x_axis") = IMPLOT_AUTO
    , py::arg("y_axis") = IMPLOT_AUTO
    , py::return_value_policy::automatic_reference);

    _implot.def("is_plot_hovered", &ImPlot::IsPlotHovered
    , py::return_value_policy::automatic_reference);

    _implot.def("is_axis_hovered", &ImPlot::IsAxisHovered
    , py::arg("axis")
    , py::return_value_policy::automatic_reference);

    _implot.def("is_subplots_hovered", &ImPlot::IsSubplotsHovered
    , py::return_value_policy::automatic_reference);

    _implot.def("is_plot_selected", &ImPlot::IsPlotSelected
    , py::return_value_policy::automatic_reference);

    _implot.def("get_plot_selection", &ImPlot::GetPlotSelection
    , py::arg("x_axis") = IMPLOT_AUTO
    , py::arg("y_axis") = IMPLOT_AUTO
    , py::return_value_policy::automatic_reference);

    _implot.def("cancel_plot_selection", &ImPlot::CancelPlotSelection
    , py::return_value_policy::automatic_reference);

    _implot.def("hide_next_item", &ImPlot::HideNextItem
    , py::arg("hidden") = true
    , py::arg("cond") = ImPlotCond_Once
    , py::return_value_policy::automatic_reference);

    _implot.def("begin_aligned_plots", &ImPlot::BeginAlignedPlots
    , py::arg("group_id")
    , py::arg("vertical") = true
    , py::return_value_policy::automatic_reference);

    _implot.def("end_aligned_plots", &ImPlot::EndAlignedPlots
    , py::return_value_policy::automatic_reference);

    _implot.def("begin_legend_popup", &ImPlot::BeginLegendPopup
    , py::arg("label_id")
    , py::arg("mouse_button") = 1
    , py::return_value_policy::automatic_reference);

    _implot.def("end_legend_popup", &ImPlot::EndLegendPopup
    , py::return_value_policy::automatic_reference);

    _implot.def("is_legend_entry_hovered", &ImPlot::IsLegendEntryHovered
    , py::arg("label_id")
    , py::return_value_policy::automatic_reference);

    _implot.def("begin_drag_drop_target_plot", &ImPlot::BeginDragDropTargetPlot
    , py::return_value_policy::automatic_reference);

    _implot.def("begin_drag_drop_target_axis", &ImPlot::BeginDragDropTargetAxis
    , py::arg("axis")
    , py::return_value_policy::automatic_reference);

    _implot.def("begin_drag_drop_target_legend", &ImPlot::BeginDragDropTargetLegend
    , py::return_value_policy::automatic_reference);

    _implot.def("end_drag_drop_target", &ImPlot::EndDragDropTarget
    , py::return_value_policy::automatic_reference);

    _implot.def("begin_drag_drop_source_plot", &ImPlot::BeginDragDropSourcePlot
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);

    _implot.def("begin_drag_drop_source_axis", &ImPlot::BeginDragDropSourceAxis
    , py::arg("axis")
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);

    _implot.def("begin_drag_drop_source_item", &ImPlot::BeginDragDropSourceItem
    , py::arg("label_id")
    , py::arg("flags") = 0
    , py::return_value_policy::automatic_reference);

    _implot.def("end_drag_drop_source", &ImPlot::EndDragDropSource
    , py::return_value_policy::automatic_reference);

    _implot.def("get_style", &ImPlot::GetStyle
    , py::return_value_policy::reference);

    _implot.def("style_colors_auto", &ImPlot::StyleColorsAuto
    , py::arg("dst") = nullptr
    , py::return_value_policy::automatic_reference);

    _implot.def("style_colors_classic", &ImPlot::StyleColorsClassic
    , py::arg("dst") = nullptr
    , py::return_value_policy::automatic_reference);

    _implot.def("style_colors_dark", &ImPlot::StyleColorsDark
    , py::arg("dst") = nullptr
    , py::return_value_policy::automatic_reference);

    _implot.def("style_colors_light", &ImPlot::StyleColorsLight
    , py::arg("dst") = nullptr
    , py::return_value_policy::automatic_reference);

    _implot.def("push_style_color", py::overload_cast<ImPlotCol, ImU32>(&ImPlot::PushStyleColor)
    , py::arg("idx")
    , py::arg("col")
    , py::return_value_policy::automatic_reference);

    _implot.def("push_style_color", py::overload_cast<ImPlotCol, const ImVec4 &>(&ImPlot::PushStyleColor)
    , py::arg("idx")
    , py::arg("col")
    , py::return_value_policy::automatic_reference);

    _implot.def("pop_style_color", &ImPlot::PopStyleColor
    , py::arg("count") = 1
    , py::return_value_policy::automatic_reference);

    _implot.def("push_style_var", py::overload_cast<ImPlotStyleVar, float>(&ImPlot::PushStyleVar)
    , py::arg("idx")
    , py::arg("val")
    , py::return_value_policy::automatic_reference);

    _implot.def("push_style_var", py::overload_cast<ImPlotStyleVar, int>(&ImPlot::PushStyleVar)
    , py::arg("idx")
    , py::arg("val")
    , py::return_value_policy::automatic_reference);

    _implot.def("push_style_var", py::overload_cast<ImPlotStyleVar, const ImVec2 &>(&ImPlot::PushStyleVar)
    , py::arg("idx")
    , py::arg("val")
    , py::return_value_policy::automatic_reference);

    _implot.def("pop_style_var", &ImPlot::PopStyleVar
    , py::arg("count") = 1
    , py::return_value_policy::automatic_reference);

    _implot.def("set_next_line_style", &ImPlot::SetNextLineStyle
    , py::arg("col") = IMPLOT_AUTO_COL
    , py::arg("weight") = IMPLOT_AUTO
    , py::return_value_policy::automatic_reference);

    _implot.def("set_next_fill_style", &ImPlot::SetNextFillStyle
    , py::arg("col") = IMPLOT_AUTO_COL
    , py::arg("alpha_mod") = IMPLOT_AUTO
    , py::return_value_policy::automatic_reference);

    _implot.def("set_next_marker_style", &ImPlot::SetNextMarkerStyle
    , py::arg("marker") = IMPLOT_AUTO
    , py::arg("size") = IMPLOT_AUTO
    , py::arg("fill") = IMPLOT_AUTO_COL
    , py::arg("weight") = IMPLOT_AUTO
    , py::arg("outline") = IMPLOT_AUTO_COL
    , py::return_value_policy::automatic_reference);

    _implot.def("set_next_error_bar_style", &ImPlot::SetNextErrorBarStyle
    , py::arg("col") = IMPLOT_AUTO_COL
    , py::arg("size") = IMPLOT_AUTO
    , py::arg("weight") = IMPLOT_AUTO
    , py::return_value_policy::automatic_reference);

    _implot.def("get_last_item_color", &ImPlot::GetLastItemColor
    , py::return_value_policy::automatic_reference);

    _implot.def("get_style_color_name", &ImPlot::GetStyleColorName
    , py::arg("idx")
    , py::return_value_policy::automatic_reference);

    _implot.def("get_marker_name", &ImPlot::GetMarkerName
    , py::arg("idx")
    , py::return_value_policy::automatic_reference);

    _implot.def("add_colormap", py::overload_cast<const char *, const ImVec4 *, int, bool>(&ImPlot::AddColormap)
    , py::arg("name")
    , py::arg("cols")
    , py::arg("size")
    , py::arg("qual") = true
    , py::return_value_policy::automatic_reference);

    _implot.def("add_colormap", py::overload_cast<const char *, const ImU32 *, int, bool>(&ImPlot::AddColormap)
    , py::arg("name")
    , py::arg("cols")
    , py::arg("size")
    , py::arg("qual") = true
    , py::return_value_policy::automatic_reference);

    _implot.def("get_colormap_count", &ImPlot::GetColormapCount
    , py::return_value_policy::automatic_reference);

    _implot.def("get_colormap_name", &ImPlot::GetColormapName
    , py::arg("cmap")
    , py::return_value_policy::automatic_reference);

    _implot.def("get_colormap_index", &ImPlot::GetColormapIndex
    , py::arg("name")
    , py::return_value_policy::automatic_reference);

    _implot.def("push_colormap", py::overload_cast<ImPlotColormap>(&ImPlot::PushColormap)
    , py::arg("cmap")
    , py::return_value_policy::automatic_reference);

    _implot.def("push_colormap", py::overload_cast<const char *>(&ImPlot::PushColormap)
    , py::arg("name")
    , py::return_value_policy::automatic_reference);

    _implot.def("pop_colormap", &ImPlot::PopColormap
    , py::arg("count") = 1
    , py::return_value_policy::automatic_reference);

    _implot.def("next_colormap_color", &ImPlot::NextColormapColor
    , py::return_value_policy::automatic_reference);

    _implot.def("get_colormap_size", &ImPlot::GetColormapSize
    , py::arg("cmap") = IMPLOT_AUTO
    , py::return_value_policy::automatic_reference);

    _implot.def("get_colormap_color", &ImPlot::GetColormapColor
    , py::arg("idx")
    , py::arg("cmap") = IMPLOT_AUTO
    , py::return_value_policy::automatic_reference);

    _implot.def("sample_colormap", &ImPlot::SampleColormap
    , py::arg("t")
    , py::arg("cmap") = IMPLOT_AUTO
    , py::return_value_policy::automatic_reference);

    _implot.def("colormap_scale", &ImPlot::ColormapScale
    , py::arg("label")
    , py::arg("scale_min")
    , py::arg("scale_max")
    , py::arg("size") = ImVec2(0,0)
    , py::arg("format") = nullptr
    , py::arg("flags") = 0
    , py::arg("cmap") = IMPLOT_AUTO
    , py::return_value_policy::automatic_reference);

    _implot.def("colormap_slider", [](const char * label, float * t, ImVec4 * out, const char * format, ImPlotColormap cmap)
    {
        auto ret = ImPlot::ColormapSlider(label, t, out, format, cmap);
        return std::make_tuple(ret, t);
    }
    , py::arg("label")
    , py::arg("t")
    , py::arg("out") = nullptr
    , py::arg("format") = nullptr
    , py::arg("cmap") = IMPLOT_AUTO
    , py::return_value_policy::automatic_reference);

    _implot.def("colormap_button", &ImPlot::ColormapButton
    , py::arg("label")
    , py::arg("size") = ImVec2(0,0)
    , py::arg("cmap") = IMPLOT_AUTO
    , py::return_value_policy::automatic_reference);

    _implot.def("bust_color_cache", &ImPlot::BustColorCache
    , py::arg("plot_title_id") = nullptr
    , py::return_value_policy::automatic_reference);

    _implot.def("get_input_map", &ImPlot::GetInputMap
    , py::return_value_policy::reference);

    _implot.def("map_input_default", &ImPlot::MapInputDefault
    , py::arg("dst") = nullptr
    , py::return_value_policy::automatic_reference);

    _implot.def("map_input_reverse", &ImPlot::MapInputReverse
    , py::arg("dst") = nullptr
    , py::return_value_policy::automatic_reference);

    _implot.def("item_icon", py::overload_cast<const ImVec4 &>(&ImPlot::ItemIcon)
    , py::arg("col")
    , py::return_value_policy::automatic_reference);

    _implot.def("item_icon", py::overload_cast<ImU32>(&ImPlot::ItemIcon)
    , py::arg("col")
    , py::return_value_policy::automatic_reference);

    _implot.def("colormap_icon", &ImPlot::ColormapIcon
    , py::arg("cmap")
    , py::return_value_policy::automatic_reference);

    _implot.def("get_plot_draw_list", &ImPlot::GetPlotDrawList
    , py::return_value_policy::automatic_reference);

    _implot.def("push_plot_clip_rect", &ImPlot::PushPlotClipRect
    , py::arg("expand") = 0
    , py::return_value_policy::automatic_reference);

    _implot.def("pop_plot_clip_rect", &ImPlot::PopPlotClipRect
    , py::return_value_policy::automatic_reference);

    _implot.def("show_style_selector", &ImPlot::ShowStyleSelector
    , py::arg("label")
    , py::return_value_policy::automatic_reference);

    _implot.def("show_colormap_selector", &ImPlot::ShowColormapSelector
    , py::arg("label")
    , py::return_value_policy::automatic_reference);

    _implot.def("show_input_map_selector", &ImPlot::ShowInputMapSelector
    , py::arg("label")
    , py::return_value_policy::automatic_reference);

    _implot.def("show_style_editor", &ImPlot::ShowStyleEditor
    , py::arg("ref") = nullptr
    , py::return_value_policy::automatic_reference);

    _implot.def("show_user_guide", &ImPlot::ShowUserGuide
    , py::return_value_policy::automatic_reference);

    _implot.def("show_metrics_window", [](bool * p_popen)
    {
        ImPlot::ShowMetricsWindow(p_popen);
        return p_popen;
    }
    , py::arg("p_popen") = nullptr
    , py::return_value_policy::automatic_reference);

    _implot.def("show_demo_window", [](bool * p_open)
    {
        ImPlot::ShowDemoWindow(p_open);
        return p_open;
    }
    , py::arg("p_open") = nullptr
    , py::return_value_policy::automatic_reference);


}