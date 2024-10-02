from model.point import Point
from typing import Optional
from math import sqrt


class LineSegment:
    def __init__(self, points: list[Point], indices: Optional[list[int, int]] = None):
        self.points = points

        # tells us how the points are connected
        self.line_indices = indices

    def get_line_indices(self) -> list[list[int, int]]:
        if self.line_indices:
            return self.line_indices
        else:
            return [[i, i + 1] for i in range(len(self.points) - 1)]

    def length(self) -> float:
        total_length = 0.0
        indices = self.get_line_indices()
        for i1, i2 in indices:
            p1 = self.points[i1]
            p2 = self.points[i2]
            segment_length = sqrt(
                (p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2 + (p2.z - p1.z) ** 2
            )
            total_length += segment_length
        return total_length
