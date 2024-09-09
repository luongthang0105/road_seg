from model.grader import Grader
import json
from model.solutions import Solution
from model.line_segment import LineSegment
from model.point import Point
from evaluators.frechet import FrechetLineSegmentEvaluator

lines = [
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
    ]),
    LineSegment([
        Point(-2.9, -0.67, 0.16),
        Point(0.85, -0.74, 0.16),
        Point(5.2, -2.5, 0.16),
        Point(7.6, 0.13, 0.16),
        Point(5.7, 3.6, 0.16),
        Point(2.2, 4.9, 0.16),
        Point(-2.1, 5.3, 0.16),
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

solution = Solution('roundabout.ply', lines).line_segment_to_json()


# blended = Solution(
#     'blended.ply', line_segment=line[1])

# print(blended)

# subs = Submissions([solution, blended])

frachet = FrechetLineSegmentEvaluator()
subs = Grader(frachet)
