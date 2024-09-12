from .line_segment import LineSegment
from evaluators.interfaces import LineSegmentEvaluator
from model.serializer import Serializer
import json
from texttable import Texttable


class Grader:
    def __init__(self, evaluator_type: LineSegmentEvaluator, ideal_solution_path: str, predicted_solution_path: str) -> None:
        self.evalutor: LineSegmentEvaluator = evaluator_type
        self.serializer: Serializer = Serializer()
        
        self.ideal_line_segments: list[dict[str, list[LineSegment]]] = self.serializer.to_line_segment(self._load_json(ideal_solution_path))
        self.solution_line_segments: list[dict[str, list[LineSegment]]] = self.serializer.to_line_segment(self._load_json(predicted_solution_path))
        self.print_distances(self.ideal_line_segments, self.solution_line_segments)

    def _load_json(self, path: str) -> list[dict]:
        try:
            with open(path, "r") as f:
                data: list[dict] = json.load(f)
            return data
        except Exception as e:
            raise e

    def print_distances(self,
                        ideal_line_segments: list[dict[str, list[LineSegment]]],
                        solution_line_segments: list[dict[str, list[LineSegment]]]) -> None:
        all_min_distances: list[float] = []
        t = Texttable()
        t.add_row(["Problem Name", "Line No", "Minimum Distance"])
 
        for solution in solution_line_segments: 
            for file_name, submission_line_seg in solution.items():
                ideal_solution_line_seg: list[LineSegment] = self._find_solution_in_ideal(ideal_line_segments, file_name)

                if not ideal_solution_line_seg or not submission_line_seg:
                    continue

                min_distances: list[float] = self._calculate_ideal_and_predicted_distances(file_name, ideal_solution_line_seg, submission_line_seg, t)
                all_min_distances.extend(min_distances)
        t.add_row(["Total", "", sum(all_min_distances)])
        print(t.draw())

    def _calculate_ideal_and_predicted_distances(self, file_name: str,
                                  ideal_solution_lines: list[LineSegment],
                                  submission_lines: list[LineSegment],
                                  t: Texttable) -> list[float]:
        min_distances: list[float] = []
        if type(ideal_solution_lines) == list and type(submission_lines) == list:
            for index, ideal_line in enumerate(ideal_solution_lines):
                matched_lines: list[float] = self._find_matching_lines(
                    ideal_line, submission_lines)
                if matched_lines:
                    min_distance: float = min(matched_lines)
                    t.add_row([file_name, index, min_distance])
                    min_distances.append(min_distance)
        return min_distances

    def _find_matching_lines(self, ideal_line: LineSegment, submission_line_seg: list[LineSegment]) -> list[float]:
        if isinstance(ideal_line,LineSegment) and isinstance(submission_line_seg, (list, list[LineSegment])):
            return [self.evalutor.distance_from_ideal(ideal_line, submission_line) for submission_line in submission_line_seg]
        return []

    def _find_solution_in_ideal(self, ideal_line_segments: list[dict[str, list[LineSegment]]], file_name: str) -> list[LineSegment]:
        for ideal in ideal_line_segments:
            if file_name in ideal:
                return ideal[file_name]
        return []
