#include "BackgroundCanvasWindow.h"
#include <cmath>

namespace UselessOS {

BackgroundCanvasWindow::BackgroundCanvasWindow(QScreen *screen, QtWayland::zwlr_layer_shell_v1 *shell)
    : LayerSurfaceWindow(screen, "useless_canvas")
{
    initMascots();

    m_animTimer = new QTimer(this);
    connect(m_animTimer, &QTimer::timeout, this, [this]() {
        // Update mascot physics
        for (auto &m : m_mascots) {
            m.x += m.vx;
            m.y += m.vy;
            m.rotation += m.vrot;

            if (m.x < 20 || m.x > width() - m.size - 20) m.vx = -m.vx;
            if (m.y < 50 || m.y > height() - m.size - 90) m.vy = -m.vy;
        }
        requestRepaint();
    });
    m_animTimer->start(33); // ~30 fps smooth animation with negligible CPU

    QSize scrSize = screen ? screen->geometry().size() : QSize(1280, 800);
    resize(scrSize);

    setupLayerSurface(
        shell,
        QtWayland::zwlr_layer_shell_v1::layer_background,
        0, 0, // Fill screen
        QtWayland::zwlr_layer_surface_v1::anchor_top |
        QtWayland::zwlr_layer_surface_v1::anchor_bottom |
        QtWayland::zwlr_layer_surface_v1::anchor_left |
        QtWayland::zwlr_layer_surface_v1::anchor_right,
        0, // Exclusive zone 0 (background)
        0
    );
}

void BackgroundCanvasWindow::initMascots()
{
    m_mascots.clear();
    // 1. Useless Square
    m_mascots.append({180.0f, 220.0f, 0.8f, 0.5f, 5.0f, 0.3f, 72, QColor(0xFF, 0xE6, 0x00), "OVERTHINK", 0});
    // 2. Cyan Circle
    m_mascots.append({500.0f, 340.0f, -0.6f, 0.7f, 0.0f, 0.0f, 68, QColor(0x00, 0xC2, 0xCB), "404", 1});
    // 3. Pink Speech Bubble
    m_mascots.append({780.0f, 180.0f, 0.5f, -0.6f, -3.0f, -0.2f, 140, QColor(0xEA, 0x34, 0xDF), "Why do today?", 2});
    // 4. Accent Red Widget
    m_mascots.append({340.0f, 500.0f, -0.7f, -0.5f, 12.0f, 0.4f, 64, QColor(0xE8, 0x28, 0x03), "HALT", 0});
}

void BackgroundCanvasWindow::onConfigured(uint32_t width, uint32_t height)
{
    Q_UNUSED(width);
    Q_UNUSED(height);
}

void BackgroundCanvasWindow::paint(QPainter &painter)
{
    painter.setRenderHint(QPainter::Antialiasing, true);
    painter.setRenderHint(QPainter::TextAntialiasing, true);

    QRect rect(0, 0, width(), height());

    // 1. Cream Paper Base Background
    painter.fillRect(rect, QColor(0xF5, 0xF4, 0xF0));

    // 2. Subtle Neobrutalist Dot Grid
    painter.setPen(QPen(QColor(0xD0, 0xCE, 0xC4), 2));
    int gridStep = 40;
    for (int x = 20; x < width(); x += gridStep) {
        for (int y = 20; y < height(); y += gridStep) {
            painter.drawPoint(x, y);
        }
    }

    // 3. Floating Animated Mascots
    for (const auto &m : m_mascots) {
        painter.save();
        painter.translate(m.x + m.size / 2.0f, m.y + m.size / 2.0f);
        painter.rotate(m.rotation);

        QRect r(-m.size / 2, -m.size / 2, m.size, m.size);

        if (m.shapeType == 0) { // Square
            // Offset shadow
            painter.fillRect(r.translated(4, 4), QColor(0x0e, 0x0e, 0x0d));
            // Body
            painter.fillRect(r, m.color);
            painter.setPen(QPen(QColor(0x0e, 0x0e, 0x0d), 3));
            painter.drawRect(r);
            // Face / Label
            painter.setPen(QColor(0x0e, 0x0e, 0x0d));
            painter.setFont(QFont("sans-serif", 8, QFont::Black));
            painter.drawText(r, Qt::AlignCenter, m.label);
        } else if (m.shapeType == 1) { // Circle
            // Offset shadow
            painter.setBrush(QColor(0x0e, 0x0e, 0x0d));
            painter.setPen(Qt::NoPen);
            painter.drawEllipse(r.translated(4, 4));
            // Body
            painter.setBrush(m.color);
            painter.setPen(QPen(QColor(0x0e, 0x0e, 0x0d), 3));
            painter.drawEllipse(r);
            // Face
            painter.setPen(QColor(0x0e, 0x0e, 0x0d));
            painter.setFont(QFont("sans-serif", 9, QFont::Black));
            painter.drawText(r, Qt::AlignCenter, m.label);
        } else if (m.shapeType == 2) { // Speech Bubble
            QRect bubbleRect(-m.size / 2, -30, m.size, 50);
            painter.fillRect(bubbleRect.translated(4, 4), QColor(0x0e, 0x0e, 0x0d));
            painter.fillRect(bubbleRect, m.color);
            painter.setPen(QPen(QColor(0x0e, 0x0e, 0x0d), 3));
            painter.drawRect(bubbleRect);
            painter.setPen(Qt::white);
            painter.setFont(QFont("sans-serif", 9, QFont::Bold));
            painter.drawText(bubbleRect, Qt::AlignCenter, m.label);
        }

        painter.restore();
    }
}

} // namespace UselessOS
