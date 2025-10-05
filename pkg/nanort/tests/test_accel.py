from crunge.nanort import BVHBuildOptions, BVHAccel

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

def test_accel():
    opts = BVHBuildOptions()

    accel = BVHAccel()

    
if __name__ == '__main__':
    test_accel()
