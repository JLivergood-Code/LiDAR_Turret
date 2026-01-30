#include "PointCloudRenderer.h"
#include "PointCloudItem.h"
#include <QOpenGLFramebufferObject>
#include <QMutexLocker>
#include <QDebug>

static const char *vertexShaderSrc = R"(
#version 330 core
layout(location = 0) in vec3 in_pos;
layout(location = 1) in vec3 in_col;
uniform mat4 u_proj;
uniform mat4 u_view;
out vec3 v_color;
void main() {
    gl_Position = u_proj * u_view * vec4(in_pos, 1.0);
    v_color = in_col;
    gl_PointSize = 3.0;
}
)";

static const char *fragmentShaderSrc = R"(
#version 330 core
in vec3 v_color;
out vec4 fragColor;
void main() {
    // simple circular point sprite
    vec2 coord = 2.0 * gl_PointCoord - 1.0;
    if (dot(coord, coord) > 1.0) discard;
    fragColor = vec4(v_color, 1.0);
}
)";

PointCloudRenderer::PointCloudRenderer(PointCloudItem *item)
    : m_item(item), m_vbo(QOpenGLBuffer::VertexBuffer)
{
    initializeOpenGLFunctions();
    m_vbo.create();
}

PointCloudRenderer::~PointCloudRenderer()
{
    delete m_program;
    if (m_vbo.isCreated()) m_vbo.destroy();
}

void PointCloudRenderer::initShaders()
{
    if (m_program) return;
    m_program = new QOpenGLShaderProgram();
    m_program->addShaderFromSourceCode(QOpenGLShader::Vertex, vertexShaderSrc);
    m_program->addShaderFromSourceCode(QOpenGLShader::Fragment, fragmentShaderSrc);
    if (!m_program->link()) {
        qWarning() << "Shader link failed:" << m_program->log();
    }
}

QOpenGLFramebufferObject *PointCloudRenderer::createFramebufferObject(const QSize &size)
{
    QOpenGLFramebufferObjectFormat fmt;
    fmt.setAttachment(QOpenGLFramebufferObject::CombinedDepthStencil);
    return new QOpenGLFramebufferObject(size, fmt);
}

void PointCloudRenderer::synchronize(QQuickFramebufferObject *item)
{
    Q_UNUSED(item);
    // Obtain a copy of the point data from the QML item (thread-safe)
    if (!m_item) return;
    m_stagedData = m_item->takePointData();
    // We do not clear the item data here; Python/QML can call clear() explicitly.
}

void PointCloudRenderer::uploadToGPU()
{
    if (m_stagedData.isEmpty()) {
        m_vertexCount = 0;
        return;
    }

    const int floatsPerVertex = 6;
    const int floatSize = sizeof(float);
    m_vertexCount = m_stagedData.size() / (floatsPerVertex * floatSize);

    m_vbo.bind();
    // allocate and upload
    m_vbo.allocate(m_stagedData.constData(), m_stagedData.size());

    // set attribute pointers
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, floatsPerVertex * floatSize, reinterpret_cast<void*>(0));
    glEnableVertexAttribArray(1);
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, floatsPerVertex * floatSize, reinterpret_cast<void*>(3 * floatSize));
    m_vbo.release();

    m_vboInitialized = true;
}

void PointCloudRenderer::render()
{
    glEnable(GL_DEPTH_TEST);
    glClearColor(0.12f, 0.12f, 0.12f, 1.0f);
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);

    initShaders();

    // If new data staged, upload it
    if (!m_stagedData.isEmpty() || !m_vboInitialized) {
        uploadToGPU();
        m_stagedData.clear();
    }

    if (m_vertexCount == 0) return;

    m_program->bind();

    // Simple camera matrices; replace with QML-driven camera if desired
    QMatrix4x4 proj;
    float aspect = float(viewportSize().width()) / float(viewportSize().height());
    proj.perspective(45.0f, aspect, 0.01f, 1000.0f);

    QMatrix4x4 view;
    view.translate(0.0f, 0.0f, -3.0f);

    m_program->setUniformValue("u_proj", proj);
    m_program->setUniformValue("u_view", view);

    m_vbo.bind();
    glEnableVertexAttribArray(0);
    glEnableVertexAttribArray(1);
    glDrawArrays(GL_POINTS, 0, m_vertexCount);
    m_vbo.release();

    m_program->release();

    // Keep rendering continuously for interactive camera; remove update() for on-demand rendering
    update();
}