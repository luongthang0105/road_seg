from util.ply_parser import parse_ply_file
from .line_segment import LineSegment
from evaluators.interfaces import LineSegmentEvaluator
from model.serializer import Serializer
import json
from texttable import Texttable


class Grader:
    def __init__(self, evaluator_type: LineSegmentEvaluator) -> None:
        self.evalutor = evaluator_type
        pass

    def get_distance_from_ideal_line(self, ideal: LineSegment, actual: LineSegment):
        return self.evalutor.distance_from_ideal(ideal, actual)

    def load_json(self, path: str):
        with open(path, 'r') as f:
            data = json.load(f)
        return data

    def calculate_distances(self, ideal_solutions: dict, solutions: dict) -> None:
        serializer = Serializer()
        ideal_line_segments = serializer.to_line_segment(ideal_solutions)
        solution_line_segments = serializer.to_line_segment(solutions)
        all_min_distances = []
        t = Texttable()
        t.add_row(['Problem Name', 'Line No', 'Minimum Distance'])

        for solution in solution_line_segments:
            for attr, value in enumerate(solution.items()):
                file_name = value[0]
                submission_line_seg = value[1]

                ideal_solution_line_seg = None
                for line in ideal_line_segments:
                    if isinstance(line, dict) and file_name in line:
                        ideal_solution_line_seg = line[file_name]
                        break

                if ideal_solution_line_seg is None:
                    continue

                for index, ideal_line in enumerate(ideal_solution_line_seg):
                    matched_lines = []
                    for submission_line in submission_line_seg:
                        distance = self.get_distance_from_ideal_line(
                            ideal_line, submission_line)
                        matched_lines.append(distance)

                    if matched_lines:
                        min_distance = min(matched_lines)
                        t.add_row([file_name, index, min_distance])
                        all_min_distances.append(min_distance)

        t.add_row(['Total', '', sum(all_min_distances)])
        print(t.draw())
