from procure import GitSolution

class Pybind11(GitSolution):
	path = 'depot/pybind11'
	url = 'https://github.com/pybind/pybind11'

class ImGui(GitSolution):
	path = 'depot/imgui'
	#url = 'https://github.com/ocornut/imgui'
	url = 'https://github.com/crungelab/imgui'
	#branch = 'docking'
	branch = 'crunge'

class ImPlot(GitSolution):
	path = 'depot/implot'
	url = 'https://github.com/epezent/implot'

class ImPlot(GitSolution):
	path = 'depot/implot'
	url = 'https://github.com/epezent/implot'

class ImNodes(GitSolution):
	path = 'depot/imnodes'
	url = 'https://github.com/Nelarius/imnodes'

class Bgfx(GitSolution):
	path = 'depot/bgfx'
	url = 'https://github.com/bkaradzic/bgfx'

class Bimg(GitSolution):
	path = 'depot/bimg'
	url = 'https://github.com/bkaradzic/bimg'

class Bx(GitSolution):
	path = 'depot/bx'
	url = 'https://github.com/bkaradzic/bx'

class AstcEncoder(GitSolution):
	path = 'depot/astc-encoder'
	url = 'https://github.com/ARM-software/astc-encoder'

class Dawn(GitSolution):
	path = 'depot/dawn'
	url = 'https://dawn.googlesource.com/dawn'

solutions = [
    Pybind11,
    ImGui,
    ImPlot,
    ImNodes,
    Bgfx,
    Bimg,
    Bx,
    AstcEncoder,
	Dawn
]
