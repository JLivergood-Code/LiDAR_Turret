import open3d as o3d
import numpy as np
import os
import velodyne_decoder as vd

# cwd = os.getcwd()

pcap_file = './PCAP./test2.pcap'

# pcap_file = cwd + pcap_file

points = []
for stamp, frame in vd.read_pcap(pcap_file):
    points.append(frame)

vis = o3d.visualization.VisualizerWithKeyCallback()
vis.create_window(window_name='Velodyne Viewer')

# 2. Create an Open3D PointCloud object
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(points[1][:, :3])
colors = np.random.rand(100, 3)
pcd.colors = o3d.utility.Vector3dVector(colors)

vis.add_geometry(pcd)

state = {'frame_i': 0}

def updateFrameForward(vis):
    # loops the the start of the frames
    state['frame_i'] = (state['frame_i'] + 1) % len(points)
    pcd.points = o3d.utility.Vector3dVector(points[state['frame_i']][:, :3])
    vis.update_geometry(pcd)
    vis.poll_events()
    vis.update_renderer()

def updateFramBack(vis):
    # loops the end of frames
    state['frame_i'] = (state['frame_i'] - 1) if state['frame_i'] > 0 else len(points) - 1
    pcd.points = o3d.utility.Vector3dVector(points[state['frame_i']][:, :3])
    vis.update_geometry(pcd)
    vis.poll_events()
    vis.update_renderer()

vis.register_key_callback(262, updateFrameForward)
vis.register_key_callback(263, updateFramBack)

vis.run()
vis.destroy_window()

