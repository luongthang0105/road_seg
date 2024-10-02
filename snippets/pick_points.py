import open3d as o3d
import numpy as np
import json
file_path = "basic.ply"

pc = o3d.io.read_point_cloud(f"./data/{file_path}")

response = {
    "indices": None,
    "lines": [],
    "ply": file_path
}


def pick_points(pc):
    vis = o3d.visualization.VisualizerWithEditing()
    vis.create_window()
    vis.add_geometry(pc)
    print("Please pick points for a line using [shift + left click].")
    print("Press [shift + right click] to undo point picking.")
    print("Press 'N' to finish picking and save the current line.")
    vis.run()
    vis.destroy_window()
    picked_indices = vis.get_picked_points()
    return picked_indices


def convert_indices_to_data(indices, pc):
    data = []
    for index in indices:
        point = np.asarray(pc.points)[index]
        coordinates = {
            "intensity": 0.0,
            "rgb": [0, 0, 0],
            "x": point[0],
            "y": point[1],
            "z": point[2]
        }
        data.append(coordinates)
    return data


while True:
    indices_line = pick_points(pc)
    data = convert_indices_to_data(indices_line, pc)
    if not data:
        print("No points picked. Exiting...")
        break

    line_data = {"points": data}
    response["lines"].append(line_data)

    with open("./data/basic_solution.json", "w") as f:
        json.dump(response, f, indent=4)

    print("Press 'Enter' to pick another line or 'Q' to quit.")
    user_input = input()
    if user_input.lower() == "q":
        break

print("All lines saved to basic_solution.json.")
