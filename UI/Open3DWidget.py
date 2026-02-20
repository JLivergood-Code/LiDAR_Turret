import sys
import open3d as o3d
import open3d.visualization.gui as gui # type: ignore
import open3d.visualization.rendering as rendering # type: ignore
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout
from PySide6.QtCore import QTimer
import PySide6.QtGui as QtGui

try:
    import win32gui
except ImportError:
    from subprocess import Popen, PIPE
    import PySide6.QtGui as QtGui

try:
    import win32gui
except ImportError:
    from subprocess import Popen, PIPE

class Open3DWidget(QWidget):
    def __init__(self, parent=None):
        super(Open3DWidget, self).__init__(parent)
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)

        # 1. Initialize Open3D GUI application (singleton instance)
        gui.Application.instance.initialize()

        # 2. Create an Open3D window and retrieve its native window ID
        self.o3d_window = gui.Application.instance.create_window("Open3D Viewer", 800, 600)

        # 3. Create a QWindow from the Open3D window ID and wrap it with QWidget
        #    This allows it to be embedded within the PySide layout
         # hwnd = win32gui.FindWindowEx(0, 0, None, "Open3D")
        try:
            print(f"Running on win32gui")
            hwnd = win32gui.FindWindowEx(0, 0, None, "Open3D Viewer")        
        except ImportError:
            print(f"Running on unix (wmctrl)")
            hwnd = self.get_unix_hwnd()
        
        self.window = QtGui.QWindow.fromWinId(hwnd) 
        self.o3d_widget = QWidget.createWindowContainer(self.window)
        self.layout().addWidget(self.o3d_widget)

        # 4. Set up an Open3D SceneWidget
        self.scene_widget = gui.SceneWidget()
        self.scene_widget.scene = rendering.Open3DScene(self.o3d_window.renderer)
        self.o3d_window.add_child(self.scene_widget)

        # 5. Add a 3D geometry (e.g., a simple coordinate frame)
        # You can replace this with your point cloud or mesh loading
        # coordinate_frame = o3d.geometry.create_coordinate_frame(size=0.5)
        pcd = o3d.io.read_point_cloud("./LiDAR_Turret/data/street/street-0.pcd")
        
        self.setGeometry(pcd)

        # 6. Use a QTimer to run the Open3D event loop periodically
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_o3d)
        self.timer.start(10) # 10 ms interval

    def setGeometry(self, pcd):
        self.scene_widget.scene.remove_geometry("pcd")
        self.scene_widget.scene.add_geometry("pcd", pcd, o3d.visualization.rendering.MaterialRecord())
        bbox = pcd.get_axis_aligned_bounding_box()
        self.scene_widget.setup_camera(60.0, bbox, bbox.get_center())

    def update_o3d(self):
        # This function processes the Open3D GUI events
        gui.Application.instance.run_one_tick()

    def get_unix_hwnd(self):
        hwnd = None
        while hwnd == None:
            proc = Popen('wmctrl -l', stdin=None, stdout=PIPE, stderr=None, shell=True)
            out, err = proc.communicate()
            for window in out.decode('utf-8').split('\n'):
                if 'Open3D' in window:
                    hwnd = int(window.split(' ')[0], 16)
                    print("Find hwnd is:",hwnd)
                    return hwnd   

    def shutdown(self):
        print("Open3DWidget.shutdown fired")
        if hasattr(self, "timer") and self.timer.isActive():
            self.timer.stop()
        try:
            self.o3d_window.close()
        except Exception as e:
            print("o3d_window.close failed:", e)

