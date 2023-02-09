from ctypes import c_uint16, c_uint32, c_uint64, c_uint8

"""
#define WGPU_ARRAY_LAYER_COUNT_UNDEFINED (0xffffffffUL)
#define WGPU_COPY_STRIDE_UNDEFINED (0xffffffffUL)
#define WGPU_LIMIT_U32_UNDEFINED (0xffffffffUL)
#define WGPU_LIMIT_U64_UNDEFINED (0xffffffffffffffffULL)
#define WGPU_MIP_LEVEL_COUNT_UNDEFINED (0xffffffffUL)
#define WGPU_STRIDE_UNDEFINED (0xffffffffUL)
#define WGPU_WHOLE_MAP_SIZE SIZE_MAX
#define WGPU_WHOLE_SIZE (0xffffffffffffffffULL)
"""
WGPU_ARRAY_LAYER_COUNT_UNDEFINED = c_uint32(0xffffffff).value
WGPU_COPY_STRIDE_UNDEFINED = c_uint32(0xffffffff).value
WGPU_LIMIT_U32_UNDEFINED = c_uint32(0xffffffff).value
WGPU_LIMIT_U64_UNDEFINED = c_uint64(0xffffffffffffffff).value
WGPU_MIP_LEVEL_COUNT_UNDEFINED = c_uint32(0xffffffff).value
WGPU_STRIDE_UNDEFINED = c_uint32(0xffffffff).value
#define WGPU_WHOLE_MAP_SIZE SIZE_MAX #TODO:?
WGPU_WHOLE_SIZE = c_uint64(0xffffffffffffffff).value
