#pragma once

#include "LayerSurfaceWindow.h"
#include <QTimer>
#include <QVector>

namespace UselessOS {

struct RetroMascot {
    float x = 0;
    float y = 0;
    float vx = 1.0f;
    float vy = 1.0f;
    float rotation = 0;
    float vrot = 0.5f;
    int size = 64;
    QColor color;
    QString label;
    int shapeType = 0; // 0: box, 1: circle, 2: speech bubble
};

class BackgroundCanvasWindow : public LayerSurfaceWindow {
    Q_OBJECT
public:
    BackgroundCanvasWindow(QScreen *screen, QtWayland::zwlr_layer_shell_v1 *shell);
    ~BackgroundCanvasWindow() override = default;

protected:
    void paint(QPainter &painter) override;
    void onConfigured(uint32_t width, uint32_t height) override;

private:
    QTimer *m_animTimer = nullptr;
    QVector<RetroMascot> m_mascots;
    void initMascots();
};

} // namespace UselessOS
