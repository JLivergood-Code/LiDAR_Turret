import open3d as o3d
import numpy as np
import os
import velodyne_decoder as vd
import matplotlib.pyplot as plt 
from functools import partial

# cwd = os.getcwd()

COLOR_MAP = 'jet'



# class PointCloud:
# pcap_file = cwd + pcap_file

def load_points(pcap_file):
    points = []
    for stamp, frame in vd.read_pcap(pcap_file):
        points.append(frame)
        # 2. Create an Open3D PointCloud object

    
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(points[1][:, :3])
    np.save("frame1.npy", points[1])

    intensity = points[1][:, 3]
    intensity_norm = (intensity - np.min(intensity)) / (np.ptp(intensity) + 1e-6)
    # Apply a matplotlib colormap (e.g. 'viridis' or 'jet')
    cmap = plt.get_cmap(COLOR_MAP)
    colors = cmap(intensity_norm)[:, :3]  # Drop alpha channel
    pcd.colors = o3d.utility.Vector3dVector(colors)

    return pcd, points

def init_vis():
    vis = o3d.visualization.VisualizerWithKeyCallback()
    vis.create_window(window_name='Velodyne Viewer')
    return vis

def updateFrameForward(vis, pcd, points, state):
    # loops the the start of the frames
    state['frame_i'] = (state['frame_i'] + 1) % len(points)
    pcd.points = o3d.utility.Vector3dVector(points[state['frame_i']][:, :3])

    # updates color
    intensity = points[state['frame_i']][:, 3]
    intensity_norm = (intensity - np.min(intensity)) / (np.ptp(intensity) + 1e-6)
    # Apply a matplotlib colormap (e.g. 'viridis' or 'jet')
    cmap = plt.get_cmap(COLOR_MAP)
    colors = cmap(intensity_norm)[:, :3]  # Drop alpha channel
    pcd.colors = o3d.utility.Vector3dVector(colors)

    vis.update_geometry(pcd)
    vis.poll_events()
    vis.update_renderer()

def updateFrameBack(vis, state, points, pcd):
    # loops the end of frames
    state['frame_i'] = (state['frame_i'] - 1) if state['frame_i'] > 0 else len(points) - 1
    pcd.points = o3d.utility.Vector3dVector(points[state['frame_i']][:, :3])
    
    # updates color
    intensity = points[state['frame_i']][:, 3]
    intensity_norm = (intensity - np.min(intensity)) / (np.ptp(intensity) + 1e-6)
    # Apply a matplotlib colormap (e.g. 'viridis' or 'jet')
    cmap = plt.get_cmap(COLOR_MAP)
    colors = cmap(intensity_norm)[:, :3]  # Drop alpha channel
    pcd.colors = o3d.utility.Vector3dVector(colors)

    vis.update_geometry(pcd)
    vis.poll_events()
    vis.update_renderer()

def remove_noise(pcd, nb_neighbors=20, std_ratio=2.0):
    filtered_pcd, ind = pcd.remove_statistical_outlier(
        nb_neighbors=nb_neighbors,
        std_ratio=std_ratio
    )
    return filtered_pcd

def downsample(pcd, voxel_size=0.05):
    return pcd.voxel_down_sample(voxel_size=voxel_size)

def cluster_and_display(pcd, eps=0.0075, min_points=10):
    """
    Performs DBSCAN clustering, colors clusters, and visualizes result.
    """
    print("\n--- Running DBSCAN clustering ---")
    labels = np.array(pcd.cluster_dbscan(eps=eps, min_points=min_points, print_progress=True))
    n_clusters = labels.max() + 1
    print(f"Detected {n_clusters} clusters")

    # Assign colors to each cluster
    if n_clusters > 0:
        colors = plt.get_cmap("tab20")(labels / n_clusters)
        colors[labels < 0] = [0, 0, 0, 1]  # noise points = black
        pcd.colors = o3d.utility.Vector3dVector(colors[:, :3])
    else:
        print("No clusters detected.")
        pcd.paint_uniform_color([1, 0, 0])  # fallback color

    # Show result
    o3d.visualization.draw_geometries([pcd], window_name="Clustered Objects (Colored)")
    return labels


def normalize(pcd):
    pts = np.asarray(pcd.points)
    pts -= np.mean(pts, axis=0)
    scale = np.max(np.linalg.norm(pts, axis=1))
    pts /= scale
    pcd.points = o3d.utility.Vector3dVector(pts)
    return pcd


def crop_region(pcd, min_bound=(-5, -5, -1), max_bound=(5, 5, 3)):
    bbox = o3d.geometry.AxisAlignedBoundingBox(min_bound, max_bound)
    return pcd.crop(bbox)

def show(title, *geoms):
    print(f"Showing: {title}")
    o3d.visualization.draw_geometries(geoms)

    

def preprocessing(pcd, visualize=True):
    if visualize:
        show("Raw Point Cloud", pcd)

    # 1. Remove noise
    pcd = remove_noise(pcd)
    if visualize:
        show("After Noise Removal", pcd)

    # 2. Downsample
    pcd = downsample(pcd, voxel_size=0.05)
    if visualize:
        show("After Downsampling", pcd)

    # 3. Ground removal
    # # ground, objects = remove_ground(pcd)
    # if visualize:
    #     ground.paint_uniform_color([0.6, 0.6, 0.6])
    #     objects.paint_uniform_color([1, 0, 0])
    #     show("Ground (gray) and Objects (red)", ground, objects)

    # 4. Normalize
    objects = normalize(pcd)
    if visualize:
        show("Normalized Objects", objects)

    # 5. (Optional) Clustering
    labels = cluster_and_display(objects)
    return labels

def main():

    pcap_file = './PCAP./test2.pcap'

    pcd, points = load_points(pcap_file)

    vis = init_vis()

    vis.add_geometry(pcd)

    state = {'frame_i': 0}

    labels = preprocessing(pcd, True)

    callbackForward = partial(updateFrameForward, pcd=pcd, points=points, state=state)
    callbackBack = partial(updateFrameBack, pcd=pcd, points=points, state=state)

    vis.register_key_callback(262, callbackForward)
    vis.register_key_callback(263, callbackBack)

    vis.run()
    vis.destroy_window()

if __name__ == '__main__':
    print("Starting Program")
    main()

