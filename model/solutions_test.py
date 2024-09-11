from model.solution import Solution
from model.line_segment import LineSegment
from model.point import Point
import pytest
import os


@pytest.fixture
def solution():
    return Solution('./data/tests/solutions.json')


def test_add_solution_with_one_solution(solution) -> None:
    solution.add_solution('basic.ply', [LineSegment([
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
    solution.add_solution('basic.ply', [LineSegment([
        Point(-2.9, -0.67, 0.16),
        Point(0.85, -0.74, 0.16),
        Point(5.2, -2.5, 0.16),
        Point(7.6, 0.13, 0.16),
        Point(5.7, 3.6, 0.16),
        Point(2.2, 4.9, 0.16),
        Point(-2.1, 5.3, 0.16),
    ])])
    solution.add_solution('bendy.ply', [LineSegment([
        Point(-2.9, -0.67, 0.16),
        Point(0.85, -0.74, 0.16),
        Point(5.2, -2.5, 0.16),
        Point(7.6, 0.13, 0.16),
        Point(5.7, 3.6, 0.16),
        Point(2.2, 4.9, 0.16),
        Point(-2.1, 5.3, 0.16),
    ])])
    assert len(solution.solutions) == 2


def test_to_json(solution) -> None:
    try:
        solution.add_solution('basic.ply', [LineSegment([
            Point(-2.9, -0.67, 0.16),
            Point(0.85, -0.74, 0.16),
            Point(5.2, -2.5, 0.16),
            Point(7.6, 0.13, 0.16),
            Point(5.7, 3.6, 0.16),
            Point(2.2, 4.9, 0.16),
            Point(-2.1, 5.3, 0.16),
        ])])
        solution.add_solution('bendy.ply', [LineSegment([
            Point(-2.9, -0.67, 0.16),
            Point(0.85, -0.74, 0.16),
            Point(5.2, -2.5, 0.16),
            Point(7.6, 0.13, 0.16),
            Point(5.7, 3.6, 0.16),
            Point(2.2, 4.9, 0.16),
            Point(-2.1, 5.3, 0.16),
        ])])

        solution.to_json()
        assert os.path.exists("./data/tests/solutions.json") == True
    finally:
        os.remove('./data/tests/solutions.json')
