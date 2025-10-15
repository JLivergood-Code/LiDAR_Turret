import open3d as o3d
import numpy as np

# 1. Create a NumPy array of 3D points
# For demonstration, generating 100 random points
points = np.random.rand(100, 3)

# 2. Create an Open3D PointCloud object
pcd = o3d.geometry.PointCloud()

# 3. Assign the points to the PointCloud object
pcd.points = o3d.utility.Vector3dVector(points)

# (Optional) Add colors to the point cloud
# For demonstration, assigning random colors
colors = np.random.rand(100, 3)
pcd.colors = o3d.utility.Vector3dVector(colors)

# 4. Visualize the point cloud
o3d.visualization.draw_geometries([pcd], window_name="My Point Cloud", width=800, height=600)