#pragma once

#include <QDialog>
#include <QString>
#include <QPoint>

class QFrame;
class QLabel;
class QPushButton;

namespace UselessOS {

/**
 * @brief Modal instructions & impractical philosophical manifesto dialog.
 */
class UselessInstructionsDialog : public QDialog {
    Q_OBJECT

public:
    explicit UselessInstructionsDialog(const QString& appTitle,
                                      const QString& appSubtitle,
                                      const QString& appIcon,
                                      const QString& accentColor,
                                      QWidget* parent = nullptr);
    ~UselessInstructionsDialog() override = default;

protected:
    void mousePressEvent(QMouseEvent* event) override;
    void mouseMoveEvent(QMouseEvent* event) override;
    void mouseReleaseEvent(QMouseEvent* event) override;

private:
    void setupUi(const QString& appTitle,
                 const QString& appSubtitle,
                 const QString& appIcon,
                 const QString& accentColor);

    QPoint m_dragPos;
    bool m_dragging{false};
    QFrame* m_frame{nullptr};
};

} // namespace UselessOS
