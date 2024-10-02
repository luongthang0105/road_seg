from abc import ABC, abstractmethod
from model.line_segment import LineSegment


class LineSegmentEvaluator(ABC):
    # Lower is better
    @abstractmethod
    def distance_from_ideal(self, ideal: LineSegment, actual: LineSegment) -> float:
        pass
