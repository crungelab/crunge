from crunge.nanort import BVHBuildOptions

'''
  BVHBuildOptions()
      : cost_t_aabb(0.2f),
        min_leaf_primitives(4),
        max_tree_depth(256),
        bin_size(64),
        shallow_depth(3),
        min_primitives_for_parallel_build(1024 * 128),
        cache_bbox(false) {}
'''

def test_build_options():
    opts = BVHBuildOptions()
    print(opts)
    print(opts.cost_t_aabb)
    print(opts.min_leaf_primitives)
    print(opts.max_tree_depth)
    print(opts.bin_size)
    print(opts.shallow_depth)
    print(opts.min_primitives_for_parallel_build)
    print(opts.cache_bbox)
    '''
    assert opts.min_leaf_primitives == 4
    assert opts.max_tree_depth == 256
    assert opts.bin_size == 64
    assert opts.shallow_depth == 3
    assert opts.min_primitives_for_parallel_build == 1024 * 128
    assert opts.cache_bbox == False
    '''

if __name__ == '__main__':
    test_build_options()
