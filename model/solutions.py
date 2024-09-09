from model.line_segment import LineSegment
from model.serializer import Serializer
from model.ply import Ply
import json


class Solution:

    def __init__(self, file_name: str, line_segments: list[LineSegment]) -> None:
        self.file_name = file_name
        self.line_segments = line_segments
        pass

    def write_solution_in_json(self, line_data) -> None:
        with open('./data/solutions.json', 'w') as f:
            json.dump(line_data, f)

    def read_solution_from_json(self) -> None:
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
            data.append(Serializer(
                './data/solutions.json').serialize_line_segment_in_json(self.line_segments, self.file_name))

        self.write_solution_in_json(data)

    def line_segment_to_json(self) -> None:
        self.read_solution_from_json()

    def has_solution(self, items: list, property_to_search: str) -> bool:
        if not items:
            return False
        return any(item and item.get('ply') == property_to_search for item in items)
