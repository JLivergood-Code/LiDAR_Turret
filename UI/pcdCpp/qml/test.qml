import QtQuick 6.5
import My.PointCloud 1.0

Rectangle {
    width: 800; height: 600
    PointCloudItem {
        id: pc
        anchors.fill: parent
    }
}