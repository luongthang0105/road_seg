import pytest
import open3d as o3d
import numpy as np
from util.point_cloud import reduce_point_cloud
from model.reduction_strategy import PointCloudReductionStrategy

@pytest.fixture
def sample_point_cloud():
    points = np.random.rand(1000, 3)
    colors = np.random.rand(1000, 3)
    pc = o3d.geometry.PointCloud()
    pc.points = o3d.utility.Vector3dVector(points)
    pc.colors = o3d.utility.Vector3dVector(colors)
    return pc

@pytest.mark.parametrize("strategy", list(PointCloudReductionStrategy))
def test_all_strategies(sample_point_cloud, strategy):
    target_size = 500
    reduced_pc = reduce_point_cloud(sample_point_cloud, target_size, strategy)
    assert len(reduced_pc.points) <= target_size
    assert len(reduced_pc.colors) == len(reduced_pc.points)

def test_reduce_point_cloud_no_reduction_needed(sample_point_cloud):
    target_size = 2000  # Larger than the sample point cloud
    reduced_pc = reduce_point_cloud(sample_point_cloud, target_size)
    assert len(reduced_pc.points) == len(sample_point_cloud.points)
    assert np.allclose(reduced_pc.points, sample_point_cloud.points)

def test_reduce_point_cloud_with_no_colors():
    points = np.random.rand(1000, 3)
    pc = o3d.geometry.PointCloud()
    pc.points = o3d.utility.Vector3dVector(points)
    
    target_size = 500
    reduced_pc = reduce_point_cloud(pc, target_size, PointCloudReductionStrategy.RANDOM)
    assert len(reduced_pc.points) == target_size
    assert not reduced_pc.has_colors()