#include "PointCloudItem.h"
#include "PointCloudRenderer.h"
#include <QMutexLocker>

PointCloudItem::PointCloudItem(QQuickItem *parent)
    : QQuickFramebufferObject(parent)
{
    setFlag(ItemHasContents, true);
    // ensure QML can find this object by name if needed
}

QQuickFramebufferObject::Renderer *PointCloudItem::createRenderer() const
{
    return new PointCloudRenderer(const_cast<PointCloudItem*>(this));
}

void PointCloudItem::setPointCloud(const QByteArray &data)
{
    QMutexLocker locker(&m_mutex);
    m_pointData = data;
    // schedule a sync with the render thread
    update();
}

void PointCloudItem::clear()
{
    QMutexLocker locker(&m_mutex);
    m_pointData.clear();
    update();
}

QByteArray PointCloudItem::takePointData()
{
    QMutexLocker locker(&m_mutex);
    return m_pointData; // returns a copy
}