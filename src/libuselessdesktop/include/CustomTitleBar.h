#pragma once

#include <QWidget>
#include <QString>
#include <QPoint>

class QPushButton;
class QLabel;

namespace UselessOS {

class UselessWindow;

/**
 * @brief macOS-inspired Brutalist client-side window title bar.
 *
 * Features traffic light controls, bespoke squircle app icon, bold typography,
 * handwritten tagline, OS pill badge, help button, and smooth screen-clamped dragging.
 */
class CustomTitleBar : public QWidget {
    Q_OBJECT

public:
    explicit CustomTitleBar(UselessWindow* parent,
                           const QString& title = QStringLiteral("Application"),
                           const QString& subtitle = QString(),
                           const QString& iconName = QString(),
                           const QString& accentColor = QStringLiteral("#ea34df"));
    ~CustomTitleBar() override = default;

protected:
    void mousePressEvent(QMouseEvent* event) override;
    void mouseMoveEvent(QMouseEvent* event) override;
    void mouseReleaseEvent(QMouseEvent* event) override;
    void mouseDoubleClickEvent(QMouseEvent* event) override;

private:
    UselessWindow* m_parentWindow{nullptr};
    QPushButton* m_btnClose{nullptr};
    QPushButton* m_btnMin{nullptr};
    QPushButton* m_btnMax{nullptr};
    QPushButton* m_btnHelp{nullptr};
    QPoint m_dragPos;
    bool m_dragging{false};
};

} // namespace UselessOS
