#include "UselessWindow.h"
#include "CustomTitleBar.h"
#include "UselessInstructionsDialog.h"
#include "UselessTheme.h"

#include <QFrame>
#include <QVBoxLayout>
#include <QScrollArea>
#include <QPainterPath>
#include <QRegion>
#include <QResizeEvent>
#include <QMouseEvent>
#include <QGuiApplication>
#include <QScreen>
#include <QCursor>
#include <QWindow>

namespace UselessOS {

UselessWindow::UselessWindow(const QString& title,
                             const QString& subtitle,
                             const QString& iconName,
                             const QString& accentColor,
                             int width,
                             int height,
                             QWidget* parent)
    : QMainWindow(parent)
    , m_appTitle(title)
    , m_appSubtitle(subtitle)
    , m_appIcon(iconName)
    , m_appAccent(accentColor)
{
    setWindowTitle(QStringLiteral("%1 - UselessOS").arg(title));
    resize(width, height);

    const int minW = std::max(340, std::min(width, 400));
    const int minH = std::max(240, std::min(height, 300));
    setMinimumSize(minW, minH);

    // Frameless translucent window
    setWindowFlags(Qt::FramelessWindowHint);
    setAttribute(Qt::WA_TranslucentBackground);
    setMouseTracking(true);

    // Center on primary display
    QScreen* screen = QGuiApplication::primaryScreen();
    if (screen) {
        const QRect sgeo = screen->availableGeometry();
        move(sgeo.x() + std::max(20, (sgeo.width() - width) / 2),
             sgeo.y() + std::max(50, (sgeo.height() - height) / 2 - 20));
    }

    // Root Frame with 2px solid Neobrutalist border
    m_rootFrame = new QFrame(this);
    m_rootFrame->setObjectName(QStringLiteral("UselessRootFrame"));
    m_rootFrame->setMouseTracking(true);
    m_rootFrame->setStyleSheet(QStringLiteral(
        "#UselessRootFrame {"
        "    background-color: #ffffff;"
        "    border: 2px solid #0e0e0d;"
        "    border-radius: 16px;"
        "}"
    ));
    setCentralWidget(m_rootFrame);

    auto* rootLayout = new QVBoxLayout(m_rootFrame);
    rootLayout->setContentsMargins(0, 0, 0, 0);
    rootLayout->setSpacing(0);

    // macOS Title Bar
    m_titleBar = new CustomTitleBar(this, title, subtitle, iconName, accentColor);
    rootLayout->addWidget(m_titleBar);

    // Responsive Scroll Area
    m_scrollArea = new QScrollArea(m_rootFrame);
    m_scrollArea->setObjectName(QStringLiteral("UselessScrollArea"));
    m_scrollArea->setWidgetResizable(true);
    m_scrollArea->setFrameShape(QFrame::NoFrame);
    m_scrollArea->setStyleSheet(QStringLiteral(
        "#UselessScrollArea {"
        "    background-color: transparent;"
        "    border: none;"
        "}"
        "QScrollBar:vertical {"
        "    border: 1.5px solid #0e0e0d;"
        "    background: #f5f4f0;"
        "    width: 10px;"
        "    border-radius: 5px;"
        "    margin: 4px 6px 6px 0px;"
        "}"
        "QScrollBar::handle:vertical {"
        "    background: #0e0e0d;"
        "    border-radius: 3px;"
        "    min-height: 20px;"
        "}"
        "QScrollBar::handle:vertical:hover {"
        "    background: #ea34df;"
        "}"
        "QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {"
        "    height: 0px;"
        "}"
        "QScrollBar::horizontal {"
        "    height: 0px;"
        "}"
    ));

    // Content container
    m_contentWidget = new QWidget(m_scrollArea);
    m_contentWidget->setObjectName(QStringLiteral("UselessContentWidget"));
    m_contentWidget->setStyleSheet(QStringLiteral(
        "#UselessContentWidget {"
        "    background-color: #ffffff;"
        "    border: none;"
        "    border-bottom-left-radius: 14px;"
        "    border-bottom-right-radius: 14px;"
        "}"
    ));
    m_contentLayout = new QVBoxLayout(m_contentWidget);
    m_contentLayout->setContentsMargins(20, 16, 20, 20);
    m_contentLayout->setSpacing(14);

    m_scrollArea->setWidget(m_contentWidget);
    rootLayout->addWidget(m_scrollArea);

    m_rootFrame->installEventFilter(this);

    updateWindowMask();
}

void UselessWindow::resizeEvent(QResizeEvent* event) {
    QMainWindow::resizeEvent(event);
    updateWindowMask();
}

void UselessWindow::updateWindowMask() {
    QPainterPath path;
    path.addRoundedRect(0.0, 0.0, static_cast<qreal>(width()), static_cast<qreal>(height()), 16.0, 16.0);
    setMask(QRegion(path.toFillPolygon().toPolygon()));
}

void UselessWindow::showInstructionsDialog() {
    auto* dlg = new UselessInstructionsDialog(m_appTitle, m_appSubtitle, m_appIcon, m_appAccent, this);
    
    // Center dialog over parent window, clamped within screen bounds
    const QRect pGeo = geometry();
    int centerX = pGeo.x() + (pGeo.width() - dlg->width()) / 2;
    int centerY = pGeo.y() + (pGeo.height() - dlg->height()) / 2;
    QScreen* screen = QGuiApplication::primaryScreen();
    if (screen) {
        const QRect sGeo = screen->availableGeometry();
        centerX = std::max(sGeo.x() + 10, std::min(centerX, sGeo.right() - dlg->width() - 10));
        centerY = std::max(sGeo.y() + 44, std::min(centerY, sGeo.bottom() - dlg->height() - 10));
    }
    dlg->move(centerX, centerY);

    dlg->exec();
    dlg->deleteLater();
}

void UselessWindow::toggleMaximized() {
    if (m_isMaximized) {
        if (!m_normalGeo.isEmpty()) {
            setGeometry(m_normalGeo);
        } else {
            showNormal();
        }
        m_isMaximized = false;
    } else {
        m_normalGeo = geometry();
        QScreen* screen = QGuiApplication::primaryScreen();
        if (screen) {
            const QRect sGeo = screen->availableGeometry();
            const int topY = sGeo.y() + 46;
            setGeometry(sGeo.x() + 8, topY, sGeo.width() - 16, std::max(300, sGeo.height() - 46 - 94));
        }
        m_isMaximized = true;
    }
}

UselessWindow::Edges UselessWindow::getActiveEdges(const QPoint& localPos) const {
    if (m_isMaximized) {
        return Edges{};
    }

    const int m = ResizeMargin;
    const int w = width();
    const int h = height();

    Edges e;
    e.top = localPos.y() < m;
    e.bottom = localPos.y() >= h - m;
    e.left = localPos.x() < m;
    e.right = localPos.x() >= w - m;
    return e;
}

void UselessWindow::updateCursorShape(const Edges& edges) {
    if ((edges.top && edges.left) || (edges.bottom && edges.right)) {
        setCursor(Qt::SizeFDiagCursor);
        m_rootFrame->setCursor(Qt::SizeFDiagCursor);
    } else if ((edges.top && edges.right) || (edges.bottom && edges.left)) {
        setCursor(Qt::SizeBDiagCursor);
        m_rootFrame->setCursor(Qt::SizeBDiagCursor);
    } else if (edges.left || edges.right) {
        setCursor(Qt::SizeHorCursor);
        m_rootFrame->setCursor(Qt::SizeHorCursor);
    } else if (edges.top || edges.bottom) {
        setCursor(Qt::SizeVerCursor);
        m_rootFrame->setCursor(Qt::SizeVerCursor);
    } else {
        unsetCursor();
        m_rootFrame->unsetCursor();
    }
}

bool UselessWindow::eventFilter(QObject* watched, QEvent* event) {
    if (watched == m_rootFrame || watched == this) {
        const QEvent::Type type = event->type();

        if (type == QEvent::MouseMove) {
            auto* mouseEvent = static_cast<QMouseEvent*>(event);
            const QPoint globalPos = mouseEvent->globalPosition().toPoint();

            if (m_resizing && !m_pressPos.isNull() && !m_pressGeo.isEmpty()) {
                const int dx = globalPos.x() - m_pressPos.x();
                const int dy = globalPos.y() - m_pressPos.y();

                QRect geo = m_pressGeo;
                const int minW = minimumWidth();
                const int minH = minimumHeight();

                if (m_resizeEdges.left) {
                    const int newW = std::max(minW, geo.width() - dx);
                    const int newX = geo.right() - newW + 1;
                    geo.setLeft(newX);
                } else if (m_resizeEdges.right) {
                    geo.setWidth(std::max(minW, geo.width() + dx));
                }

                if (m_resizeEdges.top) {
                    int newH = std::max(minH, geo.height() - dy);
                    int newY = geo.bottom() - newH + 1;
                    QScreen* screen = QGuiApplication::primaryScreen();
                    if (screen) {
                        const QRect screenGeo = screen->availableGeometry();
                        if (newY < screenGeo.y() + 40) {
                            newY = screenGeo.y() + 40;
                            newH = geo.bottom() - newY + 1;
                        }
                    }
                    geo.setTop(newY);
                } else if (m_resizeEdges.bottom) {
                    geo.setHeight(std::max(minH, geo.height() + dy));
                }

                setGeometry(geo);
                return true;
            } else {
                const QPoint localPos = mapFromGlobal(globalPos);
                const Edges edges = getActiveEdges(localPos);
                updateCursorShape(edges);
            }
        } else if (type == QEvent::MouseButtonPress) {
            auto* mouseEvent = static_cast<QMouseEvent*>(event);
            if (mouseEvent->button() == Qt::LeftButton) {
                const QPoint globalPos = mouseEvent->globalPosition().toPoint();
                const QPoint localPos = mapFromGlobal(globalPos);
                const Edges edges = getActiveEdges(localPos);

                if (edges.any()) {
                    Qt::Edges qtEdges;
                    if (edges.top) qtEdges |= Qt::TopEdge;
                    if (edges.bottom) qtEdges |= Qt::BottomEdge;
                    if (edges.left) qtEdges |= Qt::LeftEdge;
                    if (edges.right) qtEdges |= Qt::RightEdge;

                    if (windowHandle() && windowHandle()->startSystemResize(qtEdges)) {
                        return true;
                    }

                    m_resizing = true;
                    m_resizeEdges = edges;
                    m_pressPos = globalPos;
                    m_pressGeo = geometry();
                    return true;
                }
            }
        } else if (type == QEvent::MouseButtonRelease) {
            auto* mouseEvent = static_cast<QMouseEvent*>(event);
            if (mouseEvent->button() == Qt::LeftButton && m_resizing) {
                m_resizing = false;
                m_pressPos = QPoint();
                m_pressGeo = QRect();
                unsetCursor();
                m_rootFrame->unsetCursor();
                return true;
            }
        } else if (type == QEvent::Leave) {
            if (!m_resizing) {
                unsetCursor();
                m_rootFrame->unsetCursor();
            }
        }
    }

    return QMainWindow::eventFilter(watched, event);
}

} // namespace UselessOS
