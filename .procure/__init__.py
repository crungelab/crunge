from procure import GitSolution


class Pybind11(GitSolution):
    path = "depot/pybind11"
    url = "https://github.com/pybind/pybind11"


class ImGui(GitSolution):
    path = "depot/imgui"
    url = "https://github.com/ocornut/imgui"
    branch = "docking"
    # url = "https://github.com/crungelab/imgui"
    # branch = "crunge"


class ImPlot(GitSolution):
    path = "depot/implot"
    url = "https://github.com/epezent/implot"


class ImNodes(GitSolution):
    path = "depot/imnodes"
    url = "https://github.com/Nelarius/imnodes"
    # url = "https://github.com/crungelab/imnodes"
    # branch = 'crunge'


class Dawn(GitSolution):
    path = "depot/dawn"
    url = "https://dawn.googlesource.com/dawn"


class TinyGltf(GitSolution):
    path = "depot/gltf"
    # url = "https://github.com/syoyo/tinygltf"
    url = "https://github.com/crungelab/tinygltf"
    branch = "crunge"


class SDL(GitSolution):
    path = "depot/sdl"
    url = "https://github.com/libsdl-org/SDL"


class IconFontCppHeaders(GitSolution):
    path = "depot/iconfontheaders"
    url = "https://github.com/juliettef/IconFontCppHeaders"


class Nanort(GitSolution):
    path = "depot/nanort"
    url = "https://github.com/lighttransport/nanort"


class TmxLite(GitSolution):
    path = "depot/tmxlite"
    url = "https://github.com/fallahn/tmxlite"


solutions = [
    Pybind11,
    ImGui,
    ImPlot,
    ImNodes,
    Dawn,
    TinyGltf,
    SDL,
]
