## Skia

```bash
cd depot
git clone https://github.com/google/skia
cd skia
python tools/git-sync-deps
```

For some reason the partition_alloc symbols are missing so I disabled it.

```bash
bin/gn gen out/debug --args='is_debug=true is_official_build=false is_component_build=true skia_enable_graphite=true skia_use_dawn=true skia_enable_gpu=true skia_use_gl=false skia_use_vulkan=false skia_use_metal=false target_cpu="x64" use_partition_alloc=false'

ninja -C out/debug skia
```