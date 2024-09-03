import pytest
from model.grader import Grader
from model.line_segment import LineSegment
import json


@pytest.fixture
def grader():
    return Grader('./data/basic_solution.json')


@pytest.fixture
def point_indices_x():
    with open("./data/basic_solution.json", 'r') as file:
        solution = json.load(file)
        indices_x: list[float] = []
        for item in solution:
            if 'index' in item:
                indices_x.append(item['x'])
    return indices_x


def test_get_points_from_file_path(grader, point_indices_x):
    points = grader.get_points_from_file_path('./data/basic.ply')
    assert len(points) > 0
    assert points[0].x == point_indices_x[0]


def test_get_ideal(grader, point_indices_x):
    ideal_line_segment = grader.get_ideal('./data/basic.ply')
    assert type(ideal_line_segment) == LineSegment
    assert ideal_line_segment.points[1].x == point_indices_x[1]
    assert len(ideal_line_segment.points) == len(point_indices_x)
