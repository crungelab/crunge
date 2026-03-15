from loguru import logger
from crunge.nanort import TriangleMesh


def test_triangle_mesh():
    mesh = TriangleMesh()
    logger.debug(mesh)
    
if __name__ == '__main__':
    test_triangle_mesh()
