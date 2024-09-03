from util.ply_parser import parse_ply_file
from .line_segment import LineSegment
from model.point import Point
from evaluators.frechet import FrechetLineSegmentEvaluator
import json


class Grader:
    def __init__(self, solution_path: str):
        self.path = solution_path
        self.point_indices: list[int] = []
        self.solution: list = []
        self.get_indices_from_solution()

    def get_indices_from_solution(self):
        with open(self.path, 'r') as file:
            self.solution = json.load(file)
            for item in self.solution:
                if 'index' in item:
                    self.point_indices.append(item['index'])
                else:
                    print(f"Item missing index: {item}")

    def get_points_from_file_path(self, file_path: str) -> list[Point]:
        points: list[Point] = []
        if file_path:
            pc = parse_ply_file(file_path=file_path)
            for indices in self.point_indices:
                points.append(pc[indices])
        return points

    def get_ideal(self, file_path: str) -> LineSegment:
        points = self.get_points_from_file_path(file_path=file_path)
        return LineSegment(points=points)

    def calculate_distance_from_ideal_to_actual(self, ideal: LineSegment,  actual: LineSegment):
        frechet = FrechetLineSegmentEvaluator()
        return frechet.distance_from_ideal(ideal, actual)
