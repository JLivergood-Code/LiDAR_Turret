import open3d as o3d
import numpy as np
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
import sys

# 1. Setup Open3D Offscreen Renderer
render = o3d.visualization.rendering.OffscreenRenderer(640, 480)

# 2. Load and add Point Cloud
pcd = o3d.io.read_point_cloud("../LiDAR_Turret/data/street1/streed1-0.pcd")
render.scene.add_geometry("pcd", pcd, o3d.visualization.rendering.MaterialRecord())
render.scene.set_background([0, 0, 0, 1]) # Black background
render.setup_camera(60.0, pcd.get_center(), [0, 0, 1], [0, 1, 0])

# 3. Render to Image
image = render.render_to_image()
image_np = np.asarray(image)

# 4. Qt Setup
app = QApplication(sys.argv)
window = QWidget()
layout = QVBoxLayout()
label = QLabel()

# Convert numpy image to QImage
qimg = QImage(image_np.data, image_np.shape[1], image_np.shape[0], QImage.Format_RGB888)
label.setPixmap(QPixmap.fromImage(qimg))

layout.addWidget(label)
window.setLayout(layout)
window.show()
sys.exit(app.exec_())