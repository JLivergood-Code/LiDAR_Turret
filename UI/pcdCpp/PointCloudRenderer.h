#pragma once

#include <QQuickFramebufferObject>
#include <QOpenGLBuffer>
#include <QOpenGLShaderProgram>
#include <QOpenGLFunctions>
#include <QMatrix4x4>

class PointCloudItem;

class PointCloudRenderer : public QQuickFramebufferObject::Renderer, protected QOpenGLFunctions
{
public:
    explicit PointCloudRenderer(PointCloudItem *item);
    ~PointCloudRenderer() override;

    void synchronize(QQuickFramebufferObject *item) override;
    void render() override;
    QOpenGLFramebufferObject *createFramebufferObject(const QSize &size) override;

private:
    PointCloudItem *m_item;
    QByteArray m_stagedData; // copy of data synchronized to render thread
    QOpenGLBuffer m_vbo;
    int m_vertexCount = 0;
    QOpenGLShaderProgram *m_program = nullptr;
    bool m_vboInitialized = false;

    void initShaders();
    void uploadToGPU();
};