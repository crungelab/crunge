include_guard()

# Standard includes
include(GNUInstallDirs)
include(CMakePackageConfigHelpers)
include(CMakeDependentOption)

set(CRUNGE_ROOT ${CMAKE_CURRENT_LIST_DIR}/..)
set(DEPOT_ROOT ${CRUNGE_ROOT}/depot)

set(PYBIND11_ROOT ${CRUNGE_ROOT}/depot/pybind11)
set(IMGUI_ROOT ${CRUNGE_ROOT}/depot/imgui)
set(IMPLOT_ROOT ${CRUNGE_ROOT}/depot/implot)
set(IMNODES_ROOT ${CRUNGE_ROOT}/depot/imnodes)

#set(DAWN_ROOT ${CRUNGE_ROOT}/depot/dawn)
set(SKIA_ROOT ${CRUNGE_ROOT}/depot/skia)
set(DAWN_ROOT ${SKIA_ROOT}/third_party/externals/dawn)
set(SKIA_LIB_DIR ${SKIA_ROOT}/out/debug)

set(GLTF_ROOT ${CRUNGE_ROOT}/depot/gltf)

set(SDL_ROOT ${CRUNGE_ROOT}/depot/sdl)

set(BVH_ROOT ${CRUNGE_ROOT}/depot/bvh)

set(NANORT_ROOT ${CRUNGE_ROOT}/depot/nanort)

set(CRUNGE_COMPILE_DEFS 
    NOMINMAX=1
)
