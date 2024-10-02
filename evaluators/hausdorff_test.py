import pytest
from model.point import Point
from model.line_segment import LineSegment
from evaluators.hausdorff import HausdorffLineSegmentEvaluator
from math import sqrt


@pytest.fixture
def hausdorff():
    return HausdorffLineSegmentEvaluator()


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


def test_ideal_line_should_return_low_distance_on_overlapping_line(
    hausdorff, ideal_line
):
    actual_line = ideal_line
    result = hausdorff.distance_from_ideal(ideal_line, actual_line)
    assert result == pytest.approx(0.0, rel=1e-5)


def test_ideal_line_should_return_high_distance_on_ideal_but_short_line(
    hausdorff, ideal_line
):
    actual_line = LineSegment(
        [
            Point(-3, -0.15, 0.058),
            Point(0.96, -0.17, 0.16),
            Point(3.7, -1.3, 0.16),
        ]
    )
    result = hausdorff.distance_from_ideal(ideal_line, actual_line)
    assert result == pytest.approx(4.65, rel=1e-1)


def test_ideal_line_should_return_high_distance_on_ideal_but_long_line(
    hausdorff, ideal_line
):
    actual_line = LineSegment(
        [
            Point(-3, -0.15, 0.058),
            Point(0.96, -0.17, 0.16),
            Point(103.7, -1.3, 0.16),
        ]
    )
    result = hausdorff.distance_from_ideal(ideal_line, actual_line)
    assert result == pytest.approx(97.0, rel=1e-2)


def test_ideal_line_should_return_good_distance_on_zigzag_line_within_road(
    hausdorff, ideal_line
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
    result = hausdorff.distance_from_ideal(ideal_line, actual_line)
    assert result == pytest.approx(5.0, rel=1e-1)
