import json
from model.line_segment import LineSegment
from model.ply import Ply, Line
from model.point import Point


class Serializer:
    def __init__(self, file_path: str):
        self.all_line_segments: dict[str, list[LineSegment]] = {}
        try:
            with open(file_path, 'r') as f:
                self.ply_data = json.load(f)
        except FileExistsError as f:
            raise f

    def get_line_segments(self):
        """
        Reads the JSON file and convert all the line segments of JSON format and points in Ply
        class data. return a dictionary with the file name. For example: {'basic.ply', list[LineSegment])}
        """
        for ply in self.ply_data:
            ply_object = Ply(**ply)
            all_line = []
            for line in ply_object.lines:
                all_points = []
                for point in line['points']:
                    new_point = Point(x=point.get(
                        'x'), y=point.get('y'), z=point.get('z'))
                    all_points.append(new_point)
                line_segment = LineSegment(points=all_points)
                all_line.append(line_segment)

            self.all_line_segments[ply_object.ply] = all_line
        return self.all_line_segments
