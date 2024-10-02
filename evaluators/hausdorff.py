from evaluators.interfaces import LineSegmentEvaluator
from model.line_segment import LineSegment
from model.point import Point
from math import sqrt


# https://en.wikipedia.org/wiki/Hausdorff_distance
class HausdorffLineSegmentEvaluator(LineSegmentEvaluator):
    def distance_from_ideal(self, ideal: LineSegment, actual: LineSegment) -> float:
        return self._hausdorff_distance(ideal, actual)

    def _point_distance(self, p1: Point, p2: Point) -> float:
        return sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2 + (p1.z - p2.z) ** 2)

    def _directed_hausdorff(self, set_a: list[Point], set_b: list[Point]) -> float:
        return max(min(self._point_distance(a, b) for b in set_b) for a in set_a)

    def _hausdorff_distance(self, ideal: LineSegment, actual: LineSegment) -> float:
        d_ab = self._directed_hausdorff(ideal.points, actual.points)
        d_ba = self._directed_hausdorff(actual.points, ideal.points)

        return max(d_ab, d_ba)
