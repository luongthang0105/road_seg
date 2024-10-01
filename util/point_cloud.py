import open3d as o3d
from model.point import Point, PointList
import numpy as np
from model.reduction_strategy import PointCloudReductionStrategy as ReductionStrategy

def create_point_cloud(points: PointList | list[Point]) -> o3d.geometry.PointCloud:
    point_cloud = o3d.geometry.PointCloud()
    if type(points) is list:
        point_cloud.points = o3d.utility.Vector3dVector(
            [[point.x, point.y, point.z] for point in points]
        )
        point_cloud.colors = o3d.utility.Vector3dVector([point.rgb for point in points])
    elif type(points) is PointList:
        point_cloud.points = o3d.utility.Vector3dVector(points.xyz())
        if points.has_rgbi():
            point_cloud.colors = o3d.utility.Vector3dVector(points.rgb())

    return point_cloud


def append_to_point_cloud(
    point_cloud: o3d.geometry.PointCloud, points: list[Point]
) -> None:
    point_cloud.points.extend(
        o3d.utility.Vector3dVector([[point.x, point.y, point.z] for point in points])
    )
    point_cloud.colors.extend(
        o3d.utility.Vector3dVector([np.float(point.rgb) for point in points])
    )

def reduce_point_cloud(
    pc: o3d.geometry.PointCloud, 
    target_size: int = 100000, 
    strategy: ReductionStrategy = ReductionStrategy.RANDOM
) -> o3d.geometry.PointCloud:
    current_size = len(pc.points)
    if current_size <= target_size:
        return pc
    
    if strategy == ReductionStrategy.EVERY_NTH:
        every_nth_point = current_size // target_size
        reduced_points = np.asarray(pc.points)[::every_nth_point]
    elif strategy == ReductionStrategy.RANDOM:
        indices = np.random.choice(current_size, target_size, replace=False)
        reduced_points = np.asarray(pc.points)[indices]
    elif strategy == ReductionStrategy.VOXEL_DOWNSAMPLE:
        voxel_size = 0.01  # Start with a small voxel size
        max_iterations = 10
        for _ in range(max_iterations):
            downsampled = pc.voxel_down_sample(voxel_size)
            if len(downsampled.points) <= target_size:
                return downsampled
            voxel_size *= 1.5  # Increase voxel size and try again
        
        # If we couldn't reach the target size, return the last downsampled version
        return downsampled
    
    reduced_pc = o3d.geometry.PointCloud()
    reduced_pc.points = o3d.utility.Vector3dVector(reduced_points)
    
    if pc.has_colors():
        if strategy == ReductionStrategy.EVERY_NTH:
            reduced_colors = np.asarray(pc.colors)[::every_nth_point]
        elif strategy == ReductionStrategy.RANDOM:
            reduced_colors = np.asarray(pc.colors)[indices]
        reduced_pc.colors = o3d.utility.Vector3dVector(reduced_colors)
    
    return reduced_pc