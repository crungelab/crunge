# Symlinks for Development

## Skia and Dawn
```bash
ln -s ../../native/crunge/native pkg/skia/crunge/native
ln -s ../../native/crunge/native pkg/wgpu/crunge/native
```

or

```bash
cd pkg/wgpu/crunge
ln -s ../../core/crunge/native native
```

```bash
cd pkg/skia/crunge
ln -s ../../core/crunge/native native
```

## ImGui's friends

```bash
cd pkg/imnodes/crunge
ln -s ../../imgui/crunge/imgui imgui
```

```bash
cd pkg/implot/crunge
ln -s ../../imgui/crunge/imgui imgui
```

## Skia Patching

```bash
patchelf --set-rpath '$ORIGIN' libdawn_native.so
```