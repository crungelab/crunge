#include <dawn/dawn_proc.h>
#include <dawn/native/DawnNative.h>
#include <dawn/webgpu_cpp.h>

using namespace wgpu;

int main(int argc, char** argv) {
    DawnProcTable procs(dawn::native::GetProcs());
    dawnProcSetProcs(&procs);

    Instance instance = CreateInstance();
    return 0;
}
