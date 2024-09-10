from model.grader import Grader
from evaluators.frechet import FrechetLineSegmentEvaluator
from model.line_segment import LineSegment
from model.point import Point
import pytest


@pytest.fixture
def grader():
    frachet = FrechetLineSegmentEvaluator()
    return Grader(frachet)


@pytest.fixture
def ideal_lines():
    return [{'basic.ply': [LineSegment([
        Point(-2.8, 0.1, 0.16),
        Point(0.95, -0.12, 0.16),
        Point(4.5, -1.6, 0.16),
        Point(6.6, -0.39, 0.16),
        Point(5.7, 2.6, 0.16),
        Point(2.9, 3.9, 0.16),
        Point(-1.4, 4.4, 0.16),
    ])]}]


def test_load_json(grader):
    ideal_lines = grader.load_json('./data/tests/ideal_solutions.json')
    assert len(ideal_lines) == 1
    assert len(ideal_lines[0]['lines']) == 4
    assert ideal_lines[0]['ply'] == 'roundabout.ply'


def test_load_json_invalid_path(grader):
    with pytest.raises(Exception) as exc_info:
        grader.load_json('./data/testss/ideal_solutions.json')
    assert "No such file or directory" in str(exc_info.value)


def test_find_solution_in_ideal(grader, ideal_lines):
    lines = grader._find_solution_in_ideal(ideal_lines, 'basic.ply')
    assert len(lines) == 1
    assert type(lines) == list


def test_find_solution_in_ideal_not_founf(grader, ideal_lines):
    lines = grader._find_solution_in_ideal(ideal_lines, 'basic_not_found.ply')
    assert lines == None
