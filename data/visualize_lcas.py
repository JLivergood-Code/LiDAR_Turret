import open3d as o3d
import numpy as np
from lcas_dataset import LCASDataset

# Set this to your REAL dataset folder
root = r"D:\CPE 350\data"

dataset = LCASDataset(root_dir=root, npoints=2048, augment=False)

points, label = dataset[0]
points_np = points.T.numpy()

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points_np)

color_map = {
    0: [1, 0, 0],
    1: [0, 1, 0],
    2: [0, 0, 1],
}

pcd.paint_uniform_color(color_map[int(label)])

print("Label:", int(label))
o3d.visualization.draw_geometries([pcd])
