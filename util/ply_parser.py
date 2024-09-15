from model.point import Point, PointList
import numpy as np
# Going to assume there's only 2 sets of RGBa values. Modify this function if there are more.


def parse_ply_point_list(data) -> PointList:
    lines = data.strip().split("\n")
    header_end_index = 0
    num_props = 0
    points_start = 0
    num_points = None
    current_element = None
    for i, line in enumerate(lines):
        if line.startswith("element "):
            components = line.split(" ")
            current_element = components[1]
            n = int(components[2])
            if current_element == "vertex":
                num_points = n
            elif num_points is None:
                points_start += n
        elif line.startswith("property") and current_element == "vertex":
            num_props += 1
        elif line.startswith("end_header"):
            header_end_index = i
            break

    if num_points is None:
        raise ValueError("Malformed ply, no 'vertex' attribute detected")
    has_color = any(
        attr in headers
        for attr in ["road_colour_a", "ground_colour_a"]
        for headers in lines[:header_end_index]
    )

    if has_color:
        num_features = 7
    else:
        num_features = 3

    assert num_props >= num_features
    # Parse the lines starting from the 15th line
    from_line = header_end_index + points_start + 1
    joined = " ".join(lines[from_line : from_line + num_points])
    values = np.fromstring(joined, dtype=np.float32, sep=" ").reshape(-1, num_props)

    # Extract the x, y, z coordinates
    point_data = values[:, :3]
    if has_color:
        rgbi = np.where(values[:, 4:8] != np.zeros(4), values[:, 4:8], values[:, 10:14])
        point_data = np.concatenate((point_data, rgbi), axis=1)

    return PointList(np.array(point_data).reshape(-1, num_features))


def parse_ply_file_point_list(file_path: str) -> PointList:
    # Read the file
    with open(file_path, "r") as file:
        data = file.read()

    return parse_ply_point_list(data)


def parse_ply_file(file_path: str) -> list[Point]:
    point_list: PointList = parse_ply_file_point_list(file_path)
    points: list[Point] = []
    for i in range(len(point_list)):
        points.append(point_list.get(i))
    return points
