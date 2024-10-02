import open3d as o3d
import numpy as np

# Example of how to manually specify points and colors
points = np.array([[0.1, 0.2, 0.3], [0.4, 0.5, 0.6], [0.7, 0.8, 0.9]])

colors = np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]])  # Red  # Green  # Blue

pc = o3d.geometry.PointCloud()
pc.points = o3d.utility.Vector3dVector(points)
pc.colors = o3d.utility.Vector3dVector(colors)

o3d.visualization.draw_geometries([pc])
