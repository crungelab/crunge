Next steps:
- To conveniently access emsdk tools from the command line,
  consider adding the following directories to your PATH:
    /home/kurt/Dev/ludi/depot/skia/third_party/externals/emsdk
    /home/kurt/Dev/ludi/depot/skia/third_party/externals/emsdk/upstream/emscripten
- This can be done for the current shell by running:
    source "/home/kurt/Dev/ludi/depot/skia/third_party/externals/emsdk/emsdk_env.sh"
- Configure emsdk in your shell startup scripts by running:
    echo 'source "/home/kurt/Dev/ludi/depot/skia/third_party/externals/emsdk/emsdk_env.sh"' >> $HOME/.bash_profile