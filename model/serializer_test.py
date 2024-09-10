import pytest
from model.serializer import Serializer
from model.line_segment import LineSegment
from model.point import Point
import json


@pytest.fixture
def serializer():
    return Serializer()


def test_to_line_segment_with_json(serializer) -> None:
    with open('./data/tests/basic.json', 'r') as f:
        data = json.load(f)
    line_segments = serializer.to_line_segment(data)
    assert type(line_segments) == list
    assert type(line_segments[0]['basic.ply']) == list


def test_to_line_segment_with_empty_lines(serializer) -> None:
    with open('./data/tests/basic_no_lines.json', 'r') as f:
        data = json.load(f)
    line_segments = serializer.to_line_segment(data)
    assert len(line_segments[0]['basic.ply']) == 0


def test_to_line_segment_with_empty_points(serializer) -> None:
    with open('./data/tests/basic_no_points.json', 'r') as f:
        data = json.load(f)
    line_segments = serializer.to_line_segment(data)
    assert len(line_segments[0]['basic.ply']) == 1
    assert len(line_segments[0]['basic.ply'][0].points) == 0


def test_to_json(serializer) -> None:
    lines = [
        LineSegment([
            Point(-2.8, 0.1, 0.16),
            Point(0.95, -0.12, 0.16),
            Point(4.5, -1.6, 0.16),
            Point(6.6, -0.39, 0.16),
            Point(5.7, 2.6, 0.16),
            Point(2.9, 3.9, 0.16),
            Point(-1.4, 4.4, 0.16),
        ])]
    line_segments = serializer.to_json(lines, 'basic.ply')
    assert line_segments['ply'] == 'basic.ply'
    assert line_segments['indices'] == None
