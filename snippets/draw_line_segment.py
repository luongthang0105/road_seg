import open3d as o3d

pc = o3d.io.read_point_cloud("../data/01-basic.ply")


# Define the line segments
line_points = [[0, 0, 0], [1, 1, 1], [22, 22, 22]]  # List of 3D points
line_indices = [[0, 1], [1, 2], [2, 3]]  # List of line segment indices

# Create a line set
line_set = o3d.geometry.LineSet()
line_set.points = o3d.utility.Vector3dVector(line_points)
line_set.lines = o3d.utility.Vector2iVector(line_indices)
line_set.paint_uniform_color([1, 0, 0])  # Red color

# Visualize the point cloud and the line segments
vis = o3d.visualization.Visualizer()
vis.create_window()
vis.add_geometry(pc)
vis.add_geometry(line_set)
vis.run()
vis.destroy_window()
