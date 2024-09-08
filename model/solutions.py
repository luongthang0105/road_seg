from model.line_segment import LineSegment
from model.ply import Ply, Line
from model.point import Point
import jsons
import json


class Solution:
    def __init__(self, file_name: str, line_segments: list[LineSegment]) -> None:
        self.file_name = file_name
        self.line_segments = line_segments
        self.line_segment_to_json()
        pass

    def serialize_line_segment(self):
        all_lines = []
        for line in self.line_segments:
            line_points = []
            for point in line.points:
                points = Point(x=point.x, y=point.y, z=point.z)
                line_points.append(points)
            all_lines.append(Line(points=line_points))

        line = all_lines

        solution = Ply(ply=self.file_name, lines=line)
        return jsons.dump(solution)

    def write_solution_in_json(self, line_data):
        with open('./data/solutions.json', 'w') as f:
            json.dump(line_data, f)

    def read_solution_from_json(self):
        try:
            with open('./data/solutions.json', 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            print(f"File not found: {self.file_name}. Creating a new file.")
            data = []
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON for file {self.file_name}: {e}")
            data = []
        except Exception as e:
            print(f"Unexpected error for file {self.file_name}: {e}")
            data = []

        if not self.has_solution(data, self.file_name):
            data.append(self.serialize_line_segment())

        self.write_solution_in_json(data)

    def line_segment_to_json(self):
        self.read_solution_from_json()

    def has_solution(self, items: list, property_to_search: str) -> bool:
        if not items:
            return False
        return any(item and item.get('ply') == property_to_search for item in items)
