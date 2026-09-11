#include "TopBarWindow.h"
#include <QMouseEvent>
#include <QProcess>
#include <QDebug>

namespace UselessOS {

TopBarWindow::TopBarWindow(QScreen *screen, WindowTracker *tracker, QtWayland::zwlr_layer_shell_v1 *shell)
    : LayerSurfaceWindow(screen, "useless_topbar")
    , m_tracker(tracker)
{
    updateTimeStrings();

    m_clockTimer = new QTimer(this);
    connect(m_clockTimer, &QTimer::timeout, this, [this]() {
        updateTimeStrings();
        requestRepaint();
    });
    m_clockTimer->start(1000);

    if (m_tracker) {
        connect(m_tracker, &WindowTracker::activeWindowChanged, this, [this](const QString &, const QString &) {
            requestRepaint();
        });
    }

    int screenWidth = screen ? screen->geometry().width() : 1280;
    resize(screenWidth, 42);

    setupLayerSurface(
        shell,
        QtWayland::zwlr_layer_shell_v1::layer_top,
        0, // Auto-expand width
        42,
        QtWayland::zwlr_layer_surface_v1::anchor_top |
        QtWayland::zwlr_layer_surface_v1::anchor_left |
        QtWayland::zwlr_layer_surface_v1::anchor_right,
        42, // Exclusive zone 42px
        0
    );
}

void TopBarWindow::updateTimeStrings()
{
    auto now = QDateTime::currentDateTime();
    m_currentTimeString = now.toString("HH:mm:ss");
    m_currentDateString = now.toString("ddd MMM d");
}

void TopBarWindow::paint(QPainter &painter)
{
    painter.setRenderHint(QPainter::Antialiasing, false);
    painter.setRenderHint(QPainter::TextAntialiasing, true);

    QRect barRect(0, 0, width(), height());

    // 1. Neobrutalist Bright Yellow Base Fill
    painter.fillRect(barRect, QColor(0xFF, 0xE6, 0x00));

    // 2. Thick Black Bottom Border (3px)
    painter.setPen(QPen(QColor(0x0e, 0x0e, 0x0d), 3));
    painter.drawLine(0, height() - 2, width(), height() - 2);

    int curX = 12;
    int curY = 6;
    int btnH = 30;

    // 3. Start Button / Brand Pill
    int startBtnW = 120;
    m_startButtonRect = QRect(curX, curY, startBtnW, btnH);

    // Hard offset shadow (2px)
    painter.fillRect(m_startButtonRect.translated(2, 2), QColor(0x0e, 0x0e, 0x0d));
    // Pill body
    QColor startBg = m_startButtonHover ? QColor(0xEA, 0x34, 0xDF) : QColor(0x0E, 0x0E, 0x0D);
    QColor startFg = m_startButtonHover ? QColor(0x0E, 0x0E, 0x0D) : Qt::white;
    painter.fillRect(m_startButtonRect, startBg);
    painter.setPen(QPen(QColor(0x0e, 0x0e, 0x0d), 2));
    painter.drawRect(m_startButtonRect);

    painter.setFont(QFont("sans-serif", 10, QFont::Black));
    painter.setPen(startFg);
    painter.drawText(m_startButtonRect, Qt::AlignCenter, "USELESS OS");

    curX += startBtnW + 16;

    // 4. Active Window Title Badge
    QString activeTitle = m_tracker ? m_tracker->activeWindowTitle() : QString();
    if (activeTitle.isEmpty()) {
        activeTitle = "Desktop (Idle)";
    }
    QFont titleFont("sans-serif", 9, QFont::Bold);
    QFontMetrics fm(titleFont);
    QString elidedTitle = fm.elidedText(activeTitle, Qt::ElideRight, 300);
    int badgeW = std::clamp(fm.horizontalAdvance(elidedTitle) + 24, 120, 320);

    m_activeWindowRect = QRect(curX, curY, badgeW, btnH);
    // Offset shadow
    painter.fillRect(m_activeWindowRect.translated(2, 2), QColor(0x0e, 0x0e, 0x0d));
    // Badge body
    painter.fillRect(m_activeWindowRect, QColor(0x00, 0xC2, 0xCB)); // Neon Cyan
    painter.setPen(QPen(QColor(0x0e, 0x0e, 0x0d), 2));
    painter.drawRect(m_activeWindowRect);

    painter.setFont(titleFont);
    painter.setPen(QColor(0x0e, 0x0e, 0x0d));
    painter.drawText(m_activeWindowRect, Qt::AlignCenter, elidedTitle);

    // 5. Right-Hand Side Elements (Clock, Quick Actions)
    int rightX = width() - 14;

    // Power / Session Button
    rightX -= 34;
    m_powerBtnRect = QRect(rightX, curY, 34, btnH);
    painter.fillRect(m_powerBtnRect.translated(2, 2), QColor(0x0e, 0x0e, 0x0d));
    painter.fillRect(m_powerBtnRect, m_powerBtnHover ? QColor(0xFF, 0x22, 0x22) : QColor(0xFF, 0x5F, 0x56));
    painter.setPen(QPen(QColor(0x0e, 0x0e, 0x0d), 2));
    painter.drawRect(m_powerBtnRect);
    painter.setPen(Qt::white);
    painter.setFont(QFont("sans-serif", 10, QFont::Bold));
    painter.drawText(m_powerBtnRect, Qt::AlignCenter, "✕");

    // Copilot / Cognitive Assistant Quick Button
    rightX -= 40;
    m_copilotBtnRect = QRect(rightX, curY, 34, btnH);
    painter.fillRect(m_copilotBtnRect.translated(2, 2), QColor(0x0e, 0x0e, 0x0d));
    painter.fillRect(m_copilotBtnRect, m_copilotBtnHover ? Qt::white : QColor(0xEA, 0x34, 0xDF));
    painter.setPen(QPen(QColor(0x0e, 0x0e, 0x0d), 2));
    painter.drawRect(m_copilotBtnRect);
    painter.setPen(m_copilotBtnHover ? QColor(0xEA, 0x34, 0xDF) : Qt::white);
    painter.setFont(QFont("sans-serif", 9, QFont::Black));
    painter.drawText(m_copilotBtnRect, Qt::AlignCenter, "AI");

    // Terminal Quick Button
    rightX -= 40;
    m_terminalBtnRect = QRect(rightX, curY, 34, btnH);
    painter.fillRect(m_terminalBtnRect.translated(2, 2), QColor(0x0e, 0x0e, 0x0d));
    painter.fillRect(m_terminalBtnRect, m_terminalBtnHover ? QColor(0x00, 0xC2, 0xCB) : QColor(0x0E, 0x0E, 0x0D));
    painter.setPen(QPen(QColor(0x0e, 0x0e, 0x0d), 2));
    painter.drawRect(m_terminalBtnRect);
    painter.setPen(m_terminalBtnHover ? QColor(0x0E, 0x0E, 0x0D) : QColor(0x00, 0xFF, 0x66));
    painter.setFont(QFont("monospace", 10, QFont::Bold));
    painter.drawText(m_terminalBtnRect, Qt::AlignCenter, ">_");

    // Digital Clock Badge
    QString clockStr = QString("%1  |  %2").arg(m_currentTimeString, m_currentDateString);
    QFont clockFont("monospace", 9, QFont::Bold);
    QFontMetrics cfm(clockFont);
    int clockW = cfm.horizontalAdvance(clockStr) + 20;

    rightX -= (clockW + 12);
    QRect clockRect(rightX, curY, clockW, btnH);
    painter.fillRect(clockRect.translated(2, 2), QColor(0x0e, 0x0e, 0x0d));
    painter.fillRect(clockRect, Qt::white);
    painter.setPen(QPen(QColor(0x0e, 0x0e, 0x0d), 2));
    painter.drawRect(clockRect);

    painter.setFont(clockFont);
    painter.setPen(QColor(0x0e, 0x0e, 0x0d));
    painter.drawText(clockRect, Qt::AlignCenter, clockStr);
}

void TopBarWindow::mousePressEvent(QMouseEvent *ev)
{
    QPoint pos = ev->pos();

    if (m_startButtonRect.contains(pos)) {
        qInfo() << "[TopBar] Start Menu clicked";
        QProcess::startDetached("/opt/uselessos/uselessos-app", QStringList() << "--mode" << "menu");
    } else if (m_terminalBtnRect.contains(pos)) {
        qInfo() << "[TopBar] Launching Terminal";
        QProcess::startDetached("x-terminal-emulator", QStringList());
    } else if (m_copilotBtnRect.contains(pos)) {
        qInfo() << "[TopBar] Launching Cognitive Copilot";
        QProcess::startDetached("/opt/uselessos/uselessos-app", QStringList() << "--mode" << "copilot");
    } else if (m_powerBtnRect.contains(pos)) {
        qInfo() << "[TopBar] Power action clicked";
        QProcess::startDetached("systemctl", QStringList() << "poweroff");
    }
}

void TopBarWindow::mouseMoveEvent(QMouseEvent *ev)
{
    QPoint pos = ev->pos();
    bool prevStart = m_startButtonHover;
    bool prevTerm = m_terminalBtnHover;
    bool prevCopilot = m_copilotBtnHover;
    bool prevPower = m_powerBtnHover;

    m_startButtonHover = m_startButtonRect.contains(pos);
    m_terminalBtnHover = m_terminalBtnRect.contains(pos);
    m_copilotBtnHover = m_copilotBtnRect.contains(pos);
    m_powerBtnHover = m_powerBtnRect.contains(pos);

    if (prevStart != m_startButtonHover || prevTerm != m_terminalBtnHover ||
        prevCopilot != m_copilotBtnHover || prevPower != m_powerBtnHover) {
        requestRepaint();
    }
}

bool TopBarWindow::event(QEvent *ev)
{
    if (ev->type() == QEvent::Leave) {
        m_startButtonHover = false;
        m_terminalBtnHover = false;
        m_copilotBtnHover = false;
        m_powerBtnHover = false;
        requestRepaint();
    }
    return LayerSurfaceWindow::event(ev);
}

} // namespace UselessOS
