

/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick
import QtQuick.Controls
import Test
import QtQuick.Studio.Components
import QtQuick.Layouts
import QtQuick3D
import QtQuick3D.Xr
import QtQuick3D.AssetUtils
import QtQuick3D.Helpers
import QtQuick3D.Physics.Helpers
import QtQuick3D.Particles3D

Rectangle {
    id: rectangle
    width: 2780
    height: 1700
    color: "#2a2929"

    RectangleItem {
        id: controlRect
        x: 2314
        width: 446
        height: 372
        visible: true
        radius: 35
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        anchors.rightMargin: 20
        anchors.bottomMargin: 20
        fillColor: "#727272"
        clip: false
        strokeWidth: 3
        strokeColor: "#333834"
        adjustBorderRadius: true

        TextInput {
            id: textInput
            height: 30
            text: qsTr("Manual Control")
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: controlTitleRect3.bottom
            anchors.leftMargin: 8
            anchors.rightMargin: 8
            anchors.topMargin: 0
            font.pixelSize: 21
            horizontalAlignment: Text.AlignHCenter
        }

        RowLayout {
            id: rowLayout
            height: 52
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: button5.top
            anchors.leftMargin: 17
            anchors.rightMargin: 33
            anchors.bottomMargin: 20
            spacing: 40
            Button {
                id: button1
                opacity: 1
                text: qsTr("Automatic")
                highlighted: false
                flat: false
                autoExclusive: true
                checkable: true
                layer.format: ShaderEffectSource.Alpha
                font.family: "Segoe UI"
                Layout.fillWidth: true
            }

            Button {
                id: button2
                text: qsTr("Manual")
                autoExclusive: true
                checkable: true
                icon.cache: false
                highlighted: false
                flat: false
                Layout.fillWidth: true
            }
        }

        Rectangle {
            id: controlTitleRect3
            x: -1454
            y: -683
            height: 58
            color: "#323232"
            radius: 35
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.leftMargin: 5
            anchors.rightMargin: 5
            anchors.topMargin: 5
            Text {
                id: text4
                color: "#b9b9b9"
                text: qsTr("Controls")
                font.pixelSize: 30
                font.bold: true
                font.family: "Courier"
                anchors.centerIn: parent
            }
        }

        RowLayout {
            id: rowLayout2
            y: 99
            height: 52
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: rowLayout.top
            anchors.leftMargin: 25
            anchors.rightMargin: 25
            anchors.bottomMargin: 20
            spacing: 40
            Button {
                id: button3
                opacity: 1
                text: qsTr("On")
                layer.format: ShaderEffectSource.Alpha
                highlighted: false
                font.family: "Segoe UI"
                flat: false
                checkable: true
                autoExclusive: true
                Layout.fillWidth: true
            }

            Button {
                id: button4
                text: qsTr("Off")
                icon.cache: false
                highlighted: false
                flat: false
                checkable: true
                autoExclusive: true
                Layout.fillWidth: true
            }
        }

        Button {
            id: button5
            opacity: 1
            text: qsTr("Fire")
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.leftMargin: 20
            anchors.rightMargin: 20
            anchors.bottomMargin: 20
            layer.format: ShaderEffectSource.Alpha
            highlighted: false
            font.family: "Segoe UI"
            flat: false
            checkable: false
            autoExclusive: false
            Layout.fillWidth: true
        }
    }

    Rectangle {
        id: pcdRect
        color: "#727272"
        radius: 35
        anchors.left: parent.left
        anchors.right: controlRect.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.leftMargin: 20
        anchors.rightMargin: 20
        anchors.topMargin: 20
        anchors.bottomMargin: 20

        View3D {
            id: view3D
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: pcdTitleRect1.bottom
            anchors.bottom: parent.bottom
            anchors.leftMargin: 10
            anchors.rightMargin: 10
            anchors.topMargin: 10
            anchors.bottomMargin: 10
            camera: sceneCamera
            environment: sceneEnvironment
            SceneEnvironment {
                id: sceneEnvironment
                antialiasingQuality: SceneEnvironment.High
                antialiasingMode: SceneEnvironment.MSAA
            }

            Node {
                id: scene
                DirectionalLight {
                    id: directionalLight
                }

                PerspectiveCamera {
                    id: sceneCamera
                    z: 350
                }

                Model {
                    materials: PrincipledMaterial {}
                }
            }
        }

        Rectangle {
            id: pcdTitleRect1
            height: 58
            color: "#323232"
            radius: 35
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.leftMargin: 5
            anchors.rightMargin: 5
            anchors.topMargin: 5

            Text {
                id: text1
                color: "#b9b9b9"
                text: qsTr("Point Cloud")
                font.pixelSize: 30
                font.bold: true
                font.family: "Courier"
                anchors.centerIn: parent
            }
        }
    }

    Rectangle {
        id: turretRect
        width: 430
        color: "#727272"
        radius: 35
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: targetRect.top
        anchors.rightMargin: 20
        anchors.topMargin: 20
        anchors.bottomMargin: 20

        Rectangle {
            id: turretTitleRect2
            x: -1454
            y: -15
            height: 58
            color: "#323232"
            radius: 35
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.leftMargin: 5
            anchors.rightMargin: 5
            anchors.topMargin: 5

            Text {
                id: text2
                color: "#b9b9b9"
                text: qsTr("Turret Status")
                font.pixelSize: 30
                font.bold: true
                font.family: "Courier"
                anchors.centerIn: parent
            }
        }

        TriangleItem {
            id: triangle
            anchors.verticalCenterOffset: 0
            anchors.horizontalCenterOffset: 0
            anchors.centerIn: parent
            rotation: 20
        }

        RowLayout {
            id: rowLayout1
            x: -2305
            y: 601
            height: 52
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.leftMargin: 5
            anchors.rightMargin: 0
            anchors.bottomMargin: 20
            uniformCellSizes: false
            layoutDirection: Qt.LeftToRight
            spacing: 20


            Text {
                id: angleText1
                color: "#b9b9b9"
                text: qsTr("Turret Status")
                font.pixelSize: 30
                font.bold: true
                font.family: "Courier"
            }

            Text {
                id: angleText2
                color: "#b9b9b9"
                text: qsTr("0 Deg")
                font.pixelSize: 30
                font.bold: true
                font.family: "Courier"
            }

        }
    }

    Rectangle {
        id: targetRect
        width: 430
        height: 274
        color: "#727272"
        radius: 35
        anchors.verticalCenter: parent.verticalCenter
        anchors.right: parent.right
        anchors.bottom: controlRect.top
        anchors.rightMargin: 20
        anchors.bottomMargin: 20

        Rectangle {
            id: targetTitleRect2
            x: -1462
            y: -380
            height: 58
            color: "#323232"
            radius: 35
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.leftMargin: 5
            anchors.rightMargin: 5
            anchors.topMargin: 5

            Text {
                id: text3
                color: "#b9b9b9"
                text: qsTr("Target Status")
                font.pixelSize: 30
                font.bold: true
                font.family: "Courier"
                anchors.centerIn: parent
            }
        }

        GridLayout {
            id: gridControlLayout
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: targetTitleRect2.bottom
            anchors.bottom: parent.bottom
            anchors.leftMargin: 10
            anchors.rightMargin: 10
            anchors.topMargin: 10
            anchors.bottomMargin: 10
            columnSpacing: 10
            uniformCellHeights: false
            uniformCellWidths: true
            rows: 3
            columns: 2

            Text {
                id: textCont5
                color: "#b9b9b9"
                text: qsTr("Human Detected:")
                font.pixelSize: 30
                Layout.columnSpan: 1
                Layout.rowSpan: 1
                font.family: "Courier"
                font.bold: true
            }

            Text {
                id: textCont6
                color: "#b9b9b9"
                text: qsTr("Yes")
                font.pixelSize: 30
                font.family: "Courier"
                font.bold: true
                Layout.rowSpan: 1
                Layout.columnSpan: 1
            }

            Text {
                id: textCont7
                color: "#b9b9b9"
                text: qsTr("Angle:")
                font.pixelSize: 30
                Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                font.family: "Courier"
                font.bold: true
                Layout.rowSpan: 1
                Layout.columnSpan: 1
            }

            Text {
                id: textCont8
                color: "#b9b9b9"
                text: qsTr("0 Deg")
                font.pixelSize: 30
                font.family: "Courier"
                font.bold: true
                Layout.rowSpan: 1
                Layout.columnSpan: 1
            }

            Text {
                id: textCont9
                color: "#b9b9b9"
                text: qsTr("Distance:")
                font.pixelSize: 30
                Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                Layout.fillHeight: false
                Layout.fillWidth: false
                font.family: "Courier"
                font.bold: true
                Layout.rowSpan: 1
                Layout.columnSpan: 1
            }

            Text {
                id: textCont10
                color: "#b9b9b9"
                text: qsTr("10 m")
                font.pixelSize: 30
                font.family: "Courier"
                font.bold: true
                Layout.rowSpan: 1
                Layout.columnSpan: 1
            }
        }
    }

    Item {
        id: __materialLibrary__

        PrincipledMaterial {
            id: principledMaterial
            objectName: "New Material"
        }
    }
    states: [
        State {
            name: "clicked"
        }
    ]
}
