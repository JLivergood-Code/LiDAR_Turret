# Resource object code (Python 3)
# Created by: object code
# Created by: The Resource Compiler for Qt version 6.10.1
# WARNING! All changes made in this file will be lost!

from PySide6 import QtCore

qt_resource_data = b"\
\x00\x00\x00\xa6\
i\
mport QtQuick 6.\
5\x0d\x0aimport My.Poi\
ntCloud 1.0\x0d\x0a\x0d\x0aR\
ectangle {\x0d\x0a    \
width: 800; heig\
ht: 600\x0d\x0a    Poi\
ntCloudItem {\x0d\x0a \
       id: pc\x0d\x0a \
       anchors.f\
ill: parent\x0d\x0a   \
 }\x0d\x0a}\
"

qt_resource_name = b"\
\x00\x08\
\x0c\xa7[|\
\x00t\
\x00e\x00s\x00t\x00.\x00q\x00m\x00l\
"

qt_resource_struct = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x00\x00\x00\
\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
\x00\x00\x01\x9c\x10P\xb0~\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x03, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
