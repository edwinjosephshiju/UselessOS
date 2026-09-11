#pragma once

#include "LayerSurfaceWindow.h"
#include "WindowTracker.h"
#include <QTimer>
#include <QDateTime>

namespace UselessOS {

class TopBarWindow : public LayerSurfaceWindow {
    Q_OBJECT
public:
    TopBarWindow(QScreen *screen, WindowTracker *tracker, QtWayland::zwlr_layer_shell_v1 *shell);
    ~TopBarWindow() override = default;

protected:
    void paint(QPainter &painter) override;
    void mousePressEvent(QMouseEvent *ev) override;
    void mouseMoveEvent(QMouseEvent *ev) override;
    bool event(QEvent *ev) override;

private:
    WindowTracker *m_tracker = nullptr;
    QTimer *m_clockTimer = nullptr;
    QString m_currentTimeString;
    QString m_currentDateString;

    QRect m_startButtonRect;
    QRect m_activeWindowRect;
    QRect m_terminalBtnRect;
    QRect m_copilotBtnRect;
    QRect m_powerBtnRect;

    bool m_startButtonHover = false;
    bool m_terminalBtnHover = false;
    bool m_copilotBtnHover = false;
    bool m_powerBtnHover = false;

    void updateTimeStrings();
};

} // namespace UselessOS
