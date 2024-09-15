import pytest
import numpy as np
from model.point import Point, PointList


def test_point() -> None:
    x = Point(0, 1, 2)
    assert x.y == 1
    assert x.rgb == [0, 0, 0]
    assert str(x) == "Point(xyz=(0, 1, 2), rgb=[0, 0, 0], i=0)"
    y = Point(0, 1, 2, rgb=[0.5, 0.5, 0.1], intensity=2)
    assert str(y) == "Point(xyz=(0, 1, 2), rgb=[0.5, 0.5, 0.1], i=2)"


def test_point_list() -> None:
    d1 = np.array(
        [[0, 0, 0], [1, 1, 1], [2, 1, 1], [1, 2, 1], [1, 2, 3]], dtype=np.float32
    )
    p1 = PointList(d1)
    assert len(p1) == 5
    assert not p1.has_rgbi()
    assert str(p1.get(2)) == "Point(xyz=(2.0, 1.0, 1.0), rgb=[0, 0, 0], i=0)"
    assert np.array_equal(p1.x(), np.array([0, 1, 2, 1, 1]))
    assert p1.rgb() is None
    assert p1.intensity() is None

    d2 = np.array(
        [[0, 0, 0, .5, .5, .5, .2], [1, 1, 1, 2, 3, 4, 3.5]], dtype=np.float32
    )
    p2 = PointList(d2)
    assert len(p2) == 2
    assert p2.has_rgbi()
    assert str(p2.get(1)) == "Point(xyz=(1.0, 1.0, 1.0), rgb=[2.0, 3.0, 4.0], i=3.5)"
    assert np.array_equal(p2.xyz(), np.array([[0, 0, 0], [1, 1, 1]]))
    p2rgb = p2.rgb()
    p2i = p2.intensity()
    assert p2rgb is not None and np.array_equal(p2rgb, np.array([[.5, .5, .5], [2, 3, 4]]))
    assert p2i is not None and np.array_equal(p2i, np.array([.2, 3.5], dtype=np.float32))

    with pytest.raises(IndexError) as _:
        p2.get(-1)

    with pytest.raises(IndexError) as _:
        p2.get(2)

    with pytest.raises(ValueError) as _:
        PointList(np.array([0], dtype=np.float32))

    with pytest.raises(ValueError) as _:
        PointList(np.array([[0], [1]], dtype=np.float32))

    with pytest.raises(ValueError) as _:
        PointList(np.zeros(8, dtype=np.float32).reshape((2,4)))
