## Skia

```bash
cd depot
git clone https://github.com/google/skia
cd skia
python tools/git-sync-deps
```

For some reason the partition_alloc symbols are missing so I disabled it.

## Old

```bash
bin/gn gen out/debug --args='is_debug=true is_official_build=false is_component_build=true skia_enable_graphite=true skia_use_dawn=true skia_enable_gpu=true skia_use_gl=false skia_use_vulkan=false skia_use_metal=false target_cpu="x64" use_partition_alloc=false extra_cflags_cc=["-frtti"]'

ninja -C out/debug skia
```

## New

```bash
bin/gn gen out/debug --args='is_debug=true is_official_build=false is_component_build=true skia_enable_graphite=true skia_use_dawn=true skia_use_gl=false skia_use_vulkan=false skia_use_metal=false target_cpu="x64" skia_use_partition_alloc=false extra_cflags_cc=["-frtti"] cc="clang" cxx="clang++"'

ninja -C out/debug skia
```

## Copy to crunge/core
libdawn_native.so
libdawn_platform.so
libdawn_proc.so
libskia.so
libwebgpu_dawn.so
