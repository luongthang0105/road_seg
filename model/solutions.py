from model.line_segment import LineSegment
from model.serializer import Serializer
from model.ply import Ply
import json


class Solution:

    def __init__(self, output_file: str) -> None:
        self.output_file = output_file
        self.solutions = []
        self.serializer = Serializer()
        pass

    def add_solution(self, problem_name: str, lines: list[LineSegment]):
        self.solutions.append(self.serializer.to_json(lines, problem_name))

    def to_json(self) -> None:
        with open(f'./data/{self.output_file}', 'w') as f:
            json.dump(self.solutions, f)
