from demo.mesh_stats import load_mesh

UNIT_CUBE = """
# unit cube
v 0 0 0
v 1 0 0
v 1 1 0
v 0 1 0
v 0 0 1
v 1 0 1
v 1 1 1
v 0 1 1
f 1 2 3 4
f 5 6 7 8
f 1 2 6 5
f 2 3 7 6
f 3 4 8 7
f 4 1 5 8
"""


def test_unit_cube_counts_and_bounding_box():
    stats = load_mesh(UNIT_CUBE)
    assert stats.vertex_count == 8
    assert stats.face_count == 6
    assert stats.bbox_min == (0.0, 0.0, 0.0)
    assert stats.bbox_max == (1.0, 1.0, 1.0)
