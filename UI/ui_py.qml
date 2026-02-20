

/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick
import QtQuick.Controls
import QtQuick.Window
import QtQuick.Layouts
import QtQuick3D
import QtQuick.Controls.Material

ApplicationWindow {
    id: primWindow
    visible: true
    width: 1920
    height: 1080

    Material.theme: Material.Dark      // optional
    Material.accent: Material.Red    

    Rectangle {
        id: mainScreen
        anchors.fill: parent
        color: "#2a2929"
        property double sideW: Math.max(180, Math.min(520, Math.round(primWindow.width * 0.25)))
        property double ctlHeight: Math.max(180, Math.min(520, Math.round(primWindow.height * 0.33)))
        property double btnHeight: Math.max(10, Math.round(ctlHeight * 0.2))
        property real pcdWidth: Math.max(800, Math.round(primWindow.width * 0.67))
        property real pcdHeight: Math.round(primWindow.height * 0.80)
        property int ttlHeight: Math.round(primWindow.height * 0.02)
        property int txtHeight: Math.round(ttlHeight * 0.75)

        // anchors.fill: parent


        Rectangle {
            id: controlRect
            y: 365
            width: mainScreen.sideW
            height: mainScreen.ctlHeight
            visible: true
            radius: 35
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            anchors.rightMargin: 20
            anchors.bottomMargin: 10
            color: "#727272"
            clip: false

            RowLayout {
                id: rowLayout
                height: mainScreen.btnHeight
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.leftMargin: 25
                anchors.rightMargin: 25
                anchors.topMargin: 68
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
                color: "#323232"
                radius: 35
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.bottom: parent.top
                anchors.leftMargin: 5
                anchors.rightMargin: 5
                anchors.topMargin: 5
                anchors.bottomMargin: -40
                Text {
                    id: text4
                    color: "#b9b9b9"
                    text: qsTr("Controls")
                    font.pointSize: mainScreen.ttlHeight
                    font.bold: true
                    font.family: "Courier"
                    anchors.centerIn: parent
                }
            }

            RowLayout {
                id: rowLayout2
                y: 122
                height: mainScreen.btnHeight
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.bottom: parent.verticalCenter
                anchors.leftMargin: 25
                anchors.rightMargin: 25
                anchors.bottomMargin: -51
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
                anchors.bottomMargin: 10
                layer.format: ShaderEffectSource.Alpha
                highlighted: false
                font.family: "Segoe UI"
                flat: false
                checkable: false
                autoExclusive: false
                Layout.fillWidth: true

                onClicked: backend.tick()
            }
        }

        Rectangle {
            id: pcdRect
            color: "#727272"
            radius: 35
            width: mainScreen.pcdWidth
            anchors.left: parent.left
            anchors.right: controlRect.left
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.leftMargin: 20
            anchors.rightMargin: 20
            anchors.topMargin: 20
            anchors.bottomMargin: 20

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
                    font.pointSize: mainScreen.ttlHeight
                    font.bold: true
                    font.family: "Courier"
                    anchors.centerIn: parent
                }
            }

            WindowContainer {
                id: o3dContainer
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: pcdTitleRect1.bottom
                anchors.bottom: parent.bottom
                anchors.leftMargin: 15
                anchors.rightMargin: 15
                anchors.topMargin: 15
                anchors.bottomMargin: 15

                window: open3dWindow
                focus: true
            }
        }

        Rectangle {
            id: turretRect
            color: "#727272"
            radius: 35
            anchors.left: pcdRect.right
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.bottom: targetRect.top
            anchors.leftMargin: 20
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
                    font.pointSize: mainScreen.ttlHeight
                    font.bold: true
                    font.family: "Courier"
                    anchors.centerIn: parent
                }
            }

            BorderImage {
                id: turret
                source: "tank.png"
                width: 100
                height: 100
                border.left: 5
                border.top: 5
                border.right: 5
                border.bottom: 5
                anchors.verticalCenterOffset: 0
                anchors.horizontalCenterOffset: 0
                anchors.centerIn: parent
                rotation: backend.imgRotation
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
                    font.pointSize: mainScreen.txtHeight
                    fontSizeMode: Text.Fit
                    font.bold: true
                    font.family: "Courier"
                }

                Text {
                    // property string turretAngleText: qsTr("0°")

                    id: angleText2
                    color: "#b9b9b9"
                    text: backend.turretAngle
                    font.pointSize: mainScreen.txtHeight
                    font.bold: true
                    font.family: "Courier"
                }
            }
        }

        Rectangle {
            id: targetRect
            height: 274
            color: "#727272"
            radius: 35
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: pcdRect.right
            anchors.right: parent.right
            anchors.bottom: controlRect.top
            anchors.leftMargin: 20
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
                    font.pointSize: mainScreen.ttlHeight
                    font.bold: true
                    font.family: "Courier"
                    anchors.centerIn: parent
                }
            }

            GridLayout {
                id: gridControlLayout
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.leftMargin: 10
                anchors.rightMargin: 10
                anchors.topMargin: 62
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
                    Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                    font.pointSize: mainScreen.txtHeight
                    Layout.columnSpan: 1
                    Layout.rowSpan: 1
                    font.family: "Courier"
                    font.bold: true
                }

                Text {
                    // property string humanText: qsTr("No")

                    id: textCont6
                    color: "#b9b9b9"
                    text: backend.humanDetected
                    font.pointSize: mainScreen.txtHeight
                    font.family: "Courier"
                    font.bold: true
                    Layout.rowSpan: 1
                    Layout.columnSpan: 1
                }

                Text {
                    id: textCont7
                    color: "#b9b9b9"
                    text: qsTr("Angle:")
                    font.pointSize: mainScreen.txtHeight
                    Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                    font.family: "Courier"
                    font.bold: true
                    Layout.rowSpan: 1
                    Layout.columnSpan: 1
                }

                Text {
                    // property string targetAngleText: qsTr("0°")

                    id: textCont8
                    color: "#b9b9b9"
                    text: backend.humanAngle
                    font.pointSize: mainScreen.txtHeight
                    font.family: "Courier"
                    font.bold: true
                    Layout.rowSpan: 1
                    Layout.columnSpan: 1
                }

                Text {
                    id: textCont9
                    color: "#b9b9b9"
                    text: qsTr("Distance:")
                    font.pointSize: mainScreen.txtHeight
                    Layout.alignment: Qt.AlignRight | Qt.AlignVCenter
                    Layout.fillHeight: false
                    Layout.fillWidth: false
                    font.family: "Courier"
                    font.bold: true
                    Layout.rowSpan: 1
                    Layout.columnSpan: 1
                }

                Text {
                    // property string targetDistText: qsTr("0m")

                    id: textCont10
                    color: "#b9b9b9"
                    text: backend.targetDist
                    font.pointSize: mainScreen.txtHeight
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

}