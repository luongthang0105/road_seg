import pytest
from util.ply_parser import parse_ply_point_list


def gen_test_data(header_fragment, lines):
    return (
        """ply
format ascii 1.0
comment Created in Blender version 4.2.0
element edge 1
property int vertex1
property int vertex2
"""
        + header_fragment
        + """element foo 1
property float bar
end_header
1246 1247
"""
        + lines
        + """ 1.0
"""
    )


def test_load_ply_no_color() -> None:
    test_lines = (
        """-1.1420913 -0.38697618 0.73499984 -280028740 0.92895436 0.30651188\n"""
    )
    test_header = """element vertex 1
property float x
property float y
property float z
property float id
property float UVMap_x
property float UVMap_y
"""
    test_input = gen_test_data(test_header, test_lines)
    points = parse_ply_point_list(test_input)
    assert len(points) == 1
    assert not points.has_rgbi()
    p1 = points.get(0)
    assert p1.rgb == [0, 0, 0]
    assert p1.y == pytest.approx(-0.38697618)


def test_load_ply_color() -> None:
    test_header = """element vertex 3
property float x
property float y
property float z
property float id
property float road_colour_r
property float road_colour_g
property float road_colour_b
property float road_colour_a
property float UVMap_x
property float UVMap_y
property float ground_colour_r
property float ground_colour_g
property float ground_colour_b
property float ground_colour_a
"""
    test_lines = (
        "-1.2311628 0.14745238 0.005 -280028740 0.09070685 0.09070685 0.09070685 0.9 0.8844186 0.5737262 0 0 0 0\n"
        "-1.21 0.15 0.005 -280028740 0 0 0 0 0.8844186 0.5737262 0.09 0.09 0.03 0.2\n"
        "-1.23 0.15 0.005 -280028740 0 0 0 0 0.8844186 0.5737262 0 0 0 0\n"
    )
    test_input = gen_test_data(test_header, test_lines)
    points = parse_ply_point_list(test_input)
    assert len(points) == 3
    assert points.has_rgbi()
    p1 = points.get(0)
    assert p1.rgb == pytest.approx([0.09070685, 0.09070685, 0.09070685])
    assert p1.intensity == pytest.approx(0.9)
    assert p1.y == pytest.approx(0.14745238)
    p2 = points.get(1)
    assert p2.rgb == pytest.approx([0.09, 0.09, 0.03])
    assert p2.intensity == pytest.approx(0.2)
    assert p2.x == pytest.approx(-1.21)
    p3 = points.get(2)
    assert p3.rgb == [0, 0, 0]
    assert p3.intensity == 0
