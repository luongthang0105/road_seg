from model.grader import Grader
from evaluators.frechet import FrechetLineSegmentEvaluator
from model.line_segment import LineSegment
from model.point import Point
import pytest


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


def test_load_json():
    frachet = FrechetLineSegmentEvaluator()
    grader = Grader(frachet, './data/tests/ideal_solutions.json', '')
    ideal_lines = grader._load_json('./data/tests/ideal_solutions.json')
    assert len(ideal_lines) == 1
    assert len(ideal_lines[0]['lines']) == 4
    assert ideal_lines[0]['ply'] == 'roundabout.ply'


def test_load_json_invalid_path():
    frachet = FrechetLineSegmentEvaluator()
    grader = Grader(frachet, '', '')
    with pytest.raises(Exception) as exc_info:
        grader._load_json('/my/invalid/path/ideal_solutions.json')
    assert "No such file or directory" in str(exc_info.value)


def test_find_solution_in_ideal(ideal_lines):
    frachet = FrechetLineSegmentEvaluator()
    grader = Grader(frachet, '', '')
    lines = grader._find_solution_in_ideal(ideal_lines, 'basic.ply')
    assert len(lines) == 1
    assert type(lines) == list


def test_find_solution_in_ideal_not_found(ideal_lines):
    frachet = FrechetLineSegmentEvaluator()
    grader = Grader(frachet, '', '')
    lines = grader._find_solution_in_ideal(ideal_lines, 'basic_not_found.ply')
    assert lines == None
