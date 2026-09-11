#include "CustomTitleBar.h"
#include "UselessWindow.h"
#include "UselessTheme.h"

#include <QHBoxLayout>
#include <QLabel>
#include <QPushButton>
#include <QMouseEvent>
#include <QGuiApplication>
#include <QScreen>
#include <QPixmap>
#include <QWindow>

namespace UselessOS {

CustomTitleBar::CustomTitleBar(UselessWindow* parent,
                               const QString& title,
                               const QString& subtitle,
                               const QString& iconName,
                               const QString& accentColor)
    : QWidget(parent)
    , m_parentWindow(parent)
{
    setFixedHeight(42);
    setObjectName(QStringLiteral("CustomTitleBar"));
    setStyleSheet(QStringLiteral(
        "#CustomTitleBar {"
        "    background-color: #f5f4f0;"
        "    border-bottom: 2px solid #0e0e0d;"
        "    border-top-left-radius: 14px;"
        "    border-top-right-radius: 14px;"
        "}"
    ));

    auto* layout = new QHBoxLayout(this);
    layout->setContentsMargins(14, 0, 14, 0);
    layout->setSpacing(10);
    layout->setAlignment(Qt::AlignVCenter);

    // 1. macOS Traffic Light Window Controls
    auto* lights = new QHBoxLayout();
    lights->setSpacing(8);
    lights->setContentsMargins(0, 0, 8, 0);

    // Close (Red)
    m_btnClose = new QPushButton(QStringLiteral("✕"), this);
    m_btnClose->setToolTip(QStringLiteral("Close"));
    m_btnClose->setFixedSize(14, 14);
    m_btnClose->setCursor(Qt::PointingHandCursor);
    m_btnClose->setStyleSheet(QStringLiteral(
        "QPushButton {"
        "    background-color: #ff5f56;"
        "    color: transparent;"
        "    border: 1.5px solid #0e0e0d;"
        "    border-radius: 7px;"
        "    font-size: 8px;"
        "    font-weight: 900;"
        "    padding: 0px;"
        "}"
        "QPushButton:hover {"
        "    color: #5c0000;"
        "    background-color: #ff5f56;"
        "}"
    ));
    connect(m_btnClose, &QPushButton::clicked, m_parentWindow, &QMainWindow::close);
    lights->addWidget(m_btnClose);

    // Minimize (Yellow)
    m_btnMin = new QPushButton(QStringLiteral("—"), this);
    m_btnMin->setToolTip(QStringLiteral("Minimize"));
    m_btnMin->setFixedSize(14, 14);
    m_btnMin->setCursor(Qt::PointingHandCursor);
    m_btnMin->setStyleSheet(QStringLiteral(
        "QPushButton {"
        "    background-color: #ffbd2e;"
        "    color: transparent;"
        "    border: 1.5px solid #0e0e0d;"
        "    border-radius: 7px;"
        "    font-size: 8px;"
        "    font-weight: 900;"
        "    padding: 0px;"
        "}"
        "QPushButton:hover {"
        "    color: #5c3b00;"
        "    background-color: #ffbd2e;"
        "}"
    ));
    connect(m_btnMin, &QPushButton::clicked, m_parentWindow, &QMainWindow::showMinimized);
    lights->addWidget(m_btnMin);

    // Maximize / Restore (Green)
    m_btnMax = new QPushButton(QStringLiteral("+"), this);
    m_btnMax->setToolTip(QStringLiteral("Maximize / Restore"));
    m_btnMax->setFixedSize(14, 14);
    m_btnMax->setCursor(Qt::PointingHandCursor);
    m_btnMax->setStyleSheet(QStringLiteral(
        "QPushButton {"
        "    background-color: #27c93f;"
        "    color: transparent;"
        "    border: 1.5px solid #0e0e0d;"
        "    border-radius: 7px;"
        "    font-size: 8px;"
        "    font-weight: 900;"
        "    padding: 0px;"
        "}"
        "QPushButton:hover {"
        "    color: #004d10;"
        "    background-color: #27c93f;"
        "}"
    ));
    connect(m_btnMax, &QPushButton::clicked, m_parentWindow, &UselessWindow::toggleMaximized);
    lights->addWidget(m_btnMax);

    layout->addLayout(lights);

    // 2. Bespoke Squircle App Icon
    const QString iconPath = UselessTheme::getIconPath(iconName);
    if (!iconPath.isEmpty()) {
        auto* iconLbl = new QLabel(this);
        QPixmap pix(iconPath);
        if (!pix.isNull()) {
            iconLbl->setPixmap(pix.scaled(22, 22, Qt::KeepAspectRatio, Qt::SmoothTransformation));
        }
        iconLbl->setFixedSize(22, 22);
        iconLbl->setStyleSheet(QStringLiteral("background: transparent; border: none;"));
        layout->addWidget(iconLbl);
    }

    // 3. App Title (Helvetica Bold)
    auto* titleLbl = new QLabel(title, this);
    titleLbl->setStyleSheet(QStringLiteral(
        "font-family: Helvetica, sans-serif; font-size: 11pt; font-weight: 900; color: #0e0e0d; background: transparent; border: none;"
    ));
    layout->addWidget(titleLbl);

    // 4. Whimsical Handwritten Tagline (NanumPenScript)
    if (!subtitle.isEmpty()) {
        auto* subLbl = new QLabel(QStringLiteral("•  ") + subtitle, this);
        subLbl->setMaximumWidth(240);
        subLbl->setStyleSheet(QString(
            "font-family: 'NanumPenScript', 'Nanum Pen Script', cursive; font-size: 13pt; font-weight: bold; color: %1; background: transparent; border: none;"
        ).arg(accentColor));
        layout->addWidget(subLbl);
    }

    layout->addStretch();

    // 5. OS Badge Pill
    auto* pill = new QLabel(QStringLiteral("UselessOS 3.0"), this);
    pill->setStyleSheet(QStringLiteral(
        "QLabel {"
        "    background-color: #ffffff;"
        "    color: #0e0e0d;"
        "    border: 1.5px solid #0e0e0d;"
        "    border-radius: 10px;"
        "    font-family: Helvetica, sans-serif;"
        "    font-size: 8pt;"
        "    font-weight: 800;"
        "    padding: 2px 8px;"
        "}"
    ));
    layout->addWidget(pill);

    // 6. Question Mark Button for App Instructions & Logic
    m_btnHelp = new QPushButton(QStringLiteral("?"), this);
    m_btnHelp->setToolTip(QStringLiteral("Application Instructions & Philosophical Logic"));
    m_btnHelp->setCursor(Qt::PointingHandCursor);
    m_btnHelp->setFixedSize(22, 22);
    m_btnHelp->setStyleSheet(QStringLiteral(
        "QPushButton {"
        "    background-color: #ffffff;"
        "    color: #0e0e0d;"
        "    border: 1.5px solid #0e0e0d;"
        "    border-radius: 11px;"
        "    font-family: Helvetica, sans-serif;"
        "    font-size: 9pt;"
        "    font-weight: 900;"
        "    padding: 0px;"
        "}"
        "QPushButton:hover {"
        "    background-color: #00c2cb;"
        "    color: #ffffff;"
        "    border: 1.5px solid #0e0e0d;"
        "}"
    ));
    connect(m_btnHelp, &QPushButton::clicked, m_parentWindow, &UselessWindow::showInstructionsDialog);
    layout->addWidget(m_btnHelp);
}

void CustomTitleBar::mouseDoubleClickEvent(QMouseEvent* event) {
    if (event->button() == Qt::LeftButton) {
        m_parentWindow->toggleMaximized();
        event->accept();
    } else {
        QWidget::mouseDoubleClickEvent(event);
    }
}

void CustomTitleBar::mousePressEvent(QMouseEvent* event) {
    if (event->button() == Qt::LeftButton) {
        if (m_parentWindow->isMaximized()) {
            m_parentWindow->toggleMaximized();
        }

        // Native Wayland / modern compositor system move
        if (window() && window()->windowHandle()) {
            if (window()->windowHandle()->startSystemMove()) {
                event->accept();
                return;
            }
        }

        // Fallback for legacy environments where startSystemMove() is unhandled
        m_dragging = true;
        m_dragPos = event->globalPosition().toPoint() - m_parentWindow->frameGeometry().topLeft();
        event->accept();
    } else {
        QWidget::mousePressEvent(event);
    }
}

void CustomTitleBar::mouseMoveEvent(QMouseEvent* event) {
    if (m_dragging && (event->buttons() & Qt::LeftButton)) {
        const QPoint globalPos = event->globalPosition().toPoint();
        const QPoint targetPos = globalPos - m_dragPos;

        QScreen* screen = QGuiApplication::primaryScreen();
        if (screen) {
            const QRect screenGeo = screen->availableGeometry();
            // Strict macOS top-bar boundary: never allow titlebar above y=40
            const int clampedY = std::max(screenGeo.y() + 40, targetPos.y());
            const int clampedX = std::max(screenGeo.x() - m_parentWindow->width() + 80,
                                          std::min(screenGeo.right() - 80, targetPos.x()));
            m_parentWindow->move(clampedX, clampedY);
        } else {
            m_parentWindow->move(targetPos);
        }
        event->accept();
    } else {
        QWidget::mouseMoveEvent(event);
    }
}

void CustomTitleBar::mouseReleaseEvent(QMouseEvent* event) {
    m_dragging = false;
    event->accept();
}

} // namespace UselessOS
