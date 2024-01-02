include_guard()

# Standard includes
include(GNUInstallDirs)
include(CMakePackageConfigHelpers)
include(CMakeDependentOption)

set(CRUNGE_ROOT ${CMAKE_CURRENT_LIST_DIR}/..)
set(PYBIND11_ROOT ${CRUNGE_ROOT}/depot/pybind11)
set(IMGUI_ROOT ${CRUNGE_ROOT}/depot/imgui)
set(IMPLOT_ROOT ${CRUNGE_ROOT}/depot/implot)
set(IMNODES_ROOT ${CRUNGE_ROOT}/depot/imnodes)

set(DAWN_ROOT ${CRUNGE_ROOT}/depot/dawn)

set(GLTF_ROOT ${WG_ROOT}/depot/gltf)

set(CRUNGE_COMPILE_DEFS 
    NOMINMAX=1
)
