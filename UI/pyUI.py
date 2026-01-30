
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Signal, Slot, Property, QByteArray, Qt
from PyQt5.QtGui import QImage, QPixmap
import numpy as np


class PointCloudBridge(QObject):
    pointsChanged = Signal()

    # init
    def __init__(self):
        super().__init__()
        self._points = QByteArray()

    @Property(QByteArray, notify=pointsChanged)
    def points(self):
        return self._points

    # updates points from list
    @Slot("QVariantList")
    def updateFromList(self, pts):
        # pts is a list of [x,y,z] triples
        flat = []
        for p in pts:
            flat.extend(p)
        arr = np.array(flat, dtype=np.float32)
        self._points = QByteArray(arr.tobytes())
        self.pointsChanged.emit()

    # Updates Points randomly
    @Slot()
    def updateRandom(self):
        pts = np.random.rand(1000, 3) * 100
        arr = pts.astype(np.float32).flatten()
        self._points = QByteArray(arr.tobytes())
        self.pointsChanged.emit()

def main():
    app = QGuiApplication([])

    engine = QQmlApplicationEngine()
    backend = PointCloudBridge()
    print(f"Loading UI/pyUI.py")
    engine.load("./UI/ui_py.ui.qml")
    app.processEvents()
    print(f"Loading UI/pyUI.py")


    if not engine.rootObjects():
        raise RuntimeError("Failed to load QML")

    root_object = engine.rootObjects()[0]
    
    engine.rootContext().setContextProperty("pointCloudBridge", backend)
    view3d = root_object.findChild(QObject, "view3D", Qt.FindChildrenRecursively)
    

    app.exec()

    print("finished")
    exit(0)

if __name__ == "__main__":
    main()