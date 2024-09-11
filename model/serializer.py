from model.line_segment import LineSegment
from model.point import Point
import jsons


class Solution:
    ply: str
    lines: list[LineSegment]

    def __init__(self, ply: str, lines: list[LineSegment]) -> None:
        self.ply = ply
        self.lines = lines


class Serializer:
    def __init__(self):
        pass

    def to_json(self, line_segments: list[LineSegment], problem_name: str) -> dict:
        all_lines: list[LineSegment] = []
        if line_segments and problem_name:
            for line in line_segments:
                line_points = []
                for point in line.points:
                    points = Point(x=point.x, y=point.y, z=point.z)
                    line_points.append(points)
                all_lines.append(LineSegment(
                    points=line_points, indices=line.line_indices))

        solution = Solution(ply=problem_name, lines=all_lines)
        return jsons.dump(solution)

    def to_line_segment(self, solutions: list[dict]) -> list[dict[str, list[LineSegment]]]:
        """
        Convert all the line segments of JSON format and points in Ply class data.
        It returns a dictionary with the file name. For example: {"basic.ply", list[LineSegment])}
        """
        solution_list: list[dict[str, list[LineSegment]]] = []

        for solution in solutions:
            solution_object = Solution(**solution)
            empty_lines = [{solution_object.ply: []}]
            empty_points = [{solution_object.ply: [LineSegment([])]}]
            all_lines: list[LineSegment] = []

            if solution_object.lines is None or len(solution_object.lines) == 0:
                return empty_lines

            for line in solution_object.lines:
                all_points = []

                if line.get("points") is None or len(line.get("points")) == 0:
                    return empty_points

                for point in line.get("points"):
                    new_point = Point(
                        x=point.get("x"), y=point.get("y"), z=point.get("z"))
                    all_points.append(new_point)

                line_segment = LineSegment(
                    points=all_points, indices=line.get("line_indices"))
                all_lines.append(line_segment)
            _line = {solution_object.ply: all_lines}
            solution_list.append(_line)

        return solution_list
