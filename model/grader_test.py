from model.grader import Grader
from evaluators.frechet import FrechetLineSegmentEvaluator
from model.line_segment import LineSegment
from model.point import Point
import pytest
from texttable import Texttable


@pytest.fixture
def ideal_lines() -> list[dict[str, LineSegment]]:
    return [{"basic.ply": [LineSegment([
        Point(-2.8, 0.1, 0.16),
        Point(0.95, -0.12, 0.16),
        Point(4.5, -1.6, 0.16),
        Point(6.6, -0.39, 0.16),
        Point(5.7, 2.6, 0.16),
        Point(2.9, 3.9, 0.16),
        Point(-1.4, 4.4, 0.16),
    ])]}]


def test_load_json() -> None:
    frechet = FrechetLineSegmentEvaluator()
    grader = Grader(frechet, "./data/tests/ideal_solutions.json",
                    "./data/tests/basic.json")
    ideal_lines = grader._load_json("./data/tests/ideal_solutions.json")
    assert len(ideal_lines) == 1
    assert len(ideal_lines[0]["lines"]) == 4
    assert ideal_lines[0]["ply"] == "roundabout.ply"


def test_load_json_invalid_path() -> None:
    frechet = FrechetLineSegmentEvaluator()
    grader = Grader(frechet, "./data/tests/ideal_solutions.json",
                    "./data/tests/basic.json")
    with pytest.raises(Exception) as exc_info:
        grader._load_json("/my/invalid/path/ideal_solutions.json")
    assert "No such file or directory" in str(exc_info.value)


def test_find_solution_in_ideal(ideal_lines: list[dict[str, LineSegment]]) -> None:
    frechet = FrechetLineSegmentEvaluator()
    grader = Grader(frechet, "./data/tests/ideal_solutions.json",
                    "./data/tests/basic.json")
    lines = grader._find_solution_in_ideal(ideal_lines, "basic.ply")
    assert len(lines) == 1
    assert type(lines) == list


def test_find_solution_in_ideal_not_found(ideal_lines: list[dict[str, LineSegment]]) -> None:
    frechet = FrechetLineSegmentEvaluator()
    grader = Grader(frechet, "./data/tests/ideal_solutions.json",
                    "./data/tests/basic.json")
    lines = grader._find_solution_in_ideal(ideal_lines, "basic_not_found.ply")
    assert lines == []


def test_find_matching_lines() -> None:
    frechet = FrechetLineSegmentEvaluator()
    grader = Grader(frechet, "./data/tests/ideal_solutions.json",
                    "./data/tests/roundabout.json")
    distance = grader._find_matching_lines(
        grader.ideal_line_segments[0]['roundabout.ply'][0], grader.solution_line_segments[0]['roundabout.ply'])
    assert len(distance) == 4
    assert distance[0] == pytest.approx(33.5, rel=1e-2)


def test_find_matching_lines_invalid_input() -> None:
    frechet = FrechetLineSegmentEvaluator()
    grader = Grader(frechet, "./data/tests/ideal_solutions.json",
                    "./data/tests/roundabout.json")
    distance = grader._find_matching_lines(
        "invalid_string_instead_of_line_segment", "invalid_string_instead_of_line_segment")
    assert len(distance) == 0
    assert distance == []


def test_calculate_ideal_and_predicted_distances() -> None:
    frechet = FrechetLineSegmentEvaluator()
    grader = Grader(frechet, "./data/tests/ideal_solutions.json",
                    "./data/tests/roundabout.json")
    min_distances = grader._calculate_ideal_and_predicted_distances(
        "roundabout.ply", grader.ideal_line_segments[0]['roundabout.ply'], grader.solution_line_segments[0]['roundabout.ply'], Texttable())
    assert min_distances[1] == pytest.approx(27.0, rel=1e2)


def test_calculate_ideal_and_predicted_distances_empty_ideal_solution_list() -> None:
    frechet = FrechetLineSegmentEvaluator()
    grader = Grader(frechet, "./data/tests/ideal_solutions.json",
                    "./data/tests/roundabout.json")
    min_distances = grader._calculate_ideal_and_predicted_distances(
        "roundabout.ply", [], grader.solution_line_segments[0]['roundabout.ply'], Texttable())
    assert len(min_distances) == 0
    assert min_distances == []


def test_calculate_ideal_and_predicted_distances_empty_predicted_solution_list() -> None:
    frechet = FrechetLineSegmentEvaluator()
    grader = Grader(frechet, "./data/tests/ideal_solutions.json",
                    "./data/tests/roundabout.json")
    min_distances = grader._calculate_ideal_and_predicted_distances(
        "roundabout.ply", grader.solution_line_segments[0]['roundabout.ply'], [], Texttable())
    assert len(min_distances) == 0
    assert min_distances == []


def test_calculate_ideal_and_predicted_distances_empty_all_empty_lists() -> None:
    frechet = FrechetLineSegmentEvaluator()
    grader = Grader(frechet, "./data/tests/ideal_solutions.json",
                    "./data/tests/roundabout.json")
    min_distances = grader._calculate_ideal_and_predicted_distances(
        "roundabout.ply", [], [], Texttable())
    assert len(min_distances) == 0
    assert min_distances == []


def test_calculate_ideal_and_predicted_distances_invalid_data() -> None:
    frechet = FrechetLineSegmentEvaluator()
    grader = Grader(frechet, "./data/tests/ideal_solutions.json",
                    "./data/tests/roundabout.json")
    min_distances = grader._calculate_ideal_and_predicted_distances(
        "roundabout.ply", "InvalidStringInsteadOfList", "InvalidStringInsteadOfList", Texttable())
    assert len(min_distances) == 0
    assert min_distances == []
