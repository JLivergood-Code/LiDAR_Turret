# pyside_example.py
# Python example using PySide6 to load QML and push a NumPy point cloud to the C++ item.
import sys
import numpy as np
from PySide6.QtCore import QByteArray, QUrl, QObject
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)

    engine = QQmlApplicationEngine()
    engine.load(QUrl("qrc:/qml/main.qml"))
    if not engine.rootObjects():
        print("Failed to load QML")
        sys.exit(-1)

    root = engine.rootObjects()[0]
    pc_item = root.findChild(QObject, "pc")
    if pc_item is None:
        print("Could not find PointCloudItem in QML")
        sys.exit(-1)

    # Create a random point cloud: N x 6 floats (x,y,z,r,g,b)
    N = 200000  # adjust to test performance
    pts = np.random.uniform(-1.0, 1.0, size=(N, 3)).astype(np.float32)
    cols = np.random.uniform(0.0, 1.0, size=(N, 3)).astype(np.float32)
    interleaved = np.empty((N, 6), dtype=np.float32)
    interleaved[:, 0:3] = pts
    interleaved[:, 3:6] = cols

    # Convert to QByteArray
    data_bytes = QByteArray(interleaved.tobytes())

    # Call the C++ method exposed to QML
    # setPointCloud is a Q_INVOKABLE on the C++ item
    pc_item.setProperty("visible", True)
    pc_item.setPointCloud(data_bytes)

    sys.exit(app.exec())