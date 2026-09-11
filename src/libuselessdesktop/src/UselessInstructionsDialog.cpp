#include "UselessInstructionsDialog.h"
#include "UselessTheme.h"

#include <QVBoxLayout>
#include <QHBoxLayout>
#include <QLabel>
#include <QPushButton>
#include <QGroupBox>
#include <QFrame>
#include <QMouseEvent>
#include <QGuiApplication>
#include <QScreen>
#include <QPixmap>

namespace UselessOS {

UselessInstructionsDialog::UselessInstructionsDialog(const QString& appTitle,
                                                     const QString& appSubtitle,
                                                     const QString& appIcon,
                                                     const QString& accentColor,
                                                     QWidget* parent)
    : QDialog(parent)
{
    setWindowTitle(QStringLiteral("About ") + appTitle);
    setFixedSize(560, 560);
    setWindowFlags(Qt::Dialog | Qt::FramelessWindowHint);
    setAttribute(Qt::WA_TranslucentBackground);
    setModal(true);

    setupUi(appTitle, appSubtitle, appIcon, accentColor);
}

void UselessInstructionsDialog::setupUi(const QString& appTitle,
                                        const QString& appSubtitle,
                                        const QString& appIcon,
                                        const QString& accentColor)
{
    const AppGuide guide = UselessTheme::getAppGuide(appTitle);

    auto* rootLayout = new QVBoxLayout(this);
    rootLayout->setContentsMargins(0, 0, 0, 0);

    m_frame = new QFrame(this);
    m_frame->setObjectName(QStringLiteral("InstructionsModalFrame"));
    m_frame->setStyleSheet(QStringLiteral(
        "QFrame#InstructionsModalFrame {"
        "    background-color: #ffffff;"
        "    border: 2.5px solid #0e0e0d;"
        "    border-radius: 20px;"
        "}"
    ));
    rootLayout->addWidget(m_frame);

    auto* mainLayout = new QVBoxLayout(m_frame);
    mainLayout->setContentsMargins(22, 18, 22, 18);
    mainLayout->setSpacing(10);

    // 1. Header row
    auto* topLayout = new QHBoxLayout();
    topLayout->setSpacing(10);

    const QString iconPath = UselessTheme::getIconPath(appIcon);
    if (!iconPath.isEmpty()) {
        auto* iconLabel = new QLabel(m_frame);
        QPixmap pix(iconPath);
        if (!pix.isNull()) {
            iconLabel->setPixmap(pix.scaled(34, 34, Qt::KeepAspectRatio, Qt::SmoothTransformation));
        }
        iconLabel->setStyleSheet(QStringLiteral("background: transparent; border: none;"));
        topLayout->addWidget(iconLabel);
    }

    auto* titleLabel = new QLabel(appTitle, m_frame);
    titleLabel->setStyleSheet(QStringLiteral(
        "font-family: Helvetica, sans-serif; font-size: 14pt; font-weight: 900; color: #0e0e0d; background: transparent; border: none;"
    ));
    topLayout->addWidget(titleLabel);
    topLayout->addStretch();

    auto* badgeLabel = new QLabel(QStringLiteral("Useless Guide"), m_frame);
    badgeLabel->setStyleSheet(QStringLiteral(
        "background: #0e0e0d; color: #ffffff; border-radius: 8px; font-size: 8pt; font-weight: 800; padding: 4px 10px; font-family: Helvetica;"
    ));
    topLayout->addWidget(badgeLabel);
    mainLayout->addLayout(topLayout);

    // 2. Subtitle row
    if (!appSubtitle.isEmpty()) {
        auto* subLabel = new QLabel(QStringLiteral("•  ") + appSubtitle, m_frame);
        subLabel->setWordWrap(true);
        subLabel->setStyleSheet(QString(
            "font-family: 'NanumPenScript', 'Nanum Pen Script', cursive; font-size: 13pt; color: %1; background: transparent; border: none; margin-top: -2px;"
        ).arg(accentColor));
        mainLayout->addWidget(subLabel);
    }

    // 3. How to Operate GroupBox
    auto* boxUse = new QGroupBox(QStringLiteral("HOW TO OPERATE THIS APPLICATION"), m_frame);
    boxUse->setStyleSheet(QStringLiteral(
        "QGroupBox {"
        "    border: 2px solid #0e0e0d;"
        "    border-radius: 12px;"
        "    margin-top: 14px;"
        "    background-color: #f5f4f0;"
        "    font-family: Helvetica;"
        "    font-weight: 800;"
        "    font-size: 8.5pt;"
        "}"
        "QGroupBox::title {"
        "    subcontrol-origin: margin;"
        "    subcontrol-position: top left;"
        "    padding: 2px 10px;"
        "    background: #0e0e0d;"
        "    color: #ffffff;"
        "    border-radius: 6px;"
        "    font-size: 8pt;"
        "    font-weight: 900;"
        "    left: 14px;"
        "}"
    ));
    auto* useLayout = new QVBoxLayout(boxUse);
    useLayout->setContentsMargins(14, 16, 14, 12);
    useLayout->setSpacing(6);
    int stepNum = 1;
    for (const auto& step : guide.howToUse) {
        auto* stepLabel = new QLabel(QStringLiteral("<b>%1.</b> %2").arg(stepNum++).arg(step), boxUse);
        stepLabel->setWordWrap(true);
        stepLabel->setStyleSheet(QStringLiteral(
            "font-family: Helvetica; font-size: 8.5pt; color: #0e0e0d; background: transparent; border: none; line-height: 130%;"
        ));
        useLayout->addWidget(stepLabel);
    }
    mainLayout->addWidget(boxUse);

    // 4. Philosophical Logic GroupBox
    auto* boxPhil = new QGroupBox(QStringLiteral("THE IMPRACTICAL PHILOSOPHY && LOGIC"), m_frame);
    boxPhil->setStyleSheet(QStringLiteral(
        "QGroupBox {"
        "    border: 2px solid #0e0e0d;"
        "    border-radius: 12px;"
        "    margin-top: 14px;"
        "    background-color: #ffffff;"
        "    font-family: Helvetica;"
        "    font-weight: 800;"
        "    font-size: 8.5pt;"
        "}"
        "QGroupBox::title {"
        "    subcontrol-origin: margin;"
        "    subcontrol-position: top left;"
        "    padding: 2px 10px;"
        "    background: #ea34df;"
        "    color: #ffffff;"
        "    border-radius: 6px;"
        "    font-size: 8pt;"
        "    font-weight: 900;"
        "    left: 14px;"
        "}"
    ));
    auto* philLayout = new QVBoxLayout(boxPhil);
    philLayout->setContentsMargins(14, 16, 14, 12);
    auto* philLabel = new QLabel(QStringLiteral("<i>\"%1\"</i>").arg(guide.philosophy), boxPhil);
    philLabel->setWordWrap(true);
    philLabel->setStyleSheet(QStringLiteral(
        "font-family: Helvetica; font-size: 8.5pt; color: #244638; background: transparent; border: none; line-height: 135%;"
    ));
    philLayout->addWidget(philLabel);
    mainLayout->addWidget(boxPhil);

    mainLayout->addStretch();

    // 5. Understood Button
    auto* btnClose = new QPushButton(QStringLiteral("Understood (Carry On)"), m_frame);
    btnClose->setCursor(Qt::PointingHandCursor);
    btnClose->setFixedHeight(38);
    btnClose->setStyleSheet(QStringLiteral(
        "QPushButton {"
        "    background-color: #0e0e0d;"
        "    color: #ffffff;"
        "    border: 2px solid #0e0e0d;"
        "    border-radius: 19px;"
        "    font-family: Helvetica;"
        "    font-weight: 800;"
        "    font-size: 9.5pt;"
        "}"
        "QPushButton:hover {"
        "    background-color: #00c2cb;"
        "    color: #0e0e0d;"
        "}"
    ));
    connect(btnClose, &QPushButton::clicked, this, &QDialog::accept);
    mainLayout->addWidget(btnClose);
}

void UselessInstructionsDialog::mousePressEvent(QMouseEvent* event) {
    if (event->button() == Qt::LeftButton) {
        m_dragging = true;
        m_dragPos = event->globalPosition().toPoint() - frameGeometry().topLeft();
        event->accept();
    } else {
        QDialog::mousePressEvent(event);
    }
}

void UselessInstructionsDialog::mouseMoveEvent(QMouseEvent* event) {
    if (m_dragging && (event->buttons() & Qt::LeftButton)) {
        QPoint target = event->globalPosition().toPoint() - m_dragPos;
        QScreen* screen = QGuiApplication::primaryScreen();
        if (screen) {
            const QRect sg = screen->availableGeometry();
            target.setY(std::max(sg.y() + 40, std::min(target.y(), sg.bottom() - 60)));
            target.setX(std::max(sg.x() - width() + 100, std::min(target.x(), sg.right() - 100)));
        }
        move(target);
        event->accept();
    } else {
        QDialog::mouseMoveEvent(event);
    }
}

void UselessInstructionsDialog::mouseReleaseEvent(QMouseEvent* event) {
    m_dragging = false;
    event->accept();
}

} // namespace UselessOS
