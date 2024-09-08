from model.point import Point
from typing import Optional


class Line:
    points: list[Point]

    def __init__(self, points: list[Point]) -> None:
        self.points = points


class Ply:
    ply: str
    lines: list[Line]
    indices: Optional[list[list[int]]]

    def __init__(self, ply: str, lines: list[Line], indices: Optional[list[list[int]]] = None) -> None:
        self.ply = ply
        self.lines = lines
        self.indices = indices
