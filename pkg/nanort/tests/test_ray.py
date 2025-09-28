from crunge.nanort import Ray

def test_ray():
    r = Ray((1,2,3), (4,5,6))
    assert r.orig == (1,2,3)
    assert r.dir == (4,5,6)
    assert r.tmin == 0.0
    assert r.tmax == float('inf')
    
    r2 = Ray((1,2,3), (4,5,6), 0.1, 10.0)
    assert r2.orig == (1,2,3)
    assert r2.dir == (4,5,6)
    assert r2.tmin == 0.1
    assert r2.tmax == 10.0