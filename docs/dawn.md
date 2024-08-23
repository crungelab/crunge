[Building Dawn](https://dawn.googlesource.com/dawn/+/refs/heads/main/docs/building.md)

# Without depot tools
```bash
cd depot/dawn
python tools/fetch_dawn_dependencies.py --use-test-deps
```

# With depot tools
```bash
source bin/dt-env
cd depot/dawn
cp scripts/standalone.gclient .gclient
gclient sync
```

## Todo

Extend procure to run post_procure method after procure method