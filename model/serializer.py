import json
from model.line_segment import LineSegment
from model.ply import Ply, Line
from model.point import Point
import jsons


class Serializer:
    def __init__(self, file_path: str):
        self.all_line_segments: dict[str, list[LineSegment]] = {}
        try:
            with open(file_path, 'r') as f:
                self.ply_data = json.load(f)
        except FileExistsError as f:
            raise f

    def serialize_line_segment_in_json(self, line_segments: list[LineSegment], file_name: str) -> dict:
        all_lines = []
        if line_segments and file_name:
            for line in line_segments:
                line_points = []
                for point in line.points:
                    points = Point(x=point.x, y=point.y, z=point.z)
                    line_points.append(points)
                all_lines.append(Line(points=line_points))

        solution = Ply(ply=file_name, lines=all_lines)
        return jsons.dump(solution)

    def get_line_segments_from_json(self) -> dict[str, list[LineSegment]]:
        """
        Reads the JSON file and convert all the line segments of JSON format and points in Ply
        class data. It returns a dictionary with the file name. For example: {'basic.ply', list[LineSegment])}
        """

        for ply in self.ply_data:
            ply_object = Ply(**ply)
            empty_lines = {ply_object.ply: [LineSegment([])]}

            all_lines = []
            if ply_object.lines == None:
                return empty_lines
            for line in ply_object.lines:
                all_points = []
                if line['points'] == None:
                    return empty_lines
                for point in line['points']:
                    new_point = Point(x=point.get(
                        'x'), y=point.get('y'), z=point.get('z'))
                    all_points.append(new_point)
                line_segment = LineSegment(points=all_points)
                all_lines.append(line_segment)

            self.all_line_segments[ply_object.ply] = all_lines
        return self.all_line_segments
