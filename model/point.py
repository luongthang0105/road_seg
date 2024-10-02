from typing import Optional
import numpy as np


class Point:
    """
    A point in 3d space, with x, y and z ordinates and rgb/intensity color information
    """

    def __init__(
        self,
        x: float,
        y: float,
        z: float,
        rgb: list[float] = [0, 0, 0],
        intensity: float = 0,
    ):
        self.x = x
        self.y = y
        self.z = z
        self.intensity = intensity
        self.rgb = rgb

    def __repr__(self):
        return f"Point(xyz=({self.x}, {self.y}, {self.z}), rgb={self.rgb}, i={self.intensity})"


class PointList:
    """
    A list of points, represented efficiently using a numpy array.
    """
    X_INDEX: int = 0
    Y_INDEX: int = 1
    Z_INDEX: int = 2
    RGB_START: int = 3
    RGB_END: int = 6
    INTENSITY_INDEX: int = 6

    def __init__(self, raw_points: np.ndarray):
        # Must be 2d, with row size of either 3 or 7
        if len(raw_points.shape) != 2 or raw_points.shape[1] not in [3, 7]:
            raise ValueError("Tried to construct PointList from invalid array")

        if raw_points.shape[1] == 7:
            self._has_extra = True
        elif raw_points.shape[1] == 3:
            self._has_extra = False
        self._raw_points = raw_points

    def has_rgbi(self):
        """
        Returns true if and only if this pointlist has rgb/intensity data
        """
        return self._has_extra

    def x(self) -> np.ndarray:
        """
        Get the x values of the entire pointlist as a flat numpy array
        """
        return self._raw_points[:, PointList.X_INDEX].reshape((-1,))

    def y(self) -> np.ndarray:
        """
        Get the y values of the entire pointlist as a flat numpy array
        """
        return self._raw_points[:, PointList.Y_INDEX].reshape((-1,))

    def z(self) -> np.ndarray:
        """
        Get the z values of the entire pointlist as a flat numpy array
        """
        return self._raw_points[:, PointList.Z_INDEX].reshape((-1,))

    def xyz(self) -> np.ndarray:
        """
        Get the x, y and z values of the entire pointlist as a 2d numpy array.
        Array indexed as `pointlist.xyz()[point_number,axis]`.
        """
        return self._raw_points[:, : PointList.Z_INDEX + 1]

    def rgb(self) -> Optional[np.ndarray]:
        """
        Get the rgb color values of the entire pointlist as a 2d numpy array if self.has_rgbi().
        Array indexed as `pointlist.rgb()[point_number,channel]`.
        """
        if not self.has_rgbi():
            return None
        return self._raw_points[:, PointList.RGB_START : PointList.RGB_END]

    def intensity(self) -> Optional[np.ndarray]:
        """
        Get the intensity color values of the entire pointlist as a flat numpy array if self.has_rgbi().
        """
        if not self.has_rgbi():
            return None
        return self._raw_points[:, PointList.INTENSITY_INDEX]

    def slice(self, start: int, end: int) -> "PointList":
        """
        Create a new PointList consisting of all points in [start, end). This new PointList is indexed
        from 0 to (end-start).
        """
        return PointList(self._raw_points[start:end])

    def get(self, index: int) -> Point:
        """
        Get the nth point of this list as a [Point]
        """
        if index < 0 or index > len(self):
            raise IndexError()
        X = PointList.X_INDEX
        Y = PointList.Y_INDEX
        Z = PointList.Z_INDEX
        p = self._raw_points[index]
        # We say that there is no color if intensity == 0
        if self._has_extra and p[PointList.INTENSITY_INDEX] != 0:
            return Point(
                p[X],
                p[Y],
                p[Z],
                p[PointList.RGB_START : PointList.RGB_END].tolist(),
                p[PointList.INTENSITY_INDEX],
            )
        else:
            return Point(p[X], p[Y], p[Z])

    def raw_points(self) -> np.ndarray:
        """
        Get the raw point data underlying this array, as either an Nx3 or Nx7 numpy array
        """
        return self._raw_points

    def __len__(self) -> int:
        return len(self._raw_points)
