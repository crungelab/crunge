```bash
cd pkg/wgpu/crunge
ln -s ../../core/crunge/core core
```

```bash
cd pkg/skia/crunge
ln -s ../../core/crunge/core core
```

```bash
cd pkg/imnodes/crunge
ln -s ../../imgui/crunge/imgui imgui
```

```bash
cd pkg/implot/crunge
ln -s ../../imgui/crunge/imgui imgui
```

```bash
patchelf --set-rpath '$ORIGIN' libdawn_native.so
```