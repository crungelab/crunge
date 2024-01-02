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

set(BX_ROOT ${CRUNGE_ROOT}/depot/bx)
set(BIMG_ROOT ${CRUNGE_ROOT}/depot/bimg)
set(BGFX_ROOT ${CRUNGE_ROOT}/depot/bgfx)

set(DAWN_ROOT ${CRUNGE_ROOT}/depot/dawn)

set(GLTF_ROOT ${WG_ROOT}/depot/gltf)

set(CRUNGE_COMPILE_DEFS 
    NOMINMAX=1
)

if(CMAKE_SYSTEM_NAME STREQUAL "Windows")
  set(BX_COMPATIBILITY ${BX_ROOT}/include/compat/msvc)
endif()
