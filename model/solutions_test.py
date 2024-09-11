from model.solution import Solution
from model.line_segment import LineSegment
from model.point import Point
import pytest


@pytest.fixture
def solution():
    return Solution("./data/tests/solutions.json")


def test_add_solution_with_one_solution(solution) -> None:
    solution.add_solution("basic.ply", [LineSegment([
        Point(-2.9, -0.67, 0.16),
        Point(0.85, -0.74, 0.16),
        Point(5.2, -2.5, 0.16),
        Point(7.6, 0.13, 0.16),
        Point(5.7, 3.6, 0.16),
        Point(2.2, 4.9, 0.16),
        Point(-2.1, 5.3, 0.16),
    ])])
    assert len(solution.solutions) == 1


def test_add_solution_with_two_solution(solution) -> None:
    """
    1. The first line is a U shaped line provided in basic.ply
    2. The second line is a bendy line provided in bendy.ply
    """
    solution.add_solution("basic.ply", [LineSegment([
        Point(-2.9, -0.67, 0.16),
        Point(0.85, -0.74, 0.16),
        Point(5.2, -2.5, 0.16),
        Point(7.6, 0.13, 0.16),
        Point(5.7, 3.6, 0.16),
        Point(2.2, 4.9, 0.16),
        Point(-2.1, 5.3, 0.16),
    ])])
    solution.add_solution("bendy.ply", [LineSegment([
        Point(-10.84, 3.70, 0.25),
        Point(-7.75, 4.16, 0.25),
        Point(-3.48, 9.36, 0.25),
        Point(-1.46, 10.22, 0.25),
        Point(6.12, 7.28, 0.25),
        Point(11.20, 9.90, 0.25),
        Point(13.59, 10.10, 0.25),
        Point(14.44, 4.45, 0.25),
        Point(12.78, 1.13, 0.25),
        Point(14.21, -2.88, 0.25),
        Point(13.29, -4.97, 0.25),
        Point(11.81, -6.78, 0.25),
        Point(13.57, -10.23, 0.25),
        Point(9.97, -10.05, 0.25),
        Point(5.98, -5.91, 0.25),
        Point(1.71, -8.70, 0.25),
        Point(-1.23, -8.33, 0.25),
        Point(-1.97, -5.48, 0.25),
        Point(5.82, 2.06, 0.25),
        Point(4.37, 4.08, 0.25),
        Point(-1.20, 2.34, 0.25),
        Point(-5.72, -3.88, 0.25),
        Point(-7.44, -5.28, 0.25)
    ])])
    assert len(solution.solutions) == 2
