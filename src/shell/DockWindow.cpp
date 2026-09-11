#include "DockWindow.h"
#include <QMouseEvent>
#include <QProcess>
#include <QDebug>

namespace UselessOS {

DockWindow::DockWindow(QScreen *screen, WindowTracker *tracker, QtWayland::zwlr_layer_shell_v1 *shell)
    : LayerSurfaceWindow(screen, "useless_dock")
    , m_tracker(tracker)
{
    // Configure default persistent launchers
    m_launchers.append({"Terminal", ">_", QColor(0x0E, 0x0E, 0x0D), QColor(0x00, 0xFF, 0x66), "x-terminal-emulator", {}});
    m_launchers.append({"Cognitive AI", "AI", QColor(0xEA, 0x34, 0xDF), Qt::white, "/opt/uselessos/uselessos-app", {"--mode", "copilot"}});
    m_launchers.append({"Editor", "TXT", QColor(0xFF, 0xE6, 0x00), QColor(0x0E, 0x0E, 0x0D), "mousepad", {}});
    m_launchers.append({"Files", "DIR", QColor(0x00, 0xC2, 0xCB), QColor(0x0E, 0x0E, 0x0D), "thunar", {}});
    m_launchers.append({"Settings", "⚙", QColor(0x24, 0x46, 0x38), Qt::white, "/opt/uselessos/uselessos-app", {"--mode", "settings"}});

    if (m_tracker) {
        connect(m_tracker, &QAbstractListModel::dataChanged, this, [this]() {
            requestRepaint();
        });
        connect(m_tracker, &QAbstractListModel::rowsInserted, this, [this]() {
            requestRepaint();
        });
        connect(m_tracker, &QAbstractListModel::rowsRemoved, this, [this]() {
            requestRepaint();
        });
        connect(m_tracker, &WindowTracker::activeWindowChanged, this, [this]() {
            requestRepaint();
        });
    }

    int initialWidth = 620;
    int initialHeight = 80;
    resize(initialWidth, initialHeight);

    setupLayerSurface(
        shell,
        QtWayland::zwlr_layer_shell_v1::layer_top,
        initialWidth,
        initialHeight,
        QtWayland::zwlr_layer_surface_v1::anchor_bottom,
        80, // Exclusive zone 80px
        0
    );
}

void DockWindow::updateDockLayout()
{
    m_runningTiles.clear();

    if (m_tracker) {
        const auto &winList = m_tracker->windows();
        for (const auto &win : winList) {
            RunningTile tile;
            tile.uuid = win.uuid;
            tile.title = win.title.isEmpty() ? win.appId : win.title;
            tile.appId = win.appId;
            tile.isActive = win.isActive;
            tile.isMinimized = win.isMinimized;
            m_runningTiles.append(tile);
        }
    }

    // Dynamic width calculation
    int tileW = 52;
    int tileMargin = 10;
    int totalLaunchersW = m_launchers.size() * (tileW + tileMargin);
    int separatorW = 18;
    int totalRunningW = m_runningTiles.size() * (tileW + tileMargin);

    int totalContentW = totalLaunchersW + (m_runningTiles.isEmpty() ? 0 : separatorW + totalRunningW) + 24;
    int dockW = std::clamp(totalContentW, 400, 1200);

    if (dockW != width()) {
        resize(dockW, height());
        set_size(dockW, 80);
    }
}

void DockWindow::paint(QPainter &painter)
{
    updateDockLayout();

    painter.setRenderHint(QPainter::Antialiasing, false);
    painter.setRenderHint(QPainter::TextAntialiasing, true);

    QRect totalRect(0, 0, width(), height());
    // Clear background to transparent raster
    painter.fillRect(totalRect, Qt::transparent);

    // Floating Neobrutalist Pill Container
    int dockMarginX = 8;
    int dockY = 8;
    int dockH = 64;
    QRect containerRect(dockMarginX, dockY, width() - (dockMarginX * 2), dockH);

    // Hard 5px Black Offset Shadow
    painter.fillRect(containerRect.translated(5, 5), QColor(0x0e, 0x0e, 0x0d));

    // Dock Pill Body: Warm Paper White (#F5F4F0) with 3px solid black border
    painter.fillRect(containerRect, QColor(0xF5, 0xF4, 0xF0));
    painter.setPen(QPen(QColor(0x0e, 0x0e, 0x0d), 3));
    painter.drawRect(containerRect);

    int startX = containerRect.x() + 16;
    int tileW = 50;
    int tileH = 46;
    int tileY = containerRect.y() + (dockH - tileH) / 2;

    // 1. Draw Persistent Launchers
    for (int i = 0; i < m_launchers.size(); ++i) {
        auto &launcher = m_launchers[i];
        bool isHovered = (i == m_hoveredLauncherIdx);

        int curX = startX + i * (tileW + 10);
        int curY = tileY - (isHovered ? 4 : 0);

        launcher.rect = QRect(curX, curY, tileW, tileH);

        // Tile Offset Shadow
        painter.fillRect(launcher.rect.translated(3, 3), QColor(0x0e, 0x0e, 0x0d));

        // Tile Body
        painter.fillRect(launcher.rect, launcher.bgColor);
        painter.setPen(QPen(QColor(0x0e, 0x0e, 0x0d), 2));
        painter.drawRect(launcher.rect);

        // Tile Text / Icon
        painter.setPen(launcher.fgColor);
        painter.setFont(QFont("sans-serif", 10, QFont::Black));
        painter.drawText(launcher.rect, Qt::AlignCenter, launcher.iconText);
    }

    startX += m_launchers.size() * (tileW + 10);

    // 2. Draw Separator (if running applications exist)
    if (!m_runningTiles.isEmpty()) {
        int sepX = startX + 6;
        painter.setPen(QPen(QColor(0x0e, 0x0e, 0x0d), 2, Qt::DashLine));
        painter.drawLine(sepX, containerRect.y() + 8, sepX, containerRect.bottom() - 8);
        startX += 18;
    }

    // 3. Draw Running Applications (From WindowTracker)
    for (int i = 0; i < m_runningTiles.size(); ++i) {
        auto &tile = m_runningTiles[i];
        bool isHovered = (i == m_hoveredRunningIdx);

        int curX = startX + i * (tileW + 10);
        int curY = tileY - (isHovered ? 4 : 0);

        tile.rect = QRect(curX, curY, tileW, tileH);

        // Tile Offset Shadow
        painter.fillRect(tile.rect.translated(3, 3), QColor(0x0e, 0x0e, 0x0d));

        // Tile Body
        QColor tileBg = tile.isActive ? QColor(0x00, 0xC2, 0xCB) : QColor(0xFF, 0xFF, 0xFF);
        if (tile.isMinimized) {
            tileBg = QColor(0xDD, 0xDD, 0xDD);
        }
        painter.fillRect(tile.rect, tileBg);
        painter.setPen(QPen(QColor(0x0e, 0x0e, 0x0d), 2));
        painter.drawRect(tile.rect);

        // App Initial / Icon
        QString initial = tile.title.left(3).toUpper();
        if (initial.isEmpty()) initial = "APP";

        painter.setPen(QColor(0x0e, 0x0e, 0x0d));
        painter.setFont(QFont("sans-serif", 9, QFont::Black));
        painter.drawText(tile.rect.adjusted(2, 2, -2, -10), Qt::AlignCenter, initial);

        // Active State Indicator Dot
        if (tile.isActive) {
            painter.fillRect(curX + (tileW / 2) - 4, tile.rect.bottom() - 6, 8, 4, QColor(0x0e, 0x0e, 0x0d));
        } else if (tile.isMinimized) {
            painter.fillRect(curX + (tileW / 2) - 4, tile.rect.bottom() - 6, 8, 2, QColor(0x88, 0x88, 0x88));
        }
    }
}

void DockWindow::mousePressEvent(QMouseEvent *ev)
{
    QPoint pos = ev->pos();

    // Check persistent launchers
    for (const auto &launcher : m_launchers) {
        if (launcher.rect.contains(pos)) {
            qInfo() << "[Dock] Launching persistent app:" << launcher.name << launcher.command;
            QProcess::startDetached(launcher.command, launcher.args);
            return;
        }
    }

    // Check running application tiles
    for (const auto &tile : m_runningTiles) {
        if (tile.rect.contains(pos)) {
            qInfo() << "[Dock] Toggling window activation/minimize:" << tile.title << tile.uuid;
            if (m_tracker) {
                m_tracker->toggleMinimize(tile.uuid);
            }
            return;
        }
    }
}

void DockWindow::mouseMoveEvent(QMouseEvent *ev)
{
    QPoint pos = ev->pos();
    int prevL = m_hoveredLauncherIdx;
    int prevR = m_hoveredRunningIdx;

    m_hoveredLauncherIdx = -1;
    for (int i = 0; i < m_launchers.size(); ++i) {
        if (m_launchers[i].rect.contains(pos)) {
            m_hoveredLauncherIdx = i;
            break;
        }
    }

    m_hoveredRunningIdx = -1;
    for (int i = 0; i < m_runningTiles.size(); ++i) {
        if (m_runningTiles[i].rect.contains(pos)) {
            m_hoveredRunningIdx = i;
            break;
        }
    }

    if (prevL != m_hoveredLauncherIdx || prevR != m_hoveredRunningIdx) {
        requestRepaint();
    }
}

bool DockWindow::event(QEvent *ev)
{
    if (ev->type() == QEvent::Leave) {
        m_hoveredLauncherIdx = -1;
        m_hoveredRunningIdx = -1;
        requestRepaint();
    }
    return LayerSurfaceWindow::event(ev);
}

} // namespace UselessOS
