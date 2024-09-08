from util.ply_parser import parse_ply_file
from .line_segment import LineSegment
from evaluators.interfaces import LineSegmentEvaluator
from model.serializer import Serializer


class Grader:
    def __init__(self, evaluator_type: LineSegmentEvaluator) -> None:
        self.evalutor = evaluator_type
        self.aggregate_distances()
        pass

    def get_distance_ideal_line(self, ideal: LineSegment, actual: LineSegment):
        return self.evalutor.distance_from_ideal(ideal, actual)

    def aggregate_distances(self):
        submission = Serializer(
            './data/solutions.json').get_line_segments()
        ideal_solutions = Serializer(
            './data/ideal_solutions.json').get_line_segments()
        all_distances = []

        for attr, value in enumerate(submission.items()):
            file_name = value[0]
            submission_line_seg = value[1]
            ideal_solution_line_seg = ideal_solutions[file_name]
            for ideal_line in ideal_solution_line_seg:
                matched_lines = []
                for submission_line in submission_line_seg:
                    distance = self.get_distance_ideal_line(
                        ideal_line, submission_line)
                    matched_lines.append(distance)
                all_distances.append(min(matched_lines))

        print(all_distances)
        print(len(all_distances))
        print(sum(all_distances))
