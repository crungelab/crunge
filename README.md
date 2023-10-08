# Crunge :guitar:

Creative coding extensions for Python using C++ and pybind11

[Dear ImGui](https://github.com/ocornut/imgui)

## OpenGL Libraries Supported

[The Python Arcade Library](https://arcade.academy)

[ModernGL](https://github.com/moderngl/moderngl)

## Required

* [Poetry](https://python-poetry.org/)

## Optional

* [Ninja](https://ninja-build.org/)

## Clone
```bash
git clone https://github.com/crungelab/crunge
cd crunge
poetry shell
poetry install
procure
```

### Build
```bash
cxbuild
```

### Develop
```bash
cxbuild develop
```

## Build crunge-imgui
```bash
cd pkg/imgui
poetry install
python setup.py build
```

### Or
```bash
python setup.py build --build-type Debug
```

### Visual Studio 2019/2022
```bash
python setup.py build -G "Visual Studio 16 2019" --build-type Debug
python setup.py build -G "Visual Studio 17 2022" --build-type Debug
```

## Run the Demo
```bash
cd pkg/imdemo
poetry install
python imdemo
```

### Individual Examples
```bash
python examples/basic.py
etc ...
```

## Build crunge-implot
```bash
cd pkg/implot
poetry install
python setup.py build
```

## Run the Demo
```bash
cd pkg/implotdemo
poetry install
python implotdemo
```

## Run the Demo
```bash
cd pkg/imflodemo
poetry install
python imflodemo
```

# Development

## Tool Chain

[scikit-build](https://github.com/scikit-build/scikit-build)

[pybind11](https://github.com/pybind/pybind11)

## Build

### Generate Bindings
```bash
bindgen gen
```

### Release
```bash
python setup.py build
```

### Debug
```bash
python setup.py build --build-type Debug
```

# Attribution

I'd like to thank the authors of the following repositories for making this possible!

[pyimgui](https://github.com/swistakm/pyimgui)

[deargui](https://github.com/cammm/deargui)