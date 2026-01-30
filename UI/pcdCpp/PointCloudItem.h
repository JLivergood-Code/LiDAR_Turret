#pragma once

#include <QQuickFramebufferObject>
#include <QByteArray>
#include <QMutex>

class PointCloudItem : public QQuickFramebufferObject
{
    Q_OBJECT
public:
    explicit PointCloudItem(QQuickItem *parent = nullptr);
    Renderer *createRenderer() const override;

    Q_INVOKABLE void setPointCloud(const QByteArray &data); // interleaved floats: x,y,z,r,g,b
    Q_INVOKABLE void clear();

    // Called by renderer on render thread to obtain the latest data copy
    QByteArray takePointData();

private:
    QByteArray m_pointData;
    mutable QMutex m_mutex;
};