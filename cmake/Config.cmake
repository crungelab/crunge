include_guard()

# Standard includes
include(GNUInstallDirs)
include(CMakePackageConfigHelpers)
include(CMakeDependentOption)

set(CRUNGE_ROOT ${CMAKE_CURRENT_LIST_DIR}/..)
set(DEPOT_ROOT ${CRUNGE_ROOT}/depot)

set(PYBIND11_ROOT ${DEPOT_ROOT}/pybind11)
set(IMGUI_ROOT ${DEPOT_ROOT}/imgui)
set(IMPLOT_ROOT ${DEPOT_ROOT}/implot)
set(IMNODES_ROOT ${DEPOT_ROOT}/imnodes)

#set(DAWN_ROOT ${DEPOT_ROOT}/dawn)
set(SKIA_ROOT ${DEPOT_ROOT}/skia)
set(DAWN_ROOT ${SKIA_ROOT}/third_party/externals/dawn)
set(SKIA_LIB_DIR ${SKIA_ROOT}/out/debug)

set(YOGA_ROOT ${DEPOT_ROOT}/yoga)

set(GLTF_ROOT ${DEPOT_ROOT}/tinygltf)

set(SDL_ROOT ${DEPOT_ROOT}/sdl)

set(BVH_ROOT ${DEPOT_ROOT}/bvh)

set(NANORT_ROOT ${DEPOT_ROOT}/nanort)

set(TMX_ROOT ${DEPOT_ROOT}/tmxlite)

set(BOX2D_ROOT ${DEPOT_ROOT}/box2d)

set(RTAUDIO_ROOT ${DEPOT_ROOT}/rtaudio)



set(CRUNGE_COMPILE_DEFS 
    NOMINMAX=1
)
