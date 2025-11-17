# visualize_lcas_corrected.py
import numpy as np
import open3d as o3d
import os

# Paths
pcd_dir = r"D:\CPE 350\data\LCAS_20160523_1200_1218_pcd"
label_dir = r"D:\CPE 350\data\LCAS_20160523_1200_1218_labels"

# Colors
category_colors = {
    'pedestrian': [1, 0, 0],
    'group': [0, 1, 0]
}

pcd_files = sorted([f for f in os.listdir(pcd_dir) if f.endswith('.pcd')])

for base in pcd_files:
    # Load point cloud
    pcd_path = os.path.join(pcd_dir, base)
    pcd = o3d.io.read_point_cloud(pcd_path)
    points = np.asarray(pcd.points, dtype=np.float32)

    # Normalize the **whole cloud** (same as LCASDataset)
    mean = np.mean(points, axis=0)
    points -= mean
    scale = np.max(np.sqrt(np.sum(points**2, axis=1)))
    points /= scale

    # Initialize colors: gray
    colors = np.ones_like(points) * 0.7

    # Load labels
    label_path = os.path.join(label_dir, base.replace('.pcd', '.txt'))
    with open(label_path, 'r') as f:
        for line in f:
            parts = line.strip().split()
            cat = parts[0].lower()
            coords = np.array(list(map(float, parts[1:10]))).reshape(3, 3)

            # Normalize bounding box **using same mean & scale**
            coords = (coords - mean) / scale
            min_corner = coords.min(axis=0)
            max_corner = coords.max(axis=0)

            # Mask points inside bounding box
            mask = np.all((points >= min_corner) & (points <= max_corner), axis=1)
            if cat in category_colors:
                colors[mask] = category_colors[cat]

    # Apply colors and visualize
    pcd.colors = o3d.utility.Vector3dVector(colors)
    o3d.visualization.draw_geometries([pcd], window_name=base, width=800, height=600)
