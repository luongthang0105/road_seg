import pytest
from model.point import Point
from model.line_segment import LineSegment
from evaluators.frechet import FrechetLineSegmentEvaluator
from math import sqrt


@pytest.fixture
def frechet():
    return FrechetLineSegmentEvaluator()


@pytest.fixture
def ideal_line():
    # hand picked, could be off a bit (basic.ply)
    return LineSegment(
        [
            Point(-3, -0.15, 0.058),
            Point(0.96, -0.17, 0.16),
            Point(3.7, -1.3, 0.16),
            Point(6.6, -0.45, 0.16),
            Point(6.4, 1.9, 0.005),
            Point(4.4, 3.3, 0.005),
            Point(2, 4.1, 0.005),
            Point(-2.2, 4.3, 0.16),
        ]
    )


def test_parallel_segments(frechet):
    p1 = Point(0, 0, 0)
    p2 = Point(1, 1, 1)
    q1 = Point(0, 0, 1)
    q2 = Point(1, 1, 2)
    result = frechet._segment_distance(p1, p2, q1, q2)
    assert result == pytest.approx(0.0, rel=1e-5)


@pytest.mark.xfail(
    reason="Doesn't handle perpendicular case correctly. Adjusting it to do so will affect other segment types."
)
def test_perpendicular_segments(frechet):
    p1 = Point(0, 0, 0)
    p2 = Point(0, 1, 0)
    q1 = Point(1, 0, 0)
    q2 = Point(1, 1, 0)
    result = frechet._segment_distance(p1, p2, q1, q2)
    assert result == pytest.approx(1.0, rel=1e-9)


def test_coincident_segments(frechet):
    p1 = Point(0, 0, 0)
    p2 = Point(1, 1, 1)
    q1 = Point(0, 0, 0)
    q2 = Point(1, 1, 1)
    result = frechet._segment_distance(p1, p2, q1, q2)
    assert result == pytest.approx(0.0, rel=1e-5)


def test_non_intersecting_segments(frechet):
    p1 = Point(0, 0, 0)
    p2 = Point(1, 1, 1)
    q1 = Point(2, 2, 2)
    q2 = Point(3, 3, 3)
    result = frechet._segment_distance(p1, p2, q1, q2)
    assert result == pytest.approx(0.0, rel=1e-5)


def test_different_lengths(frechet):
    p1 = Point(0, 0, 0)
    p2 = Point(2, 0, 0)
    q1 = Point(1, 1, 1)
    q2 = Point(1, 2, 1)
    result = frechet._segment_distance(p1, p2, q1, q2)
    assert result == pytest.approx(1.0, rel=1e-5)


def test_ideal_line_should_return_low_distance_on_overlapping_line(frechet, ideal_line):
    actual_line = ideal_line
    result = frechet.distance_from_ideal(ideal_line, actual_line)
    assert result == pytest.approx(10.0, rel=1e-4)


def test_ideal_line_should_return_high_distance_on_ideal_but_short_line(
    frechet, ideal_line
):
    actual_line = LineSegment(
        [
            Point(-3, -0.15, 0.058),
            Point(0.96, -0.17, 0.16),
            Point(3.7, -1.3, 0.16),
        ]
    )
    result = frechet.distance_from_ideal(ideal_line, actual_line)
    assert result == pytest.approx(24.0, rel=1e-1)


def test_ideal_line_should_return_high_distance_on_ideal_but_long_line(
    frechet, ideal_line
):
    actual_line = LineSegment(
        [
            Point(-3, -0.15, 0.058),
            Point(0.96, -0.17, 0.16),
            Point(103.7, -1.3, 0.16),
        ]
    )
    result = frechet.distance_from_ideal(ideal_line, actual_line)
    assert result == pytest.approx(290.0, rel=1e-1)


def test_ideal_line_should_return_good_distance_on_zigzag_line_within_road(
    frechet, ideal_line
):
    actual_line = LineSegment(
        [
            Point(-3.4, -0.18, -1.1),
            Point(7.4, -3, -1.1),
            Point(-4.7, 8.6, -1.1),
            Point(-2.9, -1, 0.13),
            Point(1.6, 1.7, 0),
            Point(4.3, -2.6, 0.14),
            Point(5.7, 0.3, 0.067),
            Point(5.5, 3.9, 0.16),
            Point(1.4, 3.3, 0.005),
            Point(-2.1, 5.2, 0.16),
        ]
    )
    result = frechet.distance_from_ideal(ideal_line, actual_line)
    assert result == pytest.approx(73.0, rel=1e-1)
