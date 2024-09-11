from .line_segment import LineSegment
from evaluators.interfaces import LineSegmentEvaluator
from model.serializer import Serializer
import json
from texttable import Texttable


class Grader:
    def __init__(self, evaluator_type: LineSegmentEvaluator, ideal_solution_path: str, predicted_solution_path: str) -> None:
        self.evalutor = evaluator_type
        self.ideal_solution_path = ideal_solution_path
        self.predicted_solution_path = predicted_solution_path

    def _load_json(self, path: str):
        try:
            with open(path, 'r') as f:
                data = json.load(f)
            return data
        except Exception as e:
            raise e

    def calculate_distances(self) -> None:
        serializer = Serializer()
        ideal_line_segments = serializer.to_line_segment(
            self._load_json(self.ideal_solution_path))
        solution_line_segments = serializer.to_line_segment(
            self._load_json(self.predicted_solution_path))
        all_min_distances = []
        t = Texttable()
        t.add_row(['Problem Name', 'Line No', 'Minimum Distance'])

        for solution in solution_line_segments:
            for key, value in solution.items():

                file_name = key
                submission_line_seg = value

                ideal_solution_line_seg = self._find_solution_in_ideal(
                    ideal_line_segments, file_name)

                if not ideal_solution_line_seg or not submission_line_seg:
                    continue

                for index, ideal_line in enumerate(ideal_solution_line_seg):
                    matched_lines = []
                    for submission_line in submission_line_seg:
                        distance = self.evalutor.distance_from_ideal(
                            ideal_line, submission_line)
                        matched_lines.append(distance)

                    if matched_lines:
                        min_distance = min(matched_lines)
                        t.add_row([file_name, index, min_distance])
                        all_min_distances.append(min_distance)

        t.add_row(['Total', '', sum(all_min_distances)])
        print(t.draw())

    def _find_solution_in_ideal(self, ideal_lines: list[dict[str, list[LineSegment]]], problem_name: str) -> list[LineSegment] | None:
        lines = None
        for line in ideal_lines:
            if isinstance(line, dict) and problem_name in line.keys():
                lines = line[problem_name]
                break
        return lines
