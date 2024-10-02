from evaluators.interfaces import LineSegmentEvaluator
from model.line_segment import LineSegment
from model.point import Point
from math import sqrt


# https://en.wikipedia.org/wiki/Fr%C3%A9chet_distance
class FrechetLineSegmentEvaluator(LineSegmentEvaluator):
    def distance_from_ideal(self, ideal: LineSegment, actual: LineSegment) -> float:
        # Calculate the Fréchet distance between the ideal and actual line segments
        frechet_distance = self._frechet_distance(ideal, actual)
        length_diff = abs(ideal.length() - actual.length())
        # penalize differences in length
        return frechet_distance + length_diff

    # p1 and p2 are segment 1 (ideal) points, q1 and q2 are segment 2 (actual) points
    def _segment_distance(self, p1: Point, p2: Point, q1: Point, q2: Point):
        dx, dy, dz = q2.x - q1.x, q2.y - q1.y, q2.z - q1.z
        nx, ny, nz = p2.x - p1.x, p2.y - p1.y, p2.z - p1.z
        return sqrt(dx * dx + dy * dy + dz * dz) - (dx * nx + dy * ny + dz * nz) / sqrt(
            nx * nx + ny * ny + nz * nz
        )

    def _frechet_distance(self, ideal: LineSegment, actual: LineSegment):
        max_distance = 0
        for i1, i2 in ideal.get_line_indices():
            for j1, j2 in actual.get_line_indices():
                p1, p2 = ideal.points[i1], ideal.points[i2]
                q1, q2 = actual.points[j1], actual.points[j2]

                d_p1_q1 = sqrt(
                    (p1.x - q1.x) * (p1.x - q1.x)
                    + (p1.y - q1.y) * (p1.y - q1.y)
                    + (p1.z - q1.z) * (p1.z - q1.z)
                )
                d_p1_q2 = sqrt(
                    (p1.x - q2.x) * (p1.x - q2.x)
                    + (p1.y - q2.y) * (p1.y - q2.y)
                    + (p1.z - q2.z) * (p1.z - q2.z)
                )
                d_p2_q1 = sqrt(
                    (p2.x - q1.x) * (p2.x - q1.x)
                    + (p2.y - q1.y) * (p2.y - q1.y)
                    + (p2.z - q1.z) * (p2.z - q1.z)
                )
                d_p2_q2 = sqrt(
                    (p2.x - q2.x) * (p2.x - q2.x)
                    + (p2.y - q2.y) * (p2.y - q2.y)
                    + (p2.z - q2.z) * (p2.z - q2.z)
                )

                max_distance = max(
                    max_distance,
                    d_p1_q1,
                    d_p1_q2,
                    d_p2_q1,
                    d_p2_q2,
                    self._segment_distance(p1, p2, q1, q2),
                )

        return max_distance
