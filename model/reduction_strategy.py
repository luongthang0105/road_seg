from enum import Enum, auto

class PointCloudReductionStrategy(Enum):
    EVERY_NTH = auto()
    RANDOM = auto()
    VOXEL_DOWNSAMPLE = auto()