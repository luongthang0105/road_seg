from model.grader import Grader
from evaluators.frechet import FrechetLineSegmentEvaluator
import pytest


@pytest.fixture
def grader():
    frachet = FrechetLineSegmentEvaluator()
    return Grader(frachet)


def test_load_json(grader):
    ideal_lines = grader.load_json('./data/tests/ideal_solutions.json')
    assert len(ideal_lines) == 1
    assert len(ideal_lines[0]['lines']) == 4
    assert ideal_lines[0]['ply'] == 'roundabout.ply'


def test_load_json_invalid_path(grader):
    with pytest.raises(Exception) as exc_info:
        grader.load_json('./data/testss/ideal_solutions.json')
    assert "No such file or directory" in str(exc_info.value)
