import pytest
from model.serializer import Serializer


@pytest.fixture
def solution_json():
    return './data/tests/basic.json'


def test_get_line_segments_return_valid_result(solution_json):
    ply = Serializer(solution_json).get_line_segments()
    assert ply['basic.ply'] != None
    assert len(ply['basic.ply']) == 1


def test_get_line_segments_with_invalid_path():
    with pytest.raises(FileNotFoundError) as exc_info:
        ply = Serializer("./data/tests/no-basic.json")
        ply.get_line_segments()
    assert "No such file or directory" in str(exc_info.value)
