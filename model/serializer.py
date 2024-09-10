import json
from model.line_segment import LineSegment
from model.ply import Ply, Line
from model.point import Point
import jsons


class Serializer:
    def __init__(self):
        pass

    def to_json(self, line_segments: list[LineSegment], problem_name: str) -> dict:
        all_lines = []
        if line_segments and problem_name:
            for line in line_segments:
                line_points = []
                for point in line.points:
                    points = Point(x=point.x, y=point.y, z=point.z)
                    line_points.append(points)
                all_lines.append(Line(points=line_points))

        solution = Ply(ply=problem_name, lines=all_lines)
        return jsons.dump(solution)

    def to_line_segment(self, ply_data: list) -> list[dict[str, list[LineSegment]]]:
        """
        Convert all the line segments of JSON format and points in Ply class data.
        It returns a dictionary with the file name. For example: {'basic.ply', list[LineSegment])}
        """
        ply_list = []

        for ply in ply_data:
            ply_object = Ply(**ply)
            empty_lines = [{ply_object.ply: []}]
            empty_points = [{ply_object.ply: [LineSegment([])]}]
            all_lines = []

            if ply_object.lines is None or len(ply_object.lines) == 0:
                return empty_lines

            for line in ply_object.lines:
                all_points = []

                if line['points'] is None or len(line['points']) == 0:
                    return empty_points

                for point in line['points']:
                    new_point = Point(x=point.get(
                        'x'), y=point.get('y'), z=point.get('z'))
                    all_points.append(new_point)

                line_segment = LineSegment(points=all_points)
                all_lines.append(line_segment)
            _line = {ply_object.ply: all_lines}
            ply_list.append(_line)

        return ply_list
