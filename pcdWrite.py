import open3d as o3d
# import numpy as np
import os, sys
import velodyne_decoder as vd
import shutil
# import matplotlib.pyplot as plt 
# from functools import partial

# def load_points(pcap_file):
    

def main():

    if len(sys.argv) > 1:
        pcap_file = sys.argv[1]
    else:
        print("Must include pcap file or directory path", file=sys.stderr)

    points = []
    file_list = []
    num_frame = 0
    output_dir = "../LiDAR_Turret/data/"

    pcd = o3d.geometry.PointCloud()

    if os.path.isdir(pcap_file):
        dir_content = os.listdir(pcap_file)
        for file in dir_content:
            file_list.append(os.path.join(os.path.abspath(pcap_file), file))
        

    else:
        file_list.append(pcap_file)

    
    # print(f"Directory Output: {file_list}")
    for file_i in range(0, len(file_list)):
        filetype_split = file_list[file_i].split('.')

        # print(filename_split)
        if len(filetype_split) > 1 and filetype_split[1] == 'pcap':
            filename_split = filetype_split[0].split('\\')
            dir_name = os.path.join(output_dir, filename_split[-1])
            
            print(f"Dir Name: {dir_name}\nfilename: {filename_split[-1]}\npcap name: {file_list[file_i]}")

            points.clear()
            pcd.clear()

            try:
                os.makedirs(dir_name, exist_ok=True)
            except FileExistsError as e:
                shutil.rmtree(dir_name)
                os.makedirs(dir_name, exist_ok=True)
            for stamp, frame in vd.read_pcap(file_list[file_i]):
                num_frame += 1
                points.append(frame)
                # print(f"Stamp: {stamp}")
        # 2. Create an Open3D PointCloud object
            print(f"{len(points)}\n")
            for frame_i in range(0, len(points)):
                pcd.points = o3d.utility.Vector3dVector(points[frame_i][:, :3])
                pcd_filename = os.path.join(dir_name, f"{filename_split[-1]}-{frame_i}.pcd")
                o3d.io.write_point_cloud(pcd_filename, pcd)
            # np.save("frame1.npy", points[1])

if __name__ == '__main__':
    main()