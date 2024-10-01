import open3d as o3d
from typing import Callable
import open3d as o3d
import time


class NonBlockingVisualizer:
    def __init__(
        self,
        point_cloud: o3d.geometry.PointCloud,
        update_function: Callable[[], o3d.geometry.LineSet],
    ):
        self.update_function = update_function
        self.vis: o3d.visualization.VisualizerWithKeyCallback = (
            o3d.visualization.VisualizerWithKeyCallback()
        )
        self.vis.create_window(
            window_name="Non-Blocking Visualizer", width=800, height=600
        )
        self.line_set = o3d.geometry.LineSet()  # Initial line set
        self.vis.add_geometry(self.line_set)
        self.vis.add_geometry(point_cloud)
        self.running = False
        self.last_update_time = 0
        self.update_interval = 0.03  # Update every 30ms for smooth animation

    def start(self):
        self.running = True
        self.run_visualization()

    def run_visualization(self):
        t = 0
        while self.running:
            updated_line_set = self.update_function(t)
            self.line_set.points = updated_line_set.points
            self.line_set.lines = updated_line_set.lines
            self.line_set.colors = updated_line_set.colors

            self.vis.update_geometry(self.line_set)
            if not self.vis.poll_events():
                break
            self.vis.update_renderer()

            time.sleep(self.update_interval)
            t += self.update_interval
        self.stop()

    def stop(self):
        self.running = False
        self.vis.destroy_window()
