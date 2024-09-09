import pytest
from model.serializer import Serializer
from model.line_segment import LineSegment
from model.point import Point


@pytest.fixture
def solution_json():
    return './data/tests/basic.json'


def test_get_line_segments_return_valid_result(solution_json) -> None:
    ply = Serializer(solution_json).get_line_segments_from_json()
    assert ply['basic.ply'] != None
    assert len(ply['basic.ply']) == 1


def test_get_line_segments_with_invalid_path() -> None:
    with pytest.raises(FileNotFoundError) as exc_info:
        ply = Serializer("./data/tests/no-basic.json")
        ply.get_line_segments_from_json()
    assert "No such file or directory" in str(exc_info.value)


def test_get_line_segments_without_lines() -> None:
    ply = Serializer(
        './data/tests/basic_no_lines.json').get_line_segments_from_json()
    assert ply['basic.ply'] != None
    assert len(ply['basic.ply']) == 0


def test_get_line_segments_without_points() -> None:
    ply = Serializer(
        './data/tests/basic_no_points.json').get_line_segments_from_json()
    assert ply['basic.ply'] != None
    assert len(ply['basic.ply']) == 1
    assert len(ply['basic.ply'][0].points) == 0


def test_serialize_line_segment_in_json() -> None:
    line_segments = [LineSegment([
        Point(-2.9, -0.67, 0.16),
        Point(0.85, -0.74, 0.16),
        Point(5.2, -2.5, 0.16),
        Point(7.6, 0.13, 0.16),
        Point(5.7, 3.6, 0.16),
        Point(2.2, 4.9, 0.16),
        Point(-2.1, 5.3, 0.16),
    ])]
    json = Serializer(
        './data/tests/basic_no_lines.json').serialize_line_segment_in_json(line_segments, 'basic.ply')
    assert json['ply'] == 'basic.ply'
    assert len(json['lines']) == 1
    assert len(json['lines'][0]['points']) == 7
