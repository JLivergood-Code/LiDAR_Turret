# LiDAR_Turret
Capstone 350/450 Project

**Two seperate Packages**
- preprocessing package
    - PointCloud.py
- User interface
    - ./UI/pyUI.py

## Preprocessing
THis is a package that includes code to preprocess the files and improve calculation speed of the ML network. Contains the following methods:

- `init_vis()`
    - this boots up the visualizer with key callback
    - useful for debugging and viewing
- `preprocessing(pcd, visualize=False)`
    - Parameters: 
        - open3d point cloud, passed in through memory
        - Visualize: boolean to decide whether to show the output of the preprocessing, does not have smae functionality as key callback, default = False
        - Cluster: Boolean to set whether clusters or not, default = False
    - this is the preprocessing methiod, it will remove noise, crop region, downsample and cluster.

- Other code is helper functions to support visualization and processing

## UI
This package includes everything that is needed to display the UI. It should work with just PySIDE6, but please note that the QT package may need to be installed. Otherwise, requirements.txt should be fine.

-  `pyUI.py`
    - this includes all the backend of the UI, can be update with the helper functions. I will write a method that can take in a target and update on the UI
- `ui_py.qml`
    - this is the QML (QT's version of CSS) that makes everything "mostly" pretty

- TODO
    - Buttons still need implementation, but that would literally take 20-30 minutes to figure out once everything else is created. We just need a way to figure out manual vs automatic firing and I can implement that. Once we figure out the firing mechanism

Required Packages
`pip install -r requirements.txt`
