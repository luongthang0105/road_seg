from model.solutions import Solution
from model.line_segment import LineSegment
from model.point import Point
import pytest


@pytest.fixture
def line_segments():
    return [
        LineSegment([
            Point(-2.8, 0.1, 0.16),
            Point(0.95, -0.12, 0.16),
            Point(4.5, -1.6, 0.16),
            Point(6.6, -0.39, 0.16),
            Point(5.7, 2.6, 0.16),
            Point(2.9, 3.9, 0.16),
            Point(-1.4, 4.4, 0.16),
        ]),
        LineSegment([
            Point(-2.9, -0.67, 0.16),
            Point(0.85, -0.74, 0.16),
            Point(5.2, -2.5, 0.16),
            Point(7.6, 0.13, 0.16),
            Point(5.7, 3.6, 0.16),
            Point(2.2, 4.9, 0.16),
            Point(-2.1, 5.3, 0.16),
        ])
    ]


@pytest.fixture
def double_road_solution():
    return [
        {
            "indices": None,
            "lines": [
                {
                    "points": [
                        {
                            "intensity": 0.0,
                            "rgb": [0, 0, 0],
                            "x": -0.32980582,
                            "y": 0.154086,
                            "z": 1.5802343
                        },
                        {
                            "intensity": 0.0,
                            "rgb": [0, 0, 0],
                            "x": -0.3609377,
                            "y": -3.429015,
                            "z": 1.5802343
                        }
                    ]
                }
            ],
            "ply": "double_road.ply"
        }
    ]


def test_has_solution(line_segments, double_road_solution) -> None:
    is_solution_available = Solution(
        'double_raod.ply', line_segments).has_solution(double_road_solution, 'double_road.ply')
    assert is_solution_available == True
