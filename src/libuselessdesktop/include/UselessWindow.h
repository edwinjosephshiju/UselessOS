#pragma once

#include <QMainWindow>
#include <QString>
#include <QRect>
#include <QPoint>

class QFrame;
class QVBoxLayout;
class QScrollArea;

namespace UselessOS {

class CustomTitleBar;

/**
 * @brief Standard window framework for all native UselessOS applications.
 *
 * Implements a unified macOS-inspired Neobrutalist frame with custom traffic lights,
 * crisp 2px solid borders, 16px corner radius, dedicated scrollable content area,
 * shape masking for clean corner rendering, and a robust 8-directional frameless resizing engine.
 */
class UselessWindow : public QMainWindow {
    Q_OBJECT

public:
    static constexpr int ResizeMargin = 8;

    explicit UselessWindow(const QString& title = QStringLiteral("Useless Application"),
                           const QString& subtitle = QString(),
                           const QString& iconName = QString(),
                           const QString& accentColor = QStringLiteral("#ea34df"),
                           int width = 620,
                           int height = 520,
                           QWidget* parent = nullptr);
    ~UselessWindow() override = default;

    /**
     * @brief Access the layout where application content widgets should be added.
     */
    QVBoxLayout* contentLayout() const { return m_contentLayout; }

    /**
     * @brief Access the inner content container widget.
     */
    QWidget* contentWidget() const { return m_contentWidget; }

    /**
     * @brief Access the custom title bar.
     */
    CustomTitleBar* titleBar() const { return m_titleBar; }

    /**
     * @brief Check whether window is currently maximized.
     */
    bool isMaximized() const { return m_isMaximized; }

    /**
     * @brief Application title string.
     */
    QString appTitle() const { return m_appTitle; }

    /**
     * @brief Application subtitle string.
     */
    QString appSubtitle() const { return m_appSubtitle; }

    /**
     * @brief Application icon name.
     */
    QString appIcon() const { return m_appIcon; }

    /**
     * @brief Application accent color hex code.
     */
    QString appAccent() const { return m_appAccent; }

public Q_SLOTS:
    /**
     * @brief Toggles between maximized (screen-clamped for dock/topbar clearance) and normal geometry.
     */
    void toggleMaximized();

    /**
     * @brief Displays the in-app philosophical logic and operation guide dialog.
     */
    void showInstructionsDialog();

protected:
    void resizeEvent(QResizeEvent* event) override;
    bool eventFilter(QObject* watched, QEvent* event) override;

private:
    struct Edges {
        bool top{false};
        bool bottom{false};
        bool left{false};
        bool right{false};

        bool any() const { return top || bottom || left || right; }
    };

    Edges getActiveEdges(const QPoint& localPos) const;
    void updateCursorShape(const Edges& edges);
    void updateWindowMask();

    QString m_appTitle;
    QString m_appSubtitle;
    QString m_appIcon;
    QString m_appAccent;

    QFrame* m_rootFrame{nullptr};
    CustomTitleBar* m_titleBar{nullptr};
    QScrollArea* m_scrollArea{nullptr};
    QWidget* m_contentWidget{nullptr};
    QVBoxLayout* m_contentLayout{nullptr};

    bool m_isMaximized{false};
    QRect m_normalGeo;

    // Resizing engine state
    bool m_resizing{false};
    Edges m_resizeEdges;
    QPoint m_pressPos;
    QRect m_pressGeo;
};

} // namespace UselessOS
