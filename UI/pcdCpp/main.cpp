#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QtQml>
#include "PointCloudItem.h"

int main(int argc, char **argv)
{
    QGuiApplication app(argc, argv);

    qmlRegisterType<PointCloudItem>("My.PointCloud", 1, 0, "PointCloudItem");

    QQmlApplicationEngine engine;
    engine.addImportPath(QStringLiteral("qrc:/"));
    engine.load(QUrl(QStringLiteral("qrc:/qml/main.qml")));
    if (engine.rootObjects().isEmpty()) return -1;
    return app.exec();
}