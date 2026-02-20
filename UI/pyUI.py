# from readline import backend
import sys
from PySide6.QtCore import QUrl, Property, QObject, Signal, Slot
from PySide6.QtGui import QWindow
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from Open3DWidget import Open3DWidget  # your file

# Stuff for backend 
# turretAngleText = "0°"
# humanText = "No human detected"
# humanAngleText = "0°"
# targetDistText = "0m"

class Backend(QObject):
    humanDetectedChanged = Signal()
    turretAngleChanged = Signal()
    humanAngleChanged = Signal()
    targetDistChanged = Signal()
    imgRotationChanged = Signal()


    def __init__(self):
        super().__init__()
        self._humanDetected = "No"
        self._turretAngle = "0°"
        self._humanAngle = "0°"
        self._targetDist = "0m"
        self._imgRotation = 0

    def getHumanDetected(self): return self._humanDetected
    def setHumanDetected(self, v):
        if self._humanDetected == v: return
        self._humanDetected = v
        self.humanDetectedChanged.emit()
    humanDetected = Property(str, getHumanDetected, setHumanDetected, notify=humanDetectedChanged)

    def getTurretAngle(self): return self._turretAngle
    def setTurretAngle(self, v):
        if self._turretAngle == v: return
        self._turretAngle = v
        self.turretAngleChanged.emit()
    turretAngle = Property(str, getTurretAngle, setTurretAngle, notify=turretAngleChanged)

    def getHumanAngle(self): return self._humanAngle
    def setHumanAngle(self, v):
        if self._humanAngle == v: return
        self._humanAngle = v
        self.humanAngleChanged.emit()
    humanAngle = Property(str, getHumanAngle, setHumanAngle, notify=humanAngleChanged)

    def getTargetDist(self): return self._targetDist
    def setTargetDist(self, v):
        if self._targetDist == v: return
        self._targetDist = v
        self.targetDistChanged.emit()
    targetDist = Property(str, getTargetDist, setTargetDist, notify=targetDistChanged)

    def getImgRotation(self): return self._imgRotation
    def setImgRotation(self, v):
        if self._imgRotation == v: return
        self._imgRotation = v
        self.imgRotationChanged.emit()
    imgRotation = Property(int, getImgRotation, setImgRotation, notify=imgRotationChanged)

    @Slot()
    def tick(self):
        self.setHumanDetected("Yes")
        self.setTurretAngle("45°")
        self.setHumanAngle("30°")
        self.setTargetDist("10m")
        self.setImgRotation(45)

def main():
    app = QApplication(sys.argv)

    # Create your QWidget-based Open3DWidget as a *top-level native window*
    o3d_widget = Open3DWidget(parent=None)
    o3d_widget.setAttribute(Qt.WA_NativeWindow, True)
    o3d_widget.resize(2780, 1700)
    o3d_widget.show()  # IMPORTANT: ensures winId/windowHandle exists
    o3d_widget.hide()
    
    # Convert QWidget -> QWindow for QML WindowContainer
    o3d_window = o3d_widget.windowHandle()
    if o3d_window is None:
        # fallback if needed
        o3d_window = QWindow.fromWinId(int(o3d_widget.winId()))

    print("open3dWindow:", o3d_window, "winId:", o3d_window.winId() if o3d_window else None)


    engine = QQmlApplicationEngine()
    backend = Backend()

    engine.rootContext().setContextProperty("backend", backend)
    engine.rootContext().setContextProperty("open3dWindow", o3d_window)

    # Clean shutdown
    app.aboutToQuit.connect(o3d_widget.shutdown)

    engine.load(QUrl.fromLocalFile("./LiDAR_Turret/UI/ui_py.qml"))
    if not engine.rootObjects():
        sys.exit(1)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
