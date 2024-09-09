from util.ply_parser import parse_ply_file
from .line_segment import LineSegment
from evaluators.interfaces import LineSegmentEvaluator
from model.serializer import Serializer
import json


class Grader:
    def __init__(self, evaluator_type: LineSegmentEvaluator) -> None:
        self.evalutor = evaluator_type
        pass

    def get_distance_ideal_line(self, ideal: LineSegment, actual: LineSegment):
        return self.evalutor.distance_from_ideal(ideal, actual)

    def load_json(self, path: str):
        with open(path, 'r') as f:
            data = json.load(f)
        return data

    def aggregate_distances(self, ideal_solutions: dict, solutions: dict):
        serializer = Serializer()
        ideal_line_segments = serializer.to_line_segment(ideal_solutions)
        solution_line_segments = serializer.to_line_segment(solutions)
        all_distances = []
        for solution in solution_line_segments:
            for attr, value in enumerate(solution.items()):
                file_name = value[0]
                submission_line_seg = value[1]
                ideal_solution_line_seg = next((line[file_name] for line in ideal_line_segments if isinstance(
                    line, dict) and file_name in line), None)
                for ideal_line in ideal_solution_line_seg:
                    matched_lines = []
                    for submission_line in submission_line_seg:
                        distance = self.get_distance_ideal_line(
                            ideal_line, submission_line)
                        matched_lines.append(distance)
                    print(
                        f'Problem: {file_name}, Line No, Distance {min(matched_lines)}')
                    all_distances.append(min(matched_lines))
        print("Accumalated distance ", sum(all_distances))
        return sum(all_distances)
