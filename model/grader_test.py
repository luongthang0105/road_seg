from model.grader import Grader
from evaluators.frechet import FrechetLineSegmentEvaluator


def test_aggregate_distances():
    ideal = "./data/tests/ideal_solutions.json"
    actual = "./data/tests/submissions.json"
    frachet = FrechetLineSegmentEvaluator()
    accumalated_distance = Grader(
        evaluator_type=frachet).aggregate_distances(ideal, actual)
