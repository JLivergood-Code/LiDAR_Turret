import QtQuick
import QtQuick.Window

Window {
    id: win
    visible: true
    width: 2780
    height: 1700
    color: "#2a2929"

    Loader {
        anchors.fill: parent
        source: "ui_py.ui.qml"
    }
}