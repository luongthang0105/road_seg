import numpy as np
import open3d as o3d
from model.grader import Grader
import json
pc = o3d.io.read_point_cloud("./data/basic.ply")
vis = o3d.visualization.VisualizerWithEditing()

print(
    "1) Please pick at least three correspondences using [shift + left click]")
print("Press [shift + right click] to undo point picking")
print("2) After picking points, press 'Q' to close the window")
vis.create_window()
vis.add_geometry(pc)
vis.run()  # user picks points
vis.destroy_window()
print("---------")
vis.get_picked_points()

data = []
index = 0

for indice in vis.get_picked_points():
    points = np.asarray(pc.points)[vis.get_picked_points()][index]
    cordinates = {"x": points[0], "y": points[1],
                  "z": points[2], "index": indice}
    data.append(cordinates)
    index += 1
if len(data) > 0:
    with open('./data/basic_solution.json', 'w') as f:
        json.dump(data, f)
