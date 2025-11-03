import open3d as o3d
import numpy as np
import os

def convert_pcd_to_npy(pcd_path, out_path):
    pcd = o3d.io.read_point_cloud(pcd_path)
    np.save(out_path, np.asarray(pcd.points))
