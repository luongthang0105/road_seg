import pytest
from model.line_segment import LineSegment
from model.point import Point


def test_get_line_indices_returns_indices_if_specified():
    points = []
    indices = [0, 1]
    line_segment = LineSegment(points, indices)

    result = line_segment.get_line_indices()

    assert result == indices


def test_get_line_indices_returns_default_indices_for_1_point():
    points = [Point(0, 0, 0)]
    line_segment = LineSegment(points)
    expected_indices = []

    result = line_segment.get_line_indices()
    assert result == expected_indices


def test_get_line_indices_returns_default_indices_for_2_points():
    points = [Point(0, 0, 0), Point(1, 1, 1)]
    line_segment = LineSegment(points)
    expected_indices = [[0, 1]]

    result = line_segment.get_line_indices()
    assert result == expected_indices


def test_get_line_indices_returns_default_indices_for_3_points():
    points = [Point(0, 0, 0), Point(1, 1, 1), Point(2, 2, 2)]
    line_segment = LineSegment(points)
    expected_indices = [[0, 1], [1, 2]]

    result = line_segment.get_line_indices()
    assert result == expected_indices
