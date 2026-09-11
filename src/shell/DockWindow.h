#pragma once

#include "LayerSurfaceWindow.h"
#include "WindowTracker.h"
#include <QVector>
#include <QRect>

namespace UselessOS {

struct DockLauncher {
    QString name;
    QString iconText;
    QColor bgColor;
    QColor fgColor;
    QString command;
    QStringList args;
    QRect rect;
};

struct RunningTile {
    QString uuid;
    QString title;
    QString appId;
    bool isActive;
    bool isMinimized;
    QRect rect;
};

class DockWindow : public LayerSurfaceWindow {
    Q_OBJECT
public:
    DockWindow(QScreen *screen, WindowTracker *tracker, QtWayland::zwlr_layer_shell_v1 *shell);
    ~DockWindow() override = default;

protected:
    void paint(QPainter &painter) override;
    void mousePressEvent(QMouseEvent *ev) override;
    void mouseMoveEvent(QMouseEvent *ev) override;
    bool event(QEvent *ev) override;

private:
    WindowTracker *m_tracker = nullptr;
    QVector<DockLauncher> m_launchers;
    QVector<RunningTile> m_runningTiles;

    int m_hoveredLauncherIdx = -1;
    int m_hoveredRunningIdx = -1;

    void updateDockLayout();
};

} // namespace UselessOS
